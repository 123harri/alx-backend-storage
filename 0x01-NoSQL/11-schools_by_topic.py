#!/usr/bin/env python3
"""
Returns a list of schools that have a specific topic.
"""


def schools_by_topic(mongo_collection, topic):
    """
    Retrieves a list of schools from MongoDB
    collection that have the specified topic.

    Args:
        mongo_collection (pymongo.collection.Collection):
        The PyMongo collection object.
        topic (str): The topic to search for.

    Returns:
        list: List of school documents (dictionaries).
    """
    topic_filter = {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
            },
        },
    }
    return [doc for doc in mongo_collection.find(topic_filter)]
