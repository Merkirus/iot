from pytermgui.cell import (
    Cell,
    CellMatrix,
    _is_color,
    _combine,
    _split,
    _process_styles,
)


def test_is_color():
    assert _is_color("31")
    assert _is_color("45")
    assert _is_color("38;5;141")
    assert _is_color("48;5;61")
    assert _is_color("38;2;22;33;44")
    assert _is_color("48;2;22;33;44")

    assert not _is_color("1")
    assert not _is_color("9")
    assert not _is_color("22")
    assert not _is_color("1")


def test_combine():
    assert _combine(["41", "38;5;141", "1"]) == "\x1b[41;38;5;141;1m"


def test_split():
    assert _split("\x1b[38;2;53;12;123m\x1b[1m\x1b[9m\x1b[48;2;21;21;21m") == [
        "38;2;53;12;123",
        "1",
        "9",
        "48;2;21;21;21",
    ]


def test_process_styles():
    tests = [
        # Bold & Dim both get unset by the same unsetter
        (["38;5;141", "1", "9", "2", "22"], {"38;5;141", "9", "22"}),
        # 0 unsets everything
        (["38;2;66;66;66", "1", "0"], {"0"}),
        # Duplicates are ignored
        (["1", "1", "9"], {"1", "9"}),
        # Foreground colors work; background ones unset
        (["38;5;131", "1", "41", "49"], {"38;5;131", "1", "49"}),
        # Background colors work; foreground ones unset
        (["48;2;33;44;55", "7", "35", "39"], {"48;2;33;44;55", "7", "39"}),
    ]

    for target, expected in tests:
        output = _process_styles(target)[0]

        if len(set(output)) != len(output):
            raise ValueError(f"Output {output} contains duplicates.")

        assert set(output) == expected


def test_cell_from_line():
    tests = [
        # General example
        (
            "\x1b[38;5;141\x1b[1mHello\x1b[7mThere",
            [
                Cell("H", "\x1b[38;5;141;1m", "38;5;141"),
                Cell("e", "\x1b[38;5;141;1m", "38;5;141"),
                Cell("l", "\x1b[38;5;141;1m", "38;5;141"),
                Cell("l", "\x1b[38;5;141;1m", "38;5;141"),
                Cell("o", "\x1b[38;5;141;1m", "38;5;141"),
                Cell("T", "\x1b[7;38;5;141;1m", "38;5;141"),
                Cell("h", "\x1b[7;38;5;141;1m", "38;5;141"),
                Cell("e", "\x1b[7;38;5;141;1m", "38;5;141"),
                Cell("r", "\x1b[7;38;5;141;1m", "38;5;141"),
                Cell("e", "\x1b[7;38;5;141;1m", "38;5;141"),
                # Trailing style
                Cell("", "\x1b[7;38;5;141;1m", "38;5;141"),
            ],
        ),
        # Achy breaky code (chode)
        # Unsetters & trailing
        (
            "\x1b[1m\x1b[33m1\x1b[22m2\x1b[0m",
            [
                Cell(char="1", styles="\x1b[1;33m"),
                Cell(char="2", styles="\x1b[22;33m"),
                Cell(char="", styles="\x1b[0m"),
            ],
        ),
        # (Future) Compound styles
        # (
        #     "\x1b[1;33m1\x1b[22m2\x1b[0m",
        #     [
        #         Cell(char="1", styles="\x1b[1;33m"),
        #         Cell(char="2", styles="\x1b[22;33m"),
        #         Cell(char="", styles="\x1b[0m"),
        #     ],
        # ),
    ]

    for target, expected in tests:
        assert list(Cell.from_line(target)) == expected


def test_cell_foreground():
    assert Cell.first_of("\x1b[38;5;141mHello there").foreground == "\x1b[38;5;141m"


def test_cell_matrix_resize():
    mat = CellMatrix(5, 5, default="x")
    mat.resize(10, 10, default="O")

    assert mat.build_lines() == [
        "xxxxxOOOOO",
        "xxxxxOOOOO",
        "xxxxxOOOOO",
        "xxxxxOOOOO",
        "xxxxxOOOOO",
        "OOOOOOOOOO",
        "OOOOOOOOOO",
        "OOOOOOOOOO",
        "OOOOOOOOOO",
        "OOOOOOOOOO",
    ]
