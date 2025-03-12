document.addEventListener("DOMContentLoaded", function () {
    function fetchMessages() {
        fetch("/messages/")  // Updated URL
            .then((response) => response.json())
            .then((messages) => {
                const chatBox = document.getElementById("chat-box");
                chatBox.innerHTML = "";
                messages.forEach((msg) => {
                    chatBox.innerHTML += `<p><strong>${msg.user__username}:</strong> ${msg.content} <small>${msg.timestamp}</small></p>`;
                });
            })
            .catch((error) => console.error("Error fetching messages:", error));
    }

    document.getElementById("send-btn").addEventListener("click", function () {
        const username = document.getElementById("username").value.trim();
        const content = document.getElementById("message").value.trim();

        if (!username || !content) return;

        fetch("/send/", {  // Updated URL
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({ username, content }),
        })
            .then(() => {
                document.getElementById("message").value = "";
                fetchMessages();
            })
            .catch((error) => console.error("Error sending message:", error));
    });

    setInterval(fetchMessages, 3000); // Auto-refresh chat every 3 sec
});
