# Testing

### POST /auth-token/
Get an auth token for user

### DELETE /auth-token/
Delete that auth token from database, equivalent to purging a session cookie


### PATCH /api/users/:username/

- Change a user's instrument/external_id/grade
- Requesting user must be a Teacher in any class that `:username` is a Student in


### POST /api/users/bulk_create_teachers/

- For admin users only (aka users with staff=True)
- POST a newline separated list of email addresses
- Creates/sends invitations to each and these users will have Teacher group assigned when they complete signup

## GET /api/enrollments/

- All of the current user’s enrollments, regardless of role.

### POST /api/enrollments/:id/

- Add an Enrollment to a course
- The user that makes this request must be a teacher of the course


### PATCH /api/enrollments/:id/

Change user’s default instrument
Params: instrument=<instrument_id>

```
curl -v \
--request PATCH \
-H 'Authorization: Token 2b2981292f56822c1bd30d494ac7f77ec0d5171d' \
-d "instrument=20" \
https://dev-api.tele.band/api/enrollments/2/ | jq '.'
```

### DELETE /api/enrollments/:id

Remove a user/role/course enrollment


### GET /api/pieces/

- Get all the pieces in the database

```
curl -v \
--request GET \
--header 'Content-Type: application/json' \
-H 'Authorization: Token e9a82a7c334fbdfc52f502efebebec474708eef0' \
https://dev-api.tele.band/api/pieces/ && echo "\n"


```

### POST /api/courses/

- Params: name, start_date, end_date, slug
- Make a course
- Only for users with Teacher in django groups

```bash
curl -v \
--request POST \
-H 'Authorization: Token e9a82a7c334fbdfc52f502efebebec474708eef0' \
-d "name=7th Grade Band" \
-d "start_date=2022-01-01" \
-d "end_date=2022-06-01" \
-d "slug=nonsense" \
https://dev-api.tele.band/api/courses/ | jq '.'
```

### GET /api/courses/:slug/assignments

For student: get all assignments assigned to me for this course
For teacher: get every assignment for every enrollment in this course (probably you want to get activities instead) -->

