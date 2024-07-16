#!/usr/bin/env python3
"""
Lists all documents in a MongoDB collection.
"""


def list_all(mongo_collection):
    """
    Lists all documents in the given MongoDB collection.

    Args:
        mongo_collection (pymongo.collection.Collection):
        The PyMongo collection object.

    Returns:
        list: A list of documents (dictionaries).
    """
    return [doc for doc in mongo_collection.find()]
