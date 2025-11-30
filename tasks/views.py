from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import date
from .scoring import calculate_task_score

@csrf_exempt
def analyze_tasks(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)

        # If frontend sends {tasks: [...], strategy: "smart"}
        if isinstance(data, dict):
            tasks = data.get("tasks", [])
            strategy = data.get("strategy", "smart")
        else:
            tasks = data
            strategy = "smart"

        if not isinstance(tasks, list):
            return JsonResponse({"error": "JSON must be a list"}, status=400)
        
        required_fields = ["title", "due_date"]
        errors = []

        for index, task in enumerate(tasks):
            missing = [field for field in required_fields if field not in task]

            if missing:
                errors.append(f"Task {index+1} is missing required fields: {', '.join(missing)}")

        if errors:
            return JsonResponse({"error": errors}, status=400)
        
        #Default values for optional fields
        for task in tasks:
            task["importance"]=task.get("importance", 5)
            task["estimated_hours"]=task.get("estimated_hours", 1)
            task["dependencies"]=task.get("dependencies", [])

        # Calculate scores first
        for task in tasks:
            task["score"] = calculate_task_score(task)

        # Apply strategy
        if strategy == "fastest":
            # Low effort first
            tasks.sort(key=lambda x: x.get("estimated_hours", 999))

        elif strategy == "impact":
            # High importance first
            tasks.sort(key=lambda x: x.get("importance", 0), reverse=True)

        elif strategy == "deadline":
            # Nearest deadline first
            tasks.sort(key=lambda x: x.get("due_date", "9999-12-31"))

        else:
            # Smart Balance (default) → Sort by score
            tasks.sort(key=lambda x: x["score"], reverse=True)

        return JsonResponse(tasks, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
def suggest_tasks(request):
    try:
        data = json.loads(request.body)

        if not isinstance(data, list):
            return JsonResponse({"error": "JSON must be a list of tasks"}, status=400)

        today = date.today()

        required_fields = ["title", "due_date"]
        errors = []

        for index, task in enumerate(data):
            missing = [field for field in required_fields if field not in task]

            if missing:
                errors.append(f"Task {index+1} is missing fields: {', '.join(missing)}")

        if errors:
            return JsonResponse({"error": errors}, status=400)
        
        #Default values for optional fields
        for task in data:
            task["importance"]=task.get("importance", 5)
            task["estimated_hours"]=task.get("estimated_hours", 1)
            task["dependencies"]=task.get("dependencies", [])

        # Add score
        for task in data:
            task["score"] = calculate_task_score(task)

        # Tasks due today or tomorrow
        urgent_tasks = []
        for t in data:
            due = date.fromisoformat(t["due_date"])
            days_left = (due - today).days
            if days_left <= 1:
                urgent_tasks.append(t)

        # If no urgent tasks → pick highest-scoring ones
        if len(urgent_tasks) == 0:
            urgent_tasks = data

        # Sort by score descending
        urgent_tasks.sort(key=lambda x: x["score"], reverse=True)

        # Pick top 3
        top_three = urgent_tasks[:3]

        # Human-friendly explanation
        explanation = (
            "These tasks are suggested for today based on urgency "
            "and overall task score."
        )

        return JsonResponse({
            "tasks": top_three,
            "explanation": explanation
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)