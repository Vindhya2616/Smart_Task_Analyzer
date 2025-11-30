# Smart_Task_Analyzer
The Smart Task Analyzer is a mini-application that intelligently analyzes and prioritizes tasks using a custom scoring algorithm based on urgency, importance, effort, and dependencies.
This project includes a Django backend and a clean, responsive HTML/CSS/JS frontend.

## 🚀 Features

✅ Task Priority Analyzer :

Accepts a list of tasks and returns them sorted based on a smart scoring algorithm.

✅ Suggestion Engine :

Suggests the top 3 tasks for today, based on urgency and score.

✅Sorting Strategies

Supports multiple strategies:
- Smart Balance (default)
- Fastest Wins
- High Impact
- Deadline Driven

✅ Error & Edge-Case Handling

- Detects missing required fields
- Auto-fills missing optional fields
- Handles overdue tasks
- Validates JSON input
- Supports dependencies (as integer IDs)

✅ Responsive Frontend :

Clean UI with two-panel layout - input on left, results on right.

## 🧠 How the Algorithm Works

The scoring logic lives inside tasks/scoring.py.

Each task receives a score based on four factors:

1️⃣ Urgency (Highest Weight)

If overdue -> +100  

If due in ≤ 3 days -> +50 

Else -> +0

#### ❓ Why urgency > effort?
In real work environments, missing deadlines causes bigger problems than spending more time on a task.
Therefore urgency must outweigh effort.

2️⃣ Importance (Medium Weight)

score += importance * 5

Importance gives tasks meaningful impact on final score.

3️⃣ Effort (Lowest Weight)

If estimated_hours < 2 → +10 (quick win bonus)

Reason:

Quick tasks should get a small boost, but should not outrank urgent or important tasks.

4️⃣ Dependencies (Optional)

Dependencies are stored as integer IDs such as [1, 2, 3].

This enables future expansion without complicating the algorithm.

Final Score = Urgency + Importance Weight + Quick-Win Bonus

Higher score = higher priority.

## 🧩 Design Decisions

1️⃣ Backend Framework: Django

- Django was chosen because:

- Fast to build JSON-based APIs

- Built-in development server

- Simple routing

- Auto JSON handling

2️⃣ No Database Storage

- Tasks are analyzed directly from input JSON.

- JSON input makes frontend integration simpler

Reason:
DB adds unnecessary complexity

3️⃣ Default Handling for Optional Fields

If user does not provide:

- importance -> default = 5

- estimated_hours -> default = 1

- dependencies -> default = []

Reason:

- Prevents crashes
- Makes backend more robust
- Mimics real-world systems that can handle imperfect input

4️⃣ Error Handling for Required Fields

Required fields:

- title
- due_date

Missing these returns a readable error.

This satisfies edge-case expectations.

5️⃣ Two-Panel Responsive UI

- Left panel: task input & strategy selection
- Right panel: results

Reason:
- Clean separation
- No scroll issues
- More professional UX design

6️⃣ Strategy-Based Sorting

Each strategy demonstrates different prioritization thinking:
- Urgency
- Effort
- Importance
- Score

This shows problem-solving ability.

## 📂 Project Structure

task-analyzer/
├── backend/
│   ├── settings.py
│   ├── urls.py
|   ├── asgi.py
|   ├── __init__.py
│   └── wsgi.py
├── tasks/
|   ├── migrations/
|   ├── __init__.py
|   ├── admin.py
|   ├── apps.py
│   ├── scoring.py
|   ├── tests.py
│   ├── views.py
│   ├── urls.py
│   └── models.py 
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── manage.py
├── db.sqlite3
└── requirements.txt

## 📦 Requirements

- Django==4.0.4
- django-cors-headers==4.9.0

## ⚙️ Installation & Setup

1️⃣ Clone the repository

- git clone https://github.com/<your-username>/<repo-name>.git

- cd task-analyzer

2️⃣ Create & activate virtual environment

Windows:

- python -m venv venv

- venv\Scripts\activate

macOS / Linux:

- python3 -m venv venv

- source venv/bin/activate

3️⃣ Install dependencies

pip install -r requirements.txt

4️⃣ Run migrations

python manage.py migrate

5️⃣ Start server

python manage.py runserver

Server runs on:
http://127.0.0.1:8000

## 🔌 API Endpoints

- POST /api/tasks/analyze/

Analyzes tasks and returns sorted priority order.

Input

{
 "tasks": [ ... ], 
  "strategy": "smart"
}

Output

[
  {
    "title": "...",
    "score": 75,
    "due_date": "...",
    ...
  } 
] 


POST /api/tasks/suggest/

Returns top 3 important tasks for today.

Input

[
  {
    "title": "...", 
    "due_date": "...",
    ...
  }
] 

Output

{
  "tasks": [...],
  "explanation": "These tasks are suggested for today..."  
} 

## 🖥️ Frontend Usage

1️⃣ Open frontend/index.html in your browser

2️⃣ Paste your JSON tasks into the left panel

3️⃣ Select a strategy

4️⃣ Click:
Analyze Tasks

or

Suggest Tasks for Today

5️⃣ Results appear on the right panel

## 🧪 Edge Case Handling

This project handles:
✔ Overdue tasks
✔ Missing optional fields (auto-filled)
✔ Missing required fields (error)
✔ Tasks due today / tomorrow
✔ Invalid JSON
✔ Integer-based dependencies







