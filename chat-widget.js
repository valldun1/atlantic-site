/* Atlantic Sail AI-chat widget. Клиент без секретов: все запросы идут на серверный прокси chat.sailor.bar */
(function () {
  if (window.__asChatLoaded) return;
  window.__asChatLoaded = true;

  var API = "https://chat.sailor.bar/api/chat";
  var HISTORY_KEY = "as_chat_history_v1";

  /* ---- стили ---- */
  var css = [
    "#as-chat-btn{position:fixed;right:20px;bottom:20px;width:60px;height:60px;border-radius:50%;background:#0B5963;color:#fff;border:none;cursor:pointer;font-size:26px;box-shadow:0 6px 20px rgba(11,89,99,.4);z-index:9998;display:flex;align-items:center;justify-content:center;transition:transform .2s}",
    "#as-chat-btn:hover{transform:scale(1.07)}",
    "#as-chat-box{position:fixed;right:20px;bottom:92px;width:360px;max-width:calc(100vw - 40px);height:480px;max-height:calc(100vh - 130px);background:#fff;border-radius:18px;box-shadow:0 14px 44px rgba(4,36,48,.28);z-index:9999;display:none;flex-direction:column;overflow:hidden;border:1px solid #e2edf0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}",
    "#as-chat-box.open{display:flex}",
    "#as-chat-head{background:linear-gradient(135deg,#0B5963,#0a3d4f);color:#fff;padding:14px 16px;display:flex;align-items:center;gap:10px;font-size:14px;font-weight:700}",
    "#as-chat-head .as-x{margin-left:auto;background:rgba(255,255,255,.15);border:none;color:#fff;width:26px;height:26px;border-radius:50%;cursor:pointer;font-size:13px}",
    "#as-chat-msgs{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:10px;background:#F6F8FA;font-size:14px;line-height:1.5}",
    ".as-msg{max-width:85%;padding:10px 13px;border-radius:14px;white-space:pre-wrap;word-wrap:break-word}",
    ".as-msg.user{align-self:flex-end;background:#0B5963;color:#fff;border-bottom-right-radius:4px}",
    ".as-msg.bot{align-self:flex-start;background:#fff;color:#15364B;border:1px solid #e2edf0;border-bottom-left-radius:4px}",
    ".as-msg.err{background:#fef2f2;color:#b91c1c;border:1px solid #fecaca;align-self:flex-start}",
    ".as-msg.typing{align-self:flex-start;color:#5d7680;font-style:italic;background:#fff;border:1px solid #e2edf0}",
    "#as-chat-inp{display:flex;gap:8px;padding:12px;border-top:1px solid #e2edf0;background:#fff}",
    "#as-chat-inp input{flex:1;padding:11px 14px;border:1.5px solid #d5e3e6;border-radius:24px;font-size:14px;outline:none}",
    "#as-chat-inp input:focus{border-color:#0B5963}",
    "#as-chat-inp button{background:#f59e0b;color:#0a2b33;border:none;border-radius:24px;padding:11px 18px;font-weight:800;cursor:pointer;font-size:14px}",
    "#as-chat-inp button:disabled{opacity:.5;cursor:wait}",
    "#as-chat-note{font-size:10.5px;color:#94a3b8;text-align:center;padding:5px 12px 8px;background:#fff}",
    "@media(max-width:420px){#as-chat-box{right:10px;bottom:80px;width:calc(100vw - 20px);height:70vh}}"
  ].join("");
  var st = document.createElement("style");
  st.textContent = css;
  document.head.appendChild(st);

  /* ---- разметка ---- */
  var btn = document.createElement("button");
  btn.id = "as-chat-btn";
  btn.setAttribute("aria-label", "Открыть чат");
  btn.innerHTML = "⚓";
  document.body.appendChild(btn);

  var box = document.createElement("div");
  box.id = "as-chat-box";
  box.innerHTML =
    '<div id="as-chat-head">⚓ Помощник Atlantic Sail' +
    '<button class="as-x" aria-label="Закрыть">✕</button></div>' +
    '<div id="as-chat-msgs"></div>' +
    '<div id="as-chat-inp"><input id="as-chat-txt" placeholder="Ваш вопрос о переходах..." autocomplete="off"/><button id="as-chat-send">➤</button></div>' +
    '<div id="as-chat-note">ИИ-помощник · цены и наличие уточняйте у организатора</div>';
  document.body.appendChild(box);

  var msgs = document.getElementById("as-chat-msgs");
  var txt = document.getElementById("as-chat-txt");
  var send = document.getElementById("as-chat-send");

  /* ---- история ---- */
  function loadHist() {
    try { return JSON.parse(localStorage.getItem(HISTORY_KEY)) || []; } catch (e) { return []; }
  }
  function saveHist(h) {
    try { localStorage.setItem(HISTORY_KEY, JSON.stringify(h.slice(-12))); } catch (e) {}
  }

  function addMsg(role, text) {
    var m = document.createElement("div");
    m.className = "as-msg " + role;
    m.textContent = text;
    msgs.appendChild(m);
    msgs.scrollTop = msgs.scrollHeight;
    return m;
  }

  function sendMsg() {
    var text = txt.value.trim();
    if (!text) return;
    var hist = loadHist();
    addMsg("user", text);
    txt.value = "";
    send.disabled = true;

    var typing = addMsg("typing", "Думаю…");
    hist.push({ role: "user", text: text });

    fetch(API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, history: hist.slice(-10) })
    })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        typing.remove();
        if (d.reply) {
          addMsg("bot", d.reply);
          hist.push({ role: "bot", text: d.reply });
          saveHist(hist);
        } else {
          addMsg("err", (d.error && d.error.message) ? d.error.message : "Не удалось получить ответ.");
        }
      })
      .catch(function () {
        typing.remove();
        addMsg("err", "Сеть недоступна. Попробуйте ещё раз или напишите в Telegram @captainatlanticbot.");
      })
      .finally(function () { send.disabled = false; txt.focus(); });
  }

  btn.addEventListener("click", function () {
    var open = box.classList.toggle("open");
    btn.innerHTML = open ? "✕" : "⚓";
    if (open) {
      txt.focus();
      var hist = loadHist();
      if (!msgs.children.length && (!hist.length)) {
        addMsg("bot", "Привет! 👋 Я помощник Atlantic Sail. Подскажу по переходам, каютам и маршрутам. О чём хотите узнать?");
      }
      if (hist.length && !msgs.children.length) {
        addMsg("bot", "Продолжим с того, на чём остановились.");
      }
    }
  });
  document.querySelector("#as-chat-head .as-x").addEventListener("click", function () {
    box.classList.remove("open");
    btn.innerHTML = "⚓";
  });
  send.addEventListener("click", sendMsg);
  txt.addEventListener("keydown", function (e) { if (e.key === "Enter") sendMsg(); });
})();