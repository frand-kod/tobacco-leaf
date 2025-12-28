const image = document.getElementById("image");

document.getElementById("predictForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData();
  formData.append("file", image.files[0]);

  try {
    await api.post("/model/predict", formData, true);
    await loadReports();
  } catch (err) {
    alert("Prediction failed");
  }
});
