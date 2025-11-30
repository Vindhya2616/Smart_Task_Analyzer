document.getElementById("analyzeBtn").addEventListener("click", analyzeTasks);
document.getElementById("suggestBtn").addEventListener("click", suggestTasks);

// Analyze button
async function analyzeTasks() {
    try {
        const rawText = document.getElementById("taskInput").value.trim();
        const tasks = JSON.parse(rawText);

        const strategy = document.getElementById("strategy").value;

        const response = await fetch("http://127.0.0.1:8000/api/tasks/analyze/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ tasks: tasks, strategy: strategy })
        });

        const data = await response.json();
        displayResults(data);

    } catch (error) {
        console.error("Error:", error);
        alert("Invalid JSON or server error.");
    }
}

// Suggest button
async function suggestTasks() {
    try {
        const rawText = document.getElementById("taskInput").value.trim();
        const tasks = JSON.parse(rawText);

        const response = await fetch("http://127.0.0.1:8000/api/tasks/suggest/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(tasks)
        });

        const data = await response.json();
        displayResults(data);

    } catch (error) {
        console.error("Error:", error);
        alert("Invalid JSON or server error.");
    }
}


// Display Results
function displayResults(data) {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = ""; 

    // ❗ 1. Check if backend returned an error
    if (data.error) {
        const errBox = document.createElement("div");
        errBox.className = "error-box";

        // If error is an array (multiple tasks missing fields)
        if (Array.isArray(data.error)) {
            errBox.innerHTML = "<strong>Errors:</strong><br>" + data.error.join("<br>");
        }
        else {
            errBox.innerHTML = "<strong>Error:</strong> " + data.error;
        }

        resultsDiv.appendChild(errBox);
        return; // STOP → don't try to loop tasks
    }

    // ❗ 2. Explanation (from /suggest/)
    if (data.explanation) {
        const exp = document.createElement("p");
        exp.innerHTML = "<strong>" + data.explanation + "</strong>";
        resultsDiv.appendChild(exp);
    }

    // ❗ 3. Tasks list (works for analyze + suggest)
    const tasks = data.tasks || data;

    if (!Array.isArray(tasks)) {
        resultsDiv.innerHTML = "<p>Unexpected response from server.</p>";
        return;
    }

    // ❗ 4. Display tasks
    tasks.forEach(task => {
        const card = document.createElement("div");
        card.className = "task-card";

        let tag = task.score >= 80 ? "HIGH" :
                  task.score >= 50 ? "MEDIUM" : "LOW";

        card.innerHTML = `
            <h3>${task.title}</h3>
            <p><strong>Due:</strong> ${task.due_date}</p>
            <p><strong>Hours:</strong> ${task.estimated_hours}</p>
            <p><strong>Importance:</strong> ${task.importance}</p>
            <p><strong>Score:</strong> ${task.score}</p>
            <span class="priority-tag ${tag.toLowerCase()}">${tag}</span>
        `;

        resultsDiv.appendChild(card);
    });
}
