"""
Hands-On 5 - pymongo equivalent

pymongo is listed as a required package for this module, so this file
reproduces the same CRUD + aggregation operations from hands_on_5.js
using Python, for anyone who prefers scripting this in Python instead of
mongosh/Compass.
"""

from datetime import datetime
from pymongo import MongoClient, ASCENDING

client = MongoClient("mongodb://localhost:27017/")
db = client["college_nosql"]
feedback = db["feedback"]

# Task 1: insert documents (abbreviated - see hands_on_5.js for the full 10)
sample_docs = [
    {
        "student_id": 1, "course_code": "CS101", "semester": "2022-ODD",
        "rating": 5, "comments": "Excellent teaching. Would recommend.",
        "tags": ["challenging", "well-structured", "good-examples"],
        "submitted_at": datetime(2022, 11, 30, 10, 15),
        "attachments": [{"filename": "notes.pdf", "size_kb": 240}],
    },
    {
        "student_id": 5, "course_code": "CS102", "semester": "2022-ODD",
        "rating": 5, "comments": "Best course this semester.",
        "tags": ["well-structured", "engaging"],
        "submitted_at": datetime(2022, 11, 29, 16, 45),
        # intentionally no attachments field
    },
]
feedback.insert_many(sample_docs)
print("Document count:", feedback.count_documents({}))

# Task 2: CRUD
five_star = list(feedback.find({"rating": 5}))
print("5-star feedback count:", len(five_star))

cs101_challenging = list(feedback.find({"course_code": "CS101", "tags": "challenging"}))
print("CS101 'challenging' feedback:", len(cs101_challenging))

projected = list(feedback.find({}, {"student_id": 1, "course_code": 1, "rating": 1, "_id": 0}))
print("Sample projection:", projected[:2])

feedback.update_many({"rating": {"$lt": 3}}, {"$set": {"needs_review": True}})
feedback.update_many({"needs_review": True}, {"$push": {"tags": "reviewed"}})
feedback.delete_many({"semester": "2021-EVEN"})

# Task 3: aggregation pipeline
pipeline = [
    {"$match": {"semester": "2022-ODD"}},
    {"$group": {
        "_id": "$course_code",
        "avg_rating": {"$avg": "$rating"},
        "total_feedback": {"$sum": 1},
    }},
    {"$project": {
        "_id": 0,
        "course_code": "$_id",
        "average_rating": {"$round": ["$avg_rating", 1]},
        "total_feedback": 1,
    }},
    {"$sort": {"average_rating": -1}},
]
print("Per-course averages:", list(feedback.aggregate(pipeline)))

tag_pipeline = [
    {"$unwind": "$tags"},
    {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
]
print("Tag frequency leaderboard:", list(feedback.aggregate(tag_pipeline)))

# Step 74: index + explain
feedback.create_index([("course_code", ASCENDING)])
plan = feedback.find({"course_code": "CS101"}).explain()
stage = plan["executionStats"]["executionStages"]["stage"]
print("Query plan stage for course_code lookup:", stage)  # expect IXSCAN
