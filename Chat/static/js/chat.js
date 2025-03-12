document.addEventListener("DOMContentLoaded", function () {
    function fetchMessages() {
        fetch("/messages/")
            .then((response) => response.json())
            .then((messages) => {
                const chatBox = document.getElementById("chat-box");
                chatBox.innerHTML = "";
                messages.forEach((msg) => {
                    const formattedTimestamp = new Date(msg.timestamp).toLocaleString();  // Format timestamp

                    chatBox.innerHTML += `
                        <div class="message">
                            <p><strong class="username">${msg.user__username}</strong>: ${msg.content}</p>
                            <small class="timestamp">${formattedTimestamp}</small>
                        </div>
                    `;
                });
            })
            .catch((error) => console.error("Error fetching messages:", error));
    }

    document.getElementById("send-btn").addEventListener("click", function () {
        const username = document.getElementById("username").value.trim();
        const content = document.getElementById("message").value.trim();
        const room = "defaultRoom";  // Assuming you're using a static room for now

        if (!username || !content) return;

        // Send the data as JSON instead of URLSearchParams
        fetch("/send/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",  // Set content type as JSON
            },
            body: JSON.stringify({ username, content, room }),  // Send data as JSON
        })
            .then(() => {
                document.getElementById("message").value = "";
                fetchMessages();
            })
            .catch((error) => console.error("Error sending message:", error));
    });

    setInterval(fetchMessages, 3000); // Auto-refresh chat every 3 sec
});
