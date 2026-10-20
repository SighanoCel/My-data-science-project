// "Ask to Celestin" — chat assistant at the bottom right of the portfolio.
// The answers come from the RAG API (api_celestin.py in the capstone_RAG_project
// repo): the OpenAI key stays server-side, this script is only the chat UI.
(function () {
    // URL of the deployed chat API — replace after deploying (no trailing slash).
    // When the portfolio is opened locally, use the API running on this machine.
    const IS_LOCAL = ["localhost", "127.0.0.1"].includes(location.hostname);
    const CELESTIN_API_URL = IS_LOCAL ? "http://127.0.0.1:8000" : "https://ask-celestin.onrender.com";

    const GREETING =
        "Hello, I'm **Celestin** 👋\nAsk me anything about this portfolio: projects, models, skills, education…";
    const SUGGESTIONS = [
        "Which models were trained in the portfolio?",
        "Tell me about the fraud detection project",
        "Where did Celestin study?",
    ];

    // Keep the conversation while the tab is open (session memory lives in the API).
    const STORE_KEY = "celestin-chat";
    const saved = JSON.parse(sessionStorage.getItem(STORE_KEY) || "null");
    const state = saved || {
        sessionId: (crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random().toString(16).slice(2)),
        messages: [],
    };
    const save = () => sessionStorage.setItem(STORE_KEY, JSON.stringify(state));

    // ---------------------------------------------------------------- DOM
    const launcher = document.createElement("button");
    launcher.className = "celestin-launcher";
    launcher.type = "button";
    launcher.setAttribute("aria-expanded", "false");
    launcher.setAttribute("aria-controls", "celestin-panel");
    launcher.innerHTML = '<i class="fas fa-comments"></i><span>Ask to Celestin</span>';

    const panel = document.createElement("div");
    panel.className = "celestin-panel";
    panel.id = "celestin-panel";
    panel.setAttribute("aria-label", "Ask to Celestin");
    panel.innerHTML =
        '<div class="celestin-header">' +
        '<div class="celestin-identity">' +
        '<span class="celestin-avatar"><i class="fas fa-robot"></i></span>' +
        "<div><strong>Celestin</strong><small>Portfolio assistant</small></div>" +
        "</div>" +
        '<div class="celestin-header-actions">' +
        '<button type="button" class="celestin-reset" title="New conversation"><i class="fas fa-rotate-right"></i></button>' +
        '<button type="button" class="celestin-close" title="Close"><i class="fas fa-xmark"></i></button>' +
        "</div></div>" +
        '<div class="celestin-messages" aria-live="polite"></div>' +
        '<div class="celestin-suggestions"></div>' +
        '<form class="celestin-form">' +
        '<textarea class="celestin-input" rows="1" maxlength="1000" placeholder="Ask to Celestin…" aria-label="Ask to Celestin"></textarea>' +
        '<button type="submit" class="celestin-send" title="Send"><i class="fas fa-paper-plane"></i></button>' +
        "</form>";

    document.body.appendChild(panel);
    document.body.appendChild(launcher);

    const list = panel.querySelector(".celestin-messages");
    const suggestions = panel.querySelector(".celestin-suggestions");
    const form = panel.querySelector(".celestin-form");
    const input = panel.querySelector(".celestin-input");
    const sendBtn = panel.querySelector(".celestin-send");

    // ---------------------------------------------------------------- rendering
    function escapeHtml(text) {
        return text.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
    }

    // Minimal, safe markdown: escape first, then bold / italics / code / lists / line breaks.
    function renderMarkdown(text) {
        const inline = (s) =>
            s
                .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
                .replace(/(^|[^*])\*([^*\n]+)\*/g, "$1<em>$2</em>")
                .replace(/`([^`]+)`/g, "<code>$1</code>");
        const lines = escapeHtml(text).split("\n");
        let html = "";
        let listType = null;
        for (const raw of lines) {
            const line = raw.trim();
            const ul = line.match(/^[-•*]\s+(.*)/);
            const ol = line.match(/^\d+[.)]\s+(.*)/);
            const type = ul ? "ul" : ol ? "ol" : null;
            if (type !== listType) {
                if (listType) html += `</${listType}>`;
                if (type) html += `<${type}>`;
                listType = type;
            }
            if (type) html += `<li>${inline((ul || ol)[1])}</li>`;
            else if (line) html += `<p>${inline(line)}</p>`;
        }
        if (listType) html += `</${listType}>`;
        return html;
    }

    function addBubble(role, text) {
        const bubble = document.createElement("div");
        bubble.className = `celestin-msg celestin-${role}`;
        bubble.innerHTML = role === "user" ? `<p>${escapeHtml(text)}</p>` : renderMarkdown(text);
        list.appendChild(bubble);
        list.scrollTop = list.scrollHeight;
        return bubble;
    }

    function renderAll() {
        list.innerHTML = "";
        addBubble("assistant", GREETING);
        state.messages.forEach((m) => addBubble(m.role, m.content));
        suggestions.innerHTML = "";
        if (state.messages.length === 0) {
            SUGGESTIONS.forEach((q) => {
                const chip = document.createElement("button");
                chip.type = "button";
                chip.textContent = q;
                chip.addEventListener("click", () => ask(q));
                suggestions.appendChild(chip);
            });
        }
    }

    // ---------------------------------------------------------------- chat
    let busy = false;

    async function ask(question) {
        question = question.trim();
        if (!question || busy) return;
        busy = true;
        sendBtn.disabled = true;
        suggestions.innerHTML = "";
        input.value = "";
        autosize();

        state.messages.push({ role: "user", content: question });
        save();
        addBubble("user", question);

        const typing = addBubble("assistant", "");
        typing.classList.add("celestin-typing");
        typing.innerHTML = "<span></span><span></span><span></span>";
        // The free server sleeps when idle: tell the visitor if the first answer is slow.
        const slowNotice = setTimeout(() => {
            typing.classList.remove("celestin-typing");
            typing.innerHTML = "<p><em>Celestin is waking up, this can take up to a minute…</em></p>";
        }, 8000);

        let answer;
        try {
            const res = await fetch(`${CELESTIN_API_URL}/chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question, session_id: state.sessionId }),
            });
            if (res.ok) {
                answer = (await res.json()).answer;
            } else {
                const detail = (await res.json().catch(() => ({}))).detail;
                answer = typeof detail === "string" ? `⚠️ ${detail}` : "⚠️ Sorry, something went wrong. Please try again.";
            }
        } catch (err) {
            answer = "⚠️ Celestin is unreachable right now. Please try again in a moment.";
        }

        clearTimeout(slowNotice);
        typing.remove();
        if (!answer.startsWith("⚠️")) {
            state.messages.push({ role: "assistant", content: answer });
            save();
        }
        addBubble("assistant", answer);
        busy = false;
        sendBtn.disabled = false;
        input.focus();
    }

    function autosize() {
        input.style.height = "auto";
        input.style.height = Math.min(input.scrollHeight, 120) + "px";
    }

    // ---------------------------------------------------------------- events
    function setOpen(open) {
        panel.classList.toggle("open", open);
        launcher.classList.toggle("hidden", open);
        launcher.setAttribute("aria-expanded", String(open));
        if (open) {
            list.scrollTop = list.scrollHeight;
            input.focus();
            // Wake the server up while the visitor types their first question.
            fetch(`${CELESTIN_API_URL}/health`).catch(() => {});
        } else {
            launcher.focus();
        }
    }

    launcher.addEventListener("click", () => setOpen(true));
    panel.querySelector(".celestin-close").addEventListener("click", () => setOpen(false));
    panel.querySelector(".celestin-reset").addEventListener("click", () => {
        if (busy) return;
        state.sessionId = crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random().toString(16).slice(2);
        state.messages = [];
        save();
        renderAll();
        input.focus();
    });
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        ask(input.value);
    });
    input.addEventListener("input", autosize);
    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            ask(input.value);
        }
    });
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && panel.classList.contains("open")) setOpen(false);
    });

    renderAll();
})();
