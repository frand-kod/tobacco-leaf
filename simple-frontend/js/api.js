window.api = {
  async request(method, url, data = null, isForm = false) {
    const token = localStorage.getItem("token");

    const headers = {};
    if (!isForm) headers["Content-Type"] = "application/json";
    if (token) headers["Authorization"] = `Bearer ${token}`;

    const options = {
      method,
      headers,
    };

    if (data) {
      options.body = isForm ? data : JSON.stringify(data);
    }

    const res = await fetch(`${CONFIG.BASE_URL}${url}`, options);

    if (res.status === 401) {
      localStorage.removeItem("token");
      alert("Session expired, login again");
      window.location.href = "index.html";
      return;
    }

    if (!res.ok) {
      const err = await res.text();
      throw new Error(err || "Request failed");
    }

    return res.json();
  },

  get(url) {
    return this.request("GET", url);
  },

  post(url, data, isForm = false) {
    return this.request("POST", url, data, isForm);
  },

  put(url, data) {
    return this.request("PUT", url, data);
  },

  delete(url) {
    return this.request("DELETE", url);
  },
};
