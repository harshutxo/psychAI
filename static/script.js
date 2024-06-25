document.getElementById('chat-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const messageInput = document.getElementById('message');
    const message = messageInput.value;

    if (message.trim() === '') return;

    const chatbox = document.getElementById('chatbox');
    const userMessage = document.createElement('div');
    userMessage.classList.add('user-message');
    userMessage.textContent = message;
    chatbox.appendChild(userMessage);

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `message=${message}`
    })
    .then(response => response.json())
    .then(data => {
        const botMessage = document.createElement('div');
        botMessage.classList.add('bot-message');
        botMessage.textContent = data.response;
        chatbox.appendChild(botMessage);
        chatbox.scrollTop = chatbox.scrollHeight;
    });

    messageInput.value = '';
});

window.addEventListener('resize', function() {
    // Adjust layout here based on window size
    // For example, you can change the number of chat messages displayed or resize elements
});
