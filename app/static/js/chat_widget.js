(function(){
  const root = document.getElementById("chat-widget");
  if(!root) return;
  const btn = document.createElement("button");
  btn.textContent = "Чат з асистентом";
  btn.className = "btn";
  const panel = document.createElement("div");
  panel.style.display = "none";
  panel.style.position = "fixed";
  panel.style.right = "20px";
  panel.style.bottom = "60px";
  panel.style.width = "320px";
  panel.style.maxHeight = "50vh";
  panel.style.background = "#fff";
  panel.style.border = "1px solid #eee";
  panel.style.borderRadius = "10px";
  panel.style.padding = "8px";
  panel.style.overflow = "auto";

  const ta = document.createElement("textarea");
  ta.placeholder = "Ваше повідомлення...";
  ta.style.width = "100%";
  const send = document.createElement("button");
  send.textContent = "Надіслати";
  send.className = "btn";

  const out = document.createElement("div");
  out.style.marginTop = "8px";

  panel.appendChild(ta);
  panel.appendChild(send);
  panel.appendChild(out);

  btn.onclick = ()=> { panel.style.display = panel.style.display==="none" ? "block" : "none"; };
  send.onclick = async ()=>{
    const message = ta.value.trim();
    if(!message) return;
    out.innerHTML += `<div><strong>Ви:</strong> ${message}</div>`;
    ta.value = "";
    try{
      const r = await fetch("/api/chat", {
        method:"POST",
        headers:{ "Content-Type":"application/json"},
        body: JSON.stringify({ message })
      });
      const j = await r.json();
      out.innerHTML += `<div><strong>Бот:</strong> ${j.reply}</div>`;
      panel.scrollTop = panel.scrollHeight;
    }catch(e){
      out.innerHTML += `<div><em>Помилка: ${e}</em></div>`;
    }
  }

  root.appendChild(btn);
  root.appendChild(panel);
})();
