const reportList = document.getElementById("reportList");

document.addEventListener("DOMContentLoaded", loadReports);

async function loadReports() {
  try {
    const data = await api.get("/reports");
    reportList.innerHTML = "";

    const baseHost = CONFIG.BASE_URL.replace("/api/v1", "");

    // Buat header tabel
    const table = document.createElement("table");
    table.style.width = "100%";
    table.style.borderCollapse = "collapse";
    table.innerHTML = `
      <thead>
        <tr>
          <th style="border:1px solid #ccc; padding:5px">No</th>
          <th style="border:1px solid #ccc; padding:5px">Image</th>
          <th style="border:1px solid #ccc; padding:5px">Label</th>
          <th style="border:1px solid #ccc; padding:5px">Confidence</th>
          <th style="border:1px solid #ccc; padding:5px">Action</th>
        </tr>
      </thead>
      <tbody></tbody>
    `;

    const tbody = table.querySelector("tbody");

    data.forEach((r, index) => {
      const imgUrl = r.image_path.startsWith("http")
        ? r.image_path
        : `${baseHost}/${r.image_path}`;

      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td style="border:1px solid #ccc; padding:5px; text-align:center">${
          index + 1
        }</td>
        <td style="border:1px solid #ccc; padding:5px; text-align:center">
          <img src="${imgUrl}" width="24" height="24" />
        </td>
        <td style="border:1px solid #ccc; padding:5px">${r.label}</td>
        <td style="border:1px solid #ccc; padding:5px; text-align:right">${r.confidence.toFixed(
          2
        )}%</td>
        <td style="border:1px solid #ccc; padding:5px; text-align:center">
          <button onclick="deleteReport(${r.id})">Delete</button>
        </td>
      `;
      tbody.appendChild(tr);
    });

    reportList.appendChild(table);
  } catch (err) {
    console.error(err);
  }
}

async function deleteReport(id) {
  if (!confirm("Delete this report?")) return;
  await api.delete(`/reports/${id}`);
  loadReports();
}
