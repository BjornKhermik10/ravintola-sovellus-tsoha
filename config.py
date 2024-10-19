import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    COLOR_MAP = {
        1: "#FA6F6F",  # Red
        2: "#5CAEFA",  # Blue
        3: "#006D05",  # Green
        4: "#CA66F8",  # Purple
        5: "#808080",  # Grey
    }
