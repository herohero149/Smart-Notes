document.getElementById('noteForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const submitBtn = this.querySelector('button[type="submit"]');
    const submitText = submitBtn.querySelector('.submit-text');
    const loading = submitBtn.querySelector('.loading');
    
    // Show loading state
    submitText.style.display = 'none';
    loading.style.display = 'inline-block';
    submitBtn.disabled = true;
    
    const formData = new FormData();
    formData.append('title', document.getElementById('title').value);
    formData.append('content', document.getElementById('content').value);
    
    try {
        const response = await fetch('/add_note', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        
        if (data.success) {
            location.reload();
        } else {
            showToast('Error adding note: ' + data.message, 'error');
        }
    } catch (error) {
        showToast('Error adding note: ' + error, 'error');
    } finally {
        // Reset button state
        submitText.style.display = 'inline';
        loading.style.display = 'none';
        submitBtn.disabled = false;
    }
});

async function generateQuiz(noteId) {
    const quizContainer = document.getElementById(`quiz-${noteId}`);
    quizContainer.innerHTML = `
        <div class="text-center">
            <div class="loading"></div>
            <p class="mt-2">Generating quiz...</p>
        </div>
    `;
    
    try {
        const response = await fetch(`/generate_quiz/${noteId}`);
        const questions = await response.json();
        
        let quizHTML = '<div class="quiz-container">';
        questions.forEach((q, index) => {
            const encodedAnswer = encodeURIComponent(q.answer);
            quizHTML += `
                <div class="quiz-question">
                    <p><strong>Question ${index + 1}:</strong></p>
                    <p class="mb-3">${q.question}</p>
                    <p class="text-muted small">Original context: "${q.context}"</p>
                    <button class="btn btn-outline-primary btn-sm" 
                            onclick="showAnswer(this, '${encodedAnswer}')">
                        Reveal Answer
                    </button>
                    <div class="answer-reveal mt-3" style="display: none;">
                        <strong>Answer:</strong> ${q.answer}
                    </div>
                </div>
            `;
        });
        quizHTML += '</div>';
        quizContainer.innerHTML = quizHTML;
    } catch (error) {
        showToast('Error generating quiz', 'error');
        quizContainer.innerHTML = '';
    }
}

function showAnswer(button, answer) {
    const decodedAnswer = decodeURIComponent(answer);
    const answerElement = button.nextElementSibling;
    answerElement.style.display = 'block';
    setTimeout(() => answerElement.classList.add('show'), 50);
    button.style.display = 'none';
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => toast.classList.add('show'), 100);
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

async function summarizeNote(noteId) {
    const summaryContainer = document.getElementById(`summary-${noteId}`);
    summaryContainer.innerHTML = `
        <div class="text-center">
            <div class="loading"></div>
            <p class="mt-2">Analyzing and summarizing...</p>
        </div>
    `;
    
    try {
        const response = await fetch(`/summarize/${noteId}`);
        const data = await response.json();
        
        if (data.success) {
            summaryContainer.innerHTML = `
                <div class="summary-text">
                    <strong>AI-Generated Summary:</strong>
                    <p class="mt-2">${data.summary}</p>
                </div>
            `;
        } else {
            showToast('Error generating summary', 'error');
            summaryContainer.innerHTML = '';
        }
    } catch (error) {
        showToast('Error generating summary', 'error');
        summaryContainer.innerHTML = '';
    }
}

// Add styles for toast notifications
const style = document.createElement('style');
style.textContent = `
    .toast-notification {
        position: fixed;
        bottom: 20px;
        right: 20px;
        padding: 12px 24px;
        background: var(--primary-color);
        color: white;
        border-radius: 8px;
        opacity: 0;
        transform: translateY(20px);
        transition: all 0.3s ease;
        z-index: 1000;
    }
    
    .toast-notification.show {
        opacity: 1;
        transform: translateY(0);
    }
    
    .toast-error {
        background: #e74c3c;
    }
`;
document.head.appendChild(style);