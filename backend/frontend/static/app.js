const $ = (id) => document.getElementById(id);

function setStatus(txt){ $("status").textContent = txt || ""; }

async function postJSON(url, body){
  const res = await fetch(url, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(body),
  });
  if(!res.ok){
    const t = await res.text().catch(()=> "");
    throw new Error(`HTTP ${res.status}: ${t}`);
  }
  return res.json();
}

function pretty(obj){
  return JSON.stringify(obj, null, 2);
}

async function send(){
  const text = $("chatInput").value.trim();
  if(!text) return;

  $("sendBtn").disabled = true;
  setStatus("sending…");

  try{
    const namespace = $("namespace").value.trim() || "default";
    const data = await postJSON("/api/chat", { text, namespace, session_id: "demo" });
    $("chatOut").textContent = data.response;
    $("traceOut").textContent = pretty(data.trace);
    setStatus("done");
  }catch(e){
    setStatus(e.message);
  }finally{
    $("sendBtn").disabled = false;
  }
}

async function seed(){
  $("seedBtn").disabled = true;
  setStatus("seeding memory…");

  const namespace = $("namespace").value.trim() || "default";
  const title = "Что такое pgvector и почему он удобен для AiMW";
  const content = [
    "pgvector — расширение PostgreSQL, которое добавляет тип vector и операции для поиска ближайших соседей.",
    "В AiMW это позволяет хранить структурированные данные, события и embeddings в одном storage-слое.",
    "Это упрощает RAG: мы вычисляем эмбеддинг запроса и делаем векторный поиск с порогами/лимитами,",
    "а дальше собираем контекст и выполняем запрос через адаптер LLM."
  ].join(" ");

  try{
    const out = await postJSON("/api/memory/write", { namespace, title, content });
    setStatus(`memory id: ${out.id}`);
  }catch(e){
    setStatus(e.message);
  }finally{
    $("seedBtn").disabled = false;
  }
}

function initTheme(){
  const key = "aimw_theme";
  const saved = localStorage.getItem(key) || "dark";
  document.documentElement.dataset.theme = saved;

  $("themeBtn").addEventListener("click", ()=>{
    const cur = document.documentElement.dataset.theme || "dark";
    const next = (cur === "dark") ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    localStorage.setItem(key, next);
  });
}

$("sendBtn").addEventListener("click", send);
$("seedBtn").addEventListener("click", seed);
$("chatInput").addEventListener("keydown", (e)=>{
  if((e.ctrlKey || e.metaKey) && e.key === "Enter") send();
});

initTheme();
