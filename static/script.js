const funnyLoadingLines = [
  "Convincing the AI to sound human…",
  "Removing robot vibes… beep boop ❌",
  "Teaching silicon how emotions work…",
  "Untangling overly perfect sentences…",
  "Making it less LinkedIn, more real life…",
  "Injecting imperfections (on purpose)…",
  "Asking the AI to chill a bit…",
  "Turning AI into ‘yeah, that sounds human’…"
];

let loadingInterval = null;

function humanize() {
  const loader = document.getElementById("loader");
  const textEl = document.getElementById("text");
  const personaEl = document.getElementById("persona");

  // start loader
  loader.classList.remove("hidden");
  let i = 0;
  loader.innerText = funnyLoadingLines[i];

  loadingInterval = setInterval(() => {
    i++;
    loader.innerText = funnyLoadingLines[i % funnyLoadingLines.length];
  }, 1300);

  fetch("/humanize", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      text: textEl.value,
      persona: personaEl.value
    })
  })
    .then(res => res.json())
    .then(data => {
      clearInterval(loadingInterval);
      loader.classList.add("hidden");

      // OUTPUT
      document.getElementById("output").value = data.output || "";

      // METRICS
      document.getElementById("burst").innerText =
        data.burstiness ?? "–";
      document.getElementById("human").innerText =
        data.realism?.human_likeness ?? "–";

      if (data.meaning?.disagreement) {
        document.getElementById("meaning").innerText = "⚠️ Agents disagree";
      } else {
        document.getElementById("meaning").innerText = "Preserved";
      }

      // TRACE
      const traceEl = document.getElementById("trace");
      traceEl.innerHTML = "";
      (data.trace || []).forEach(step => {
        const li = document.createElement("li");
        li.innerText = step;
        traceEl.appendChild(li);
      });

      // DIFF (WHAT CHANGED)
      const diffEl = document.getElementById("diff");
      diffEl.innerHTML = "";

      if (!data.highlighted || data.highlighted.length === 0) {
        const msg = document.createElement("div");
        msg.className = "diff-line diff-same";
        msg.innerText = "No significant sentence-level changes detected.";
        diffEl.appendChild(msg);
      } else {
        data.highlighted.forEach(item => {
          const div = document.createElement("div");
          div.className =
            "diff-line " + (item.changed ? "diff-changed" : "diff-same");
          div.innerText = item.text;
          diffEl.appendChild(div);
        });
      }
    })
    .catch(err => {
      clearInterval(loadingInterval);
      loader.classList.add("hidden");
      console.error("Humanize error:", err);
    });
}

function copyOutput() {
  const output = document.getElementById("output");
  output.select();
  output.setSelectionRange(0, 99999);
  document.execCommand("copy");

  const btn = document.querySelector(".copy-btn");
  const oldText = btn.innerText;
  btn.innerText = "✅ Copied!";
  setTimeout(() => (btn.innerText = oldText), 1200);
}
