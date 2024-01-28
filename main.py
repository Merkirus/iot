import datetime

from Database import models, database, crud, schemas
from Server.request_handler import RequestHandler

models.Base.metadata.create_all(bind=database.engine)




if __name__ == '__main__':

    req = RequestHandler("http://localhost:8000")
    # req.post_card(5754356)
    req.post_card(47364736)