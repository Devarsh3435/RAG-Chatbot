function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value;

    if (message.trim() === "") return;

    appendMessage("You", message);
    input.value = "";

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    })
    .then(res => res.json())
    .then(data => {
        appendMessage("Bot", data.response);
    });
}

function appendMessage(sender, message) {
    const chatBox = document.getElementById("chat-box");
    const msgDiv = document.createElement("div");
    msgDiv.className = sender === "You" ? "user-msg" : "bot-msg";
    msgDiv.innerText = sender + ": " + message;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: "smooth" });
    chatBox.scrollTop = chatBox.scrollHeight;
}

document.getElementById("user-input").addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});
