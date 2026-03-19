(function () {
  function collectTables() {
    const cards = Array.from(document.querySelectorAll("#tablesGrid .table-card"));
    const result = {};
    cards.forEach((card) => {
      const title = (card.querySelector("h3")?.textContent || "").trim();
      const rows = Array.from(card.querySelectorAll("tbody tr")).map((tr) =>
        Array.from(tr.querySelectorAll("td")).map((td) => {
          const dateInput = td.querySelector("input[type='date']");
          if (dateInput) return dateInput.value || "";
          return (td.textContent || "").trim();
        })
      );
      result[title] = rows;
    });
    return result;
  }

  function applyTables(tables) {
    const cards = Array.from(document.querySelectorAll("#tablesGrid .table-card"));
    cards.forEach((card) => {
      const title = (card.querySelector("h3")?.textContent || "").trim();
      const rows = tables?.[title];
      if (!Array.isArray(rows)) return;

      const trList = Array.from(card.querySelectorAll("tbody tr"));
      trList.forEach((tr, i) => {
        const savedRow = rows[i];
        if (!Array.isArray(savedRow)) return;
        const tds = Array.from(tr.querySelectorAll("td"));
        tds.forEach((td, j) => {
          if (savedRow[j] === undefined) return;
          const dateInput = td.querySelector("input[type='date']");
          if (dateInput) {
            dateInput.value = savedRow[j] || "";
          } else {
            td.textContent = savedRow[j];
          }
        });
      });
    });
  }

  function stationProgress() {
    const station = window.STATION;
    const value = localStorage.getItem(`metro_foh_progress_${station}`);
    try {
      return value ? JSON.parse(value) : null;
    } catch {
      return null;
    }
  }

  function renderButtons() {
    const host = document.getElementById("stationKpis");
    if (!host) return;
    if (host.querySelector('[data-persist="save"]')) return;

    host.insertAdjacentHTML(
      "beforeend",
      '<button data-persist="save" class="hero-pill" style="border:0;cursor:pointer;">Save</button>' +
        '<button data-persist="load" class="hero-pill" style="border:0;cursor:pointer;">Load</button>'
    );
  }

  async function saveStation() {
    const station = window.STATION;
    if (!station) return;
    const payload = {
      tables: collectTables(),
      progress: stationProgress(),
      updatedAt: new Date().toISOString(),
    };

    const res = await fetch(`/api/station/${station}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) throw new Error("Save failed");
    alert("Saved successfully.");
  }

  let autoSaveTimer = null;
  window.autoPersistStationProgress = function autoPersistStationProgress(progressPayload) {
    clearTimeout(autoSaveTimer);
    autoSaveTimer = setTimeout(async () => {
      const station = window.STATION;
      if (!station) return;
      const payload = {
        tables: collectTables(),
        progress: progressPayload || stationProgress(),
        updatedAt: new Date().toISOString(),
      };
      try {
        await fetch(`/api/station/${station}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
      } catch {
        // Keep local storage fallback when API is unavailable.
      }
    }, 250);
  };

  async function loadStation(options) {
    const silent = !!(options && options.silent);
    const station = window.STATION;
    if (!station) return;

    const res = await fetch(`/api/station/${station}`);
    if (!res.ok) throw new Error("Load failed");

    const payload = await res.json();
    applyTables(payload.tables || {});

    document.getElementById("tablesGrid")?.dispatchEvent(new Event("input", { bubbles: true }));
    if (!silent) alert("Loaded saved data.");
  }

  async function syncHomeProgress() {
    if (!document.getElementById("portfolioTimeline")) return;
    try {
      const res = await fetch("/api/progress");
      if (!res.ok) return;
      const progress = await res.json();
      Object.entries(progress || {}).forEach(([station, value]) => {
        localStorage.setItem(`metro_foh_progress_${station}`, JSON.stringify(value));
      });
      if (typeof window.renderSummary === "function") window.renderSummary();
      if (typeof window.renderPortfolioTimeline === "function") window.renderPortfolioTimeline();
    } catch {
      // ignore offline API mode
    }
  }

  window.attachPersistence = function attachPersistence() {
    renderButtons();
    document.addEventListener("click", async (e) => {
      const target = e.target;
      if (!(target instanceof HTMLElement)) return;
      if (target.dataset.persist === "save") {
        try { await saveStation(); } catch { alert("Unable to save. Start server.py first."); }
      }
      if (target.dataset.persist === "load") {
        try { await loadStation({ silent: false }); } catch { alert("Unable to load. Start server.py first."); }
      }
    });
  };

  window.syncHomeProgress = syncHomeProgress;
})();
