# db/connection.py

from pymongo import MongoClient
from utils.config import MONGODB_URI, DB_NAME

def get_mongo_collection(collection_name):
    """
    Establece la conexión a MongoDB y obtiene una colección específica.
    Args:
        collection_name (str): Nombre de la colección a acceder.
    Returns:
        pymongo.collection.Collection: Objeto de colección de MongoDB.
    """
    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]
    return db[collection_name]
