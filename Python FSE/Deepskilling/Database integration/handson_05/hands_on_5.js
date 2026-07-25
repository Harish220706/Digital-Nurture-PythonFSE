// =====================================================================
// HANDS-ON 5: MongoDB — Document Modelling, CRUD & Aggregation
// Run with: mongosh < hands_on_5.js   (or paste sections into mongosh / Compass)
// =====================================================================

use college_nosql;

// =====================================================================
// Task 1: Create the Collection and Insert Documents (Steps 60-64)
// =====================================================================

db.createCollection("feedback");

db.feedback.insertMany([
  {
    student_id: 1, course_code: "CS101", semester: "2022-ODD", rating: 5,
    comments: "Excellent teaching. Would recommend.",
    tags: ["challenging", "well-structured", "good-examples"],
    submitted_at: ISODate("2022-11-30T10:15:00Z"),
    attachments: [{ filename: "notes.pdf", size_kb: 240 }]
  },
  {
    student_id: 2, course_code: "CS101", semester: "2022-ODD", rating: 4,
    comments: "Good pace, occasionally too fast.",
    tags: ["challenging", "fast-paced"],
    submitted_at: ISODate("2022-11-30T11:00:00Z"),
    attachments: [{ filename: "assignment1.pdf", size_kb: 120 }]
  },
  {
    student_id: 5, course_code: "CS101", semester: "2022-ODD", rating: 2,
    comments: "Hard to follow, needs clearer examples.",
    tags: ["challenging", "unclear"],
    submitted_at: ISODate("2022-12-01T09:30:00Z"),
    attachments: [{ filename: "notes.pdf", size_kb: 240 }]
  },
  {
    student_id: 1, course_code: "CS102", semester: "2022-ODD", rating: 4,
    comments: "Solid coverage of database fundamentals.",
    tags: ["well-structured", "good-examples"],
    submitted_at: ISODate("2022-11-28T14:00:00Z"),
    attachments: [{ filename: "er_diagrams.pdf", size_kb: 310 }]
  },
  {
    student_id: 5, course_code: "CS102", semester: "2022-ODD", rating: 5,
    comments: "Best course this semester.",
    tags: ["well-structured", "engaging"],
    submitted_at: ISODate("2022-11-29T16:45:00Z")
    // Step 63: intentionally omits attachments field
  },
  {
    student_id: 3, course_code: "EC101", semester: "2021-ODD", rating: 3,
    comments: "Average, could use more practical examples.",
    tags: ["needs-improvement"],
    submitted_at: ISODate("2021-11-20T10:00:00Z"),
    attachments: []
  },
  {
    student_id: 6, course_code: "EC101", semester: "2021-EVEN", rating: 1,
    comments: "Very difficult to follow, disorganised.",
    tags: ["unclear", "disorganised"],
    submitted_at: ISODate("2021-05-10T08:00:00Z"),
    attachments: []
  },
  {
    student_id: 2, course_code: "CS103", semester: "2022-ODD", rating: 5,
    comments: "Loved the hands-on projects.",
    tags: ["engaging", "good-examples", "well-structured"],
    submitted_at: ISODate("2022-12-02T13:20:00Z"),
    attachments: [{ filename: "project_final.zip", size_kb: 4096 }]
  },
  {
    student_id: 8, course_code: "CS103", semester: "2022-ODD", rating: 4,
    comments: "Challenging but rewarding.",
    tags: ["challenging", "engaging"],
    submitted_at: ISODate("2022-12-02T15:00:00Z"),
    attachments: [{ filename: "notes.pdf", size_kb: 180 }]
  },
  {
    student_id: 7, course_code: "ME101", semester: "2021-EVEN", rating: 3,
    comments: "Decent, but the pace was inconsistent.",
    tags: ["inconsistent"],
    submitted_at: ISODate("2021-05-15T09:00:00Z"),
    attachments: []
  }
]);

// Step 64: verify insert count
db.feedback.countDocuments();


// =====================================================================
// Task 2: CRUD Operations (Steps 65-70)
// =====================================================================

// Step 65: READ - all feedback with rating 5
db.feedback.find({ rating: 5 });

// Step 66: READ - CS101 feedback where tags contains 'challenging'
db.feedback.find({ course_code: "CS101", tags: "challenging" });
// (a simple value match against an array field checks membership directly -
// $elemMatch is only needed when matching multiple conditions on the same
// array element, e.g. sub-documents with several fields)

// Step 67: READ - projection: only student_id, course_code, rating, exclude _id
db.feedback.find({}, { student_id: 1, course_code: 1, rating: 1, _id: 0 });

// Step 68: UPDATE - add needs_review: true where rating < 3
db.feedback.updateMany(
  { rating: { $lt: 3 } },
  { $set: { needs_review: true } }
);

// Step 69: UPDATE - push 'reviewed' tag where needs_review is true
db.feedback.updateMany(
  { needs_review: true },
  { $push: { tags: "reviewed" } }
);

// Step 70: DELETE - remove feedback from semester '2021-EVEN'
db.feedback.deleteMany({ semester: "2021-EVEN" });


// =====================================================================
// Task 3: Aggregation Pipeline (Steps 71-74)
// =====================================================================

// Step 71 + 72: average rating & count per course for 2022-ODD,
// sorted descending, with a renamed/rounded field
db.feedback.aggregate([
  { $match: { semester: "2022-ODD" } },
  {
    $group: {
      _id: "$course_code",
      avg_rating: { $avg: "$rating" },
      total_feedback: { $sum: 1 }
    }
  },
  {
    $project: {
      _id: 0,
      course_code: "$_id",
      average_rating: { $round: ["$avg_rating", 1] },
      total_feedback: 1
    }
  },
  { $sort: { average_rating: -1 } }
]);

// Step 73: tag frequency leaderboard using $unwind
db.feedback.aggregate([
  { $unwind: "$tags" },
  { $group: { _id: "$tags", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
]);

// Step 74: index on course_code + verify usage
db.feedback.createIndex({ course_code: 1 });

db.feedback.find({ course_code: "CS101" }).explain("executionStats");
// Confirm the "executionStages.stage" (or nested inputStage) shows IXSCAN,
// not COLLSCAN, once the index above has been created.
