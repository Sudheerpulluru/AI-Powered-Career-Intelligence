console.log("🔥 Chatbot JS loaded");

document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("chatbot-toggle");
  const box = document.getElementById("chatbot-box");
  const input = document.getElementById("chatbot-input");
  const send = document.getElementById("chatbot-send");
  const messages = document.getElementById("chatbot-messages");

  if (!toggle || !box) {
    console.error("❌ Chatbot elements not found");
    return;
  }

  // 🔥 FLOATING ICON CLICK FIX
  toggle.addEventListener("click", () => {
    box.classList.toggle("open");
    console.log("🤖 Floating icon clicked");
  });

  send.addEventListener("click", sendMessage);

  input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });

  function addMessage(text, cls) {
    const div = document.createElement("div");
    div.className = "msg " + cls;
    div.innerText = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  function sendMessage() {
    const msg = input.value.trim();
    if (!msg) return;

    addMessage(msg, "user");
    input.value = "";

    fetch("/chatbot", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg })
    })
    .then(res => res.json())
    .then(data => addMessage(data.reply, "bot"))
    .catch(() => addMessage("⚠️ Server error", "bot"));
  }
});
