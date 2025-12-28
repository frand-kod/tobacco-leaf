document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = {
    email: email.value,
    password: password.value,
  };

  try {
    const res = await api.post("/auth/login", payload);
    localStorage.setItem("token", res.access_token);
    window.location.href = "dashboard.html";
  } catch (err) {
    err.innerText = "Login failed";
  }
});

function logout() {
  // hapus token
  localStorage.removeItem("token");
  sessionStorage.removeItem("token");

  // redirect ke halaman login
  window.location.href = "/simple-frontend/index.html";
}
