// Get the chat log and form elements
const chatLog = document.getElementById('chatbox');
const chatForm = document.querySelector('form');
const userInput = document.getElementById('userInput');
const clearChatButton = document.getElementById('clearChat');

// Add event listener to the form
chatForm.addEventListener("submit", function (event) {
    event.preventDefault();

    // Get user input
    const userMessage = userInput.value.trim();
    if (userMessage === "") return;

    // Display user message
    const userMessageHTML = `<div class="message user-message"><strong>You:</strong> ${userMessage}</div>`;
    chatLog.innerHTML += userMessageHTML;
    userInput.value = "";

    // Fetch the response from the backend
    fetch("/get_response", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ user_input: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        // Display chatbot response
        const botResponseHTML = `<div class="message bot-message"><strong>Chatty:</strong> ${data.response}</div>`;
        chatLog.innerHTML += botResponseHTML;
    });
});

// Add event listener to the clear chat button
clearChatButton.addEventListener('click', () => {
    // Clear the chat log
    chatLog.innerHTML = '';
});