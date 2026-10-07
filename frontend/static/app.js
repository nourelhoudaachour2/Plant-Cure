const fileInput = document.getElementById("fileInput");
const analyzeBtn = document.getElementById("analyzeBtn");
const previewBox = document.getElementById("previewBox");
const resultBox = document.getElementById("resultBox");
const historyList = document.getElementById("historyList");

const statEconomies = document.getElementById("statEconomies");
const statTotal = document.getElementById("statTotal");
const statHealthy = document.getElementById("statHealthy");
const statDiseased = document.getElementById("statDiseased");

fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (!file) return;

  const imageURL = URL.createObjectURL(file);
  previewBox.innerHTML = `<img src="${imageURL}" alt="Prévisualisation">`;
});

analyzeBtn.addEventListener("click", async () => {
  const file = fileInput.files[0];

  if (!file) {
    resultBox.innerHTML = `<div class="empty-state">Veuillez sélectionner une image avant de lancer l'analyse.</div>`;
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  resultBox.innerHTML = `<div class="empty-state">Analyse en cours...</div>`;

  try {
    const response = await fetch("/api/analyser", {
      method: "POST",
      body: formData
    });

    const payload = await response.json();

    if (!payload.success) {
      resultBox.innerHTML = `<div class="empty-state">Erreur: ${payload.error}</div>`;
      return;
    }

    renderResult(payload.data);
    renderStats(payload.stats);
    await loadHistory();
  } catch (error) {
    resultBox.innerHTML = `<div class="empty-state">Une erreur est survenue pendant l'analyse.</div>`;
  }
});

function renderStats(stats) {
  statEconomies.textContent = `${stats.economies_total} TND`;
  statTotal.textContent = stats.total_predictions;
  statHealthy.textContent = stats.plantes_saines;
  statDiseased.textContent = stats.plantes_malades;
}

function renderResult(entry) {
  const p = entry.prediction;
  const r = entry.recommendation;

  const orgPrice = r.traitement_organique?.prix_estime || 0;
  const chimPrice = r.traitement_chimique?.prix_estime || 0;
  const saving = Math.max(chimPrice - orgPrice, 0);

  resultBox.innerHTML = `
    <div class="result-header">
      <h2 class="result-title">${p.plant}</h2>
      <p class="result-sub"><strong>État / Maladie :</strong> ${p.is_healthy ? "Plante saine" : p.disease}</p>
      <p class="result-sub"><strong>Niveau de confiance :</strong> ${p.confidence}%</p>
      <p class="result-sub"><strong>Date :</strong> ${entry.date_analyse}</p>
    </div>

    <div class="section-card">
      <h3>Résumé</h3>
      <p>${r.resume}</p>
    </div>

    ${
      p.is_healthy
      ? `
      <div class="section-card">
        <h3>Recommandations d’entretien</h3>
        <ul class="clean-list">
          ${r.conseils.map(item => `<li>${item}</li>`).join("")}
        </ul>
      </div>

      <div class="section-card">
        <h3>Entretien organique conseillé</h3>
        <p><strong>Solution :</strong> ${r.traitement_organique.nom}</p>
        <p class="price"><strong>Coût estimé :</strong> ${orgPrice} TND</p>
      </div>

      <div class="section-card">
        <h3>Durée</h3>
        <p>${r.duree}</p>
      </div>
      `
      : `
      <div class="section-card">
        <h3>Causes possibles</h3>
        <ul class="clean-list">
          ${r.causes.map(item => `<li>${item}</li>`).join("")}
        </ul>
      </div>

      <div class="dual-grid">
        <div class="section-card">
          <h3>Traitement organique</h3>
          <p>${r.traitement_organique.nom}</p>
          <p class="price">Coût estimé : ${orgPrice} TND</p>
        </div>

        <div class="section-card">
          <h3>Traitement chimique</h3>
          <p>${r.traitement_chimique.nom}</p>
          <p class="price">Coût estimé : ${chimPrice} TND</p>
        </div>
      </div>

      <div class="saving-box">
        Économie estimée avec la solution organique : ${saving} TND
      </div>

      <div class="section-card">
        <h3>Mode d’application</h3>
        <p>${r.application}</p>
      </div>

      <div class="section-card">
        <h3>Durée estimée du traitement</h3>
        <p>${r.duree}</p>
      </div>

      <div class="section-card">
        <h3>Conseils utiles</h3>
        <ul class="clean-list">
          ${r.conseils.map(item => `<li>${item}</li>`).join("")}
        </ul>
      </div>
      `
    }
  `;
}

async function loadStats() {
  try {
    const response = await fetch("/api/stats");
    const stats = await response.json();
    renderStats(stats);
  } catch (e) {}
}

async function loadHistory() {
  try {
    const response = await fetch("/api/history");
    const history = await response.json();

    if (!history.length) {
      historyList.innerHTML = `<div class="empty-state">Aucune analyse enregistrée pour le moment.</div>`;
      return;
    }

    historyList.innerHTML = history.map(item => {
      const p = item.prediction;
      const label = p.is_healthy ? "Plante saine" : p.disease;

      return `
        <article class="history-item history-card">
          <div class="history-thumb">
            <img src="${item.image_url}" alt="${p.plant}">
          </div>
          <div class="history-content">
            <h4>${p.plant}</h4>
            <div class="history-meta">
              <span><strong>Résultat :</strong> ${label}</span>
              <span><strong>Confiance :</strong> ${p.confidence}%</span>
              <span><strong>Date :</strong> ${item.date_analyse}</span>
            </div>
          </div>
        </article>
      `;
    }).join("");
  } catch (e) {
    historyList.innerHTML = `<div class="empty-state">Impossible de charger l’historique.</div>`;
  }
}

loadStats();
loadHistory();