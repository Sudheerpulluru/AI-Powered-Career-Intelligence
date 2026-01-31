document.addEventListener("DOMContentLoaded", () => {

  // ===============================
  // Demand Distribution (Bar Chart)
  // ===============================
  const demandCtx = document.getElementById("demandChart");
  if (demandCtx) {
    new Chart(demandCtx, {
      type: "bar",
      data: {
        labels: Object.keys(demandCounts),
        datasets: [{
          label: "Demand Count",
          data: Object.values(demandCounts),
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false }
        }
      }
    });
  }

  // ===============================
  // Demand Trend (Line Chart)
  // ===============================
  const trendCtx = document.getElementById("trendChart");
  if (trendCtx) {
    new Chart(trendCtx, {
      type: "line",
      data: {
        labels: recentPredictions.map((_, i) => `#${i + 1}`),
        datasets: [{
          label: "Demand Trend",
          data: recentPredictions.map(d =>
            d === "High" ? 3 : d === "Medium" ? 2 : 1
          ),
          tension: 0.4,
          fill: true
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            ticks: {
              callback: v => ["", "Low", "Medium", "High"][v]
            }
          }
        }
      }
    });
  }

});
