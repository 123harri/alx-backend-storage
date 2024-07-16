#!/usr/bin/env python3
"""
Updates topics of a school document based on the school name.
"""


def update_topics(mongo_collection, name, topics):
    """
    Updates the 'topics' field of a school document in the
    MongoDB collection based on the school name.

    Args:
        mongo_collection (pymongo.collection.Collection):
        The PyMongo collection object.
        name (str): The name of the school to update.
        topics (list): List of topics (strings) to update or set.

    Returns:
        None
    """
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )
