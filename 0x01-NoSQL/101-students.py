#!/usr/bin/env python3
'''Task 14's module.
'''
from pymongo import MongoClient


def top_students(mongo_collection):
    '''Returns all students sorted by average score.
    '''
    pipeline = [
        {
            '$project': {
                'name': 1,
                'topics': 1,
                'averageScore': {
                    '$avg': '$topics.score'
                }
            }
        },
        {
            '$sort': {'averageScore': -1}
        }
    ]

    students = list(mongo_collection.aggregate(pipeline))

    return students