```
curl -v \
--request GET \
--header 'Content-Type: application/json' \
-H 'Authorization: Token d0c5a7bf9508026cab574bf149785caa52bb069b' \
http://localhost:8000/api/courses/6th-grade-band/assignments/ && echo "\n"

### PATCH /api/courses/:slug/assignment/:id/

Teacher only: change instrument

<!-- GET /api/courses/:slug/activities
Teacher only: list of all activities that any student has had (this doesn’t make much sense after the model simplification
Example:
[
    {
        "activity_type": "Melody",
        "part_type": "Melody",
        "body": "Do it"
    }
]-->

### GET /api/courses/:slug/roster/

- Teacher only: get all enrollments for this course 

### POST /api/courses/:slug/roster/

- Create Users if needed and Enrollments of those Users to this Course
- POST a CSV file (param name `file`) with format fullname,username,password,grade
- If user with that username exists and password matches, will use existing user
- Otherwise user will be created, unless username with different password exists, these are returned as `invalid`
- If existing Enrollments exist they will be returned


```
{
  "users": {
    "existing": [
      {
        "username": "bobby",
        "name": "Bobby Bones",
        "url": "http://localhost:8000/api/users/bobby/"
      }
    ],
    "created": [
      {
        "username": "sally",
        "name": "Sally Sue",
        "url": "http://localhost:8000/api/users/sally/"
      }
    ],
    "invalid": [
      {
        "name": "Vanessa Banessa",
        "username": "vsauce",
        "password": "123456",
        "grade": "6th grade",
        "reason": "Wrong password"
      }
    ]
  },
  "enrollments": {
    "existing": [],
    "created": [
      {
        "id": 22,
        "course": {
          "id": 8,
          "name": "From FE",
          "start_date": "2022-01-01",
          "end_date": "2022-06-01",
          "url": "http://localhost:8000/api/courses/from-fe/",
          "slug": "from-fe",
          "owner": {
            "username": "admin",
            "name": "",
            "url": "http://localhost:8000/api/users/admin/"
          }
        },
        "instrument": null,
        "role": "Student"
      },
      {
        "id": 23,
        "course": {
          "id": 8,
          "name": "From FE",
          "start_date": "2022-01-01",
          "end_date": "2022-06-01",
          "url": "http://localhost:8000/api/courses/from-fe/",
          "slug": "from-fe",
          "owner": {
            "username": "admin",
            "name": "",
            "url": "http://localhost:8000/api/users/admin/"
          }
        },
        "instrument": null,
        "role": "Student"
      }
    ]
  }
}
```

### POST /api/courses/:slug/assign

- Params: piece_id
- Creates one Assignment per person per Activity in database

curl -v \
--request POST \
--header 'Content-Type: application/json' \
-H 'Authorization: Token e9a82a7c334fbdfc52f502efebebec474708eef0' \
-d '{"piece_id":"1"}' \
https://dev-api.tele.band/api/courses/6th-grade-band/assign/ && echo "\n"

- error bc it's the student

curl -v \
--request POST \
--header 'Content-Type: application/json' \
-H 'Authorization: Token 2b2981292f56822c1bd30d494ac7f77ec0d5171d' \
-d "piece_id=1" \
https://dev-api.tele.band/api/courses/6th-grade-band/assign/ && echo "\n"

- (now with a teacher):

```json
[{"activity":{"activity_type":"Melody","part_type":"Melody","body":"Practice the melody and then record yourself performing it."},"deadline":null,"instrument":{"name":"Trombone","transposition":"Concert Pitch BC"},"part":{"name":"Air for Band Melody","piece":{"id":1,"name":"Air for Band","composer":null,"video":"","audio":"","date_composed":null,"ensemble_type":1}},"id":1},{"activity":{"activity_type":"Melody","part_type":"Melody","body":"Practice the melody and then record yourself performing it."},"deadline":null,"instrument":{"name":"Trombone","transposition":"Concert Pitch BC"},"part":{"name":"Air for Band Melody","piece":{"id":1,"name":"Air for Band","composer":null,"video":"","audio":"","date_composed":null,"ensemble_type":1}},"id":2},{"activity":{"activity_type":"Bassline","part_type":"Bassline","body":"Practice the bassline and then record yourself performing it."},"deadline":null,"instrument":{"name":"Trombone","transposition":"Concert Pitch BC"},"part":{"name":"Air for Band Bassline","piece":{"id":1,"name":"Air for Band","composer":null,"video":"","audio":"","date_composed":null,"ensemble_type":1}},"id":3},{"activity":{"activity_type":"Bassline","part_type":"Bassline","body":"Practice the bassline and then record yourself performing it."},"deadline":null,"instrument":{"name":"Trombone","transposition":"Concert Pitch BC"},"part":{"name":"Air for Band Bassline","piece":{"id":1,"name":"Air for Band","composer":null,"video":"","audio":"","date_composed":null,"ensemble_type":1}},"id":4}]
```

- If there are students in the course that do not have an instrument on their Enrollment or their User this endpoint will return 400 with the following

```json
{
  "message": "Some users and their enrollments have no instrument",
  "enrollments": [
    {
      "id": 22,
      "course": {
        "id": 8,
        "name": "From FE",
        "start_date": "2022-01-01",
        "end_date": "2022-06-01",
        "url": "http://localhost:8000/api/courses/from-fe/",
        "slug": "from-fe",
        "owner": {
          "id": 1,
          "username": "admin",
          "name": "",
          "url": "http://localhost:8000/api/users/admin/",
          "grade": "",
          "instrument": null,
          "external_id": ""
        }
      },
      "instrument": null,
      "role": "Student"
    },
    {
      "id": 23,
      "course": {
        "id": 8,
        "name": "From FE",
        "start_date": "2022-01-01",
        "end_date": "2022-06-01",
        "url": "http://localhost:8000/api/courses/from-fe/",
        "slug": "from-fe",
        "owner": {
          "id": 1,
          "username": "admin",
          "name": "",
          "url": "http://localhost:8000/api/users/admin/",
          "grade": "",
          "instrument": null,
          "external_id": ""
        }
      },
      "instrument": null,
      "role": "Student"
    }
  ]
}
```

### POST /api/courses/:slug/unassign

- Params: piece_id
- Removes every Assignment for this piece assigned to anyone in this class
- Returns 400 if piece_id is missing
- Returns 404 if no such piece_id
- Returns 400 if any submissions have already been made to this assignment
- Returns 200 with empty body on success


### GET /api/courses/:slug/assignments/:id/notation

- Both: gets the PartTranscription for this assignment
  curl -v \
  --request GET \
  --header 'Content-Type: application/json' \
  -H 'Authorization: Token e9a82a7c334fbdfc52f502efebebec474708eef0' \
  https://dev-api.tele.band/api/courses/6th-grade-band/assignments/3/notation/ && echo "\n"

curl -v \
--request GET \
--header 'Content-Type: application/json' \
-H 'Authorization: Token e9a82a7c334fbdfc52f502efebebec474708eef0' \
https://dev-api.tele.band/api/courses/6th-grade-band/assignments/ && echo "\n"

## GET/POST /api/courses/:slug/assignments/:id/submissions

- Student: list my submissions to this assignment or make a new one
- Teacher: can do the same (could forbid POSTing will leave for now)

curl -v \
--request POST \
-H 'Authorization: Token e9a82a7c334fbdfc52f502efebebec474708eef0' \
-d "content='hello, here is my content'" \
https://dev-api.tele.band/api/courses/6th-grade-band/assignments/3/submissions/ && echo "\n"

curl -v \
--request GET \
-H 'Authorization: Token 70c0fbdb510234c9c94bd29641a3ba95752dcfea' \
https://localhost:8000/api/courses/6th-grade-band/assignments/4/submissions/ && echo "\n"

### GET/POST /api/courses/:slug/assignments/:id/submissions/:id/attachments/

- Student: list attachments to this submission or create one
- Teacher: same

curl -v \
--request POST \
-H 'Authorization: Token e9a82a7c334fbdfc52f502efebebec474708eef0' \
-F 'file=@/Users/tgm/Downloads/Music CPR/Jubilo - Melody/Jubilo - Melody - Bb.musicxml.xml' \
https://dev-api.tele.band/api/courses/6th-grade-band/assignments/3/submissions/1/attachments/ && echo "\n"

# To add a new Piece

Send a POST to /api/pieces with body like this:

```json
{
  "name": "Air for Band",
  "ensemble_type": "Band",
  "parts": [
    {
      "name": "Air for Band Melody",
      "part_type": "Melody",
      "transpositions": [
        {
          "transposition": "Bb",
          "flatio": ""
        },
        {
          "transposition": "Concert Pitch BC 8vb",
          "flatio": ""
        },
        {
          "transposition": "Concert Pitch BC",
          "flatio": ""
        },
        {
          "transposition": "Concert Pitch TC 8va",
          "flatio": ""
        },
        {
          "transposition": "Concert Pitch TC",
          "flatio": ""
        },
        {
          "transposition": "Eb",
          "flatio": ""
        },
        {
          "transposition": "F",
          "flatio": ""
        }
      ]
    },
    {
      "name": "Air for Band Bassline",
      "part_type": "Bassline",
      "transpositions": [
        {
          "transposition": "Bb",
          "flatio": ""
        },
        {
          "transposition": "Concert Pitch BC 8vb",
          "flatio": ""
        },
        {
          "transposition": "Concert Pitch BC",
          "flatio": ""
        },
        {
          "transposition": "Concert Pitch TC 8va",
          "flatio": ""
        },
        {
          "transposition": "Concert Pitch TC",
          "flatio": ""
        },
        {
          "transposition": "Eb",
          "flatio": ""
        },
        {
          "transposition": "F",
          "flatio": ""
        }
      ]
    }
  ]
}
```

## GET all students in this course's most recent submissions for an "assignment" (piece x activity)
* `http://localhost:8000/api/courses/6th-grade-band/submissions/recent/?piece_id=1&activity_id=1`

## Grade assignment submission

```bash
curl -v \
--request POST \
-H 'Authorization: Token d0c5a7bf9508026cab574bf149785caa52bb069b' \
-d "submission=5" \
-d "rhythm=1" \
-d "tone=2" \
-d "expression=5" \
-d "grader=27" \
http://localhost:8000/api/courses/6th-grade-band/grades/ | jq '.'
```
## update course name or start/end `PATCH /api/courses/:slug/
curl -v \
--request PATCH \
-H 'Authorization: Token d0c5a7bf9508026cab574bf149785caa52bb069b' \
-d "slug=testing-newb-course" \
http://localhost:8000/api/courses/testing-new-course/ | jq '.'

curl -v \
-H 'Authorization: Token 13e8379f4bfb235e218b1452df97fc315707d8f0' \
http://localhost:8000/api/courses/really-no-instruments/grades/