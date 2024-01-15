from __future__ import annotations

from dataclasses import dataclass

STYLE_START_CHAR = "\x1b"
STYLE_END_CHAR = "m"

UNSETTER_LOOKUP = {
    **{"38": {"39"}, "48": {"49"}, "54": {"53"}},
    **{str(index + 20): {str(index)} for index in range(1, 10)},
    **{"22": {"1", "2"}},
}


def _is_color(style: str) -> bool:
    """Determines whether the given style string is a color."""

    if style.startswith(("38", "48")):
        return True

    if style.isdigit():
        index = int(style)

        if 30 <= index <= 38 or 40 <= index <= 48:
            return True

    return False


def _process_styles(styles: list[str]) -> tuple[list[str], str, str]:
    """Processes the given styles, cleaning them up along the way.

    This does 2 major tasks:

    - Remove styles that are unset by later ones
    - Extract the fore and background colors, returning them

    Args:
        style: The list of styles to process.

    Returns:
        A tuple containing:

        - The processed list of styles
        - The foreground color
        - The background color
    """

    # TODO: Split up compound styles before handling them.

    applied = []
    foreground = ""
    background = ""

    for style in styles:
        unset_styles = UNSETTER_LOOKUP.get(style)

        if _is_color(style):
            if style.startswith("3"):
                foreground = style
            else:
                background = style

            continue

        if style == "39":
            foreground = ""

        elif style == "49":
            background = ""

        elif style == "0":
            applied = []
            foreground = ""
            background = ""

        elif unset_styles is not None:
            for unset_style in unset_styles:
                if unset_style in applied:
                    applied.remove(unset_style)

        if style not in applied:
            applied.append(style)

    if foreground:
        applied.append(foreground)

    if background:
        applied.append(background)

    return applied, foreground, background


def _split(styles: str) -> list[str]:
    """Splits styles into a list of their content.

    For example, `\x1b[38;5;141;1m` would become `38;5;141` and `1`.
    """

    return [style.rstrip("m") for style in styles.split("\x1b[")[1:]]


def _combine(styles: list[str]) -> str:
    """Combines a list of style content into a compound style setter.

    Instead of doing individual tags, it puts all of the styles into
    a single unit, i.e. instead of `\x1b[38;5;141m\x1b[1m` it returns
    `\x1b[38;5;141;1m`.
    """

    if len(styles) == 0:
        return ""

    return f"\x1b[{';'.join(styles)}{STYLE_END_CHAR}"


@dataclass
class Cell:
    """A unit that represents a single, possibly ANSI-styled character."""

    char: str = ""
    styles: str = ""

    _foreground: str | None = None
    _background: str | None = None

    def __str__(self) -> str:
        """Gets the content of this cell."""

        return self.styles + self.char

    @property
    def foreground(self) -> str | None:
        """Returns the currently set foreground color in this cell."""

        return self._foreground

    @foreground.setter
    def foreground(self, new: str | None) -> None:
        """Allows setting the foreground color, while unsetting the current one."""

        current = self.foreground

        if current is not None:
            self.styles = self.styles.replace(current, "")

        self.styles += new

        if new is not None:
            self._foreground = f"\x1b[{new}m"

        else:
            self._foreground = None

    @property
    def background(self) -> str | None:
        """Returns the currently set background color in this cell."""

        return self._background

    @background.setter
    def background(self, new: str | None) -> None:
        """Allows setting the background color, while unsetting the current one."""

        current = self.background

        if current is not None:
            self.styles = self.styles.replace(current, "")

        self.styles += new

        if new is not None:
            self._background = f"\x1b[{new}m"

        else:
            self._background = None

    @classmethod
    def from_line(cls, line: str, styles: str = "") -> Generator[None, None, Cell]:
        """Yields Cells generated from a line of text.

        Args:
            line: The input line. May or may not contain ANSI styles.
            styles: Styles that are applied to the line from before the line started.

        Returns:
            A Cell generator.
        """

        in_style = False
        current_style = styles
        current_styles = []

        for char in line:
            if char == STYLE_START_CHAR:
                in_style = True
                current_style = ""
                continue

            if in_style:
                if char == "[":
                    continue

                if char == STYLE_END_CHAR:
                    current_styles.append(current_style)
                    in_style = False
                    continue

                current_style += char
                continue

            current_styles, fore, back = _process_styles(current_styles)

            yield Cell(char or " ", _combine(current_styles), fore, back)

        if current_style != "":
            current_styles, fore, back = _process_styles(
                current_styles + [current_style]
            )

            yield Cell("", _combine(current_styles), fore, back)

    @classmethod
    def first_of(cls, line: str) -> Cell:
        """Returns the first cell yielded by `from_line`."""

        for cell in cls.from_line(line):
            return cell


class CellMatrix:
    def __init__(self, width: int, height: int, default: str = " ") -> None:
        self._cells = []
        self._changes: list[tuple[int, int, Cell]] = []

        for _ in range(height):
            row = []

            for _ in range(width):
                row.append(Cell(default))

            self._cells.append(row)

        self.width = width
        self.height = height

    def resize(self, width: int, height: int, default: str = " ") -> None:
        diff_cols = width - self.width
        diff_rows = height - self.height

        default_cell = list(Cell.from_line(default))[0]

        for row in range(self.height):
            self._cells[row].extend([default_cell] * diff_cols)

        for _ in range(diff_rows):
            self._cells.append([default_cell] * (width))

        self.width, self.height = width, height

    def add_text(
        self, text: str, offset: tuple[int, int] = (0, 0), register_change: bool = True
    ) -> None:
        x, y = offset

        if y >= self.height:
            return

        for i, cell in enumerate(Cell.from_line(text)):
            # Sometimes some styles (usually the global unsetter 0) are left over at
            # the end of a line of text. These are dealt with here; overflowing either
            # into the next cell in the same row, or the first cell of the next one.
            if cell.char == "":
                if x + i < self.width:
                    self._cells[y][x + i].styles += cell.styles

                else:
                    if y + 1 >= self.height:
                        continue

                    self._cells[y + 1][0].styles += cell.styles

                continue

            if self.width <= x + i:
                break

            if self._cells[y][x + i] != cell:
                self._cells[y][x + i] = cell

                if register_change:
                    self._changes.append((x + i, y, cell))

    def fill(self, content: str) -> None:
        for row in range(self.height):
            for col in range(self.width):
                self.add_text(content, (col, row), register_change=False)

    def build_lines(self) -> list[str]:
        lines = []
        for row in self._cells:
            buff = ""

            for cell in row:
                buff += str(cell)

            lines.append(buff + "")

        return lines

    def get_diff(self, origin: tuple[int, int] = (1, 1)) -> tuple[str, int]:
        buff = ""

        for x, y, cell in self._changes:
            buff += f"\x1b[{y + origin[1]};{x + origin[0]}H{cell}"

        change_count = len(self._changes)
        self._changes.clear()

        return buff, change_count
