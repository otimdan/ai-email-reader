document.getElementById("send-btn").addEventListener("click", handleAISearch);
document.getElementById("ai-input").addEventListener("keypress", (e) => {
  if (e.key === "Enter") handleAISearch();
});

async function handleAISearch() {
  const inputField = document.getElementById("ai-input");
  const status = document.getElementById("status-message");
  const emailList = document.getElementById("email-list");
  const message = inputField.value.trim();

  if (!message) return;

  // UI State: Loading
  status.innerText = "AI is scanning your inbox...";
  emailList.innerHTML = "";
  inputField.value = "";

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message }),
    });

    const data = await response.json();

    if (data.emails && data.emails.length > 0) {
      status.innerText = `Found ${data.total_results} results for: "${data.query_used}"`;
      renderEmails(data.emails);
    } else {
      status.innerText = data.response || "No emails found for that request.";
    }
  } catch (error) {
    status.innerText = "Error connecting to AI agent.";
    console.error(error);
  }
}

function renderEmails(emails) {
  const emailList = document.getElementById("email-list");
  emailList.innerHTML = emails
    .map(
      (email) => `
        <div class="email-card ${email.unread ? "unread" : ""}">
            <div class="email-header">
                <span class="sender">${escapeHtml(email.sender)}</span>
                <span class="date">${email.date}</span>
            </div>
            <div class="subject">${escapeHtml(email.subject)}</div>
            <div class="snippet">${escapeHtml(email.snippet)}</div>
        </div>
    `,
    )
    .join("");
}

// Security: Prevent XSS from email content
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}
