import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()  # reads the .env file

client = MongoClient(os.getenv("MONGO_URI"))
db = client["shopping_db"]
products_collection = db["products"]