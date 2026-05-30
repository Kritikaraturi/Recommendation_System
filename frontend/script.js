// ===============================
// 🔹 GET STARTED BUTTON FUNCTION
// ===============================
function startQuiz() {
    window.location.href = "quiz.html";
}

// ===============================
// 🔹 SUBMIT QUIZ FUNCTION
// ===============================
function submitQuiz() {

    let answers = [];

    // 25 questions loop
    for (let i = 1; i <= 25; i++) {
        let selected = document.querySelector(`input[name="q${i}"]:checked`);

        if (!selected) {
            alert("Please answer all questions!");
            return;
        }

        answers.push(parseInt(selected.value));
    }

    // category divide
    const data = {
        interest: answers.slice(0, 5),
        skills: answers.slice(5, 10),
        aptitude: answers.slice(10, 15),
        personality: answers.slice(15, 20),
        work: answers.slice(20, 25)
    };

    console.log("Sending Data:", data);

    // ===============================
    // 🔹 BACKEND API CALL
    // ===============================
    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Server error");
        }
        return response.json();
    })
    .then(result => {
        console.log("Received from backend:", result);

        // ===============================
        // 🔹 SAVE DATA
        // ===============================
        localStorage.setItem("careerResults", JSON.stringify(result));

        // ===============================
        // 🔹 REDIRECT TO RESULT PAGE
        // ===============================
        window.location.href = "result.html";
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Backend not working! Check Flask server.");
    });
}


// ===============================
// 🔹 BACK TO HOME BUTTON (RESULT PAGE)
// ===============================
function goHome() {
    window.location.href = "index.html";
}