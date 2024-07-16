#!/usr/bin/env python3
"""
Inserts a new document into a MongoDB collection based on keyword arguments.
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document into the MongoDB collection with the given fields.

    Args:
        mongo_collection (pymongo.collection.Collection):
        The PyMongo collection object.
        **kwargs: Keyword arguments representing document fields.

    Returns:
        str: The _id of the newly inserted document.
    """
    result = mongo_collection.insert_one(kwargs)
    return str(result.inserted_id)
