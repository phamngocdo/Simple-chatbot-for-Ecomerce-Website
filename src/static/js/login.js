document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("loginForm");
  const rememberMeCheckbox = document.getElementById("remember");

  if (localStorage.getItem("rememberMe") === "true") {
    document.getElementById("email").value = localStorage.getItem("email") || "";
    const encryptedPassword = localStorage.getItem("password");
    if (encryptedPassword) {
      document.getElementById("password").value = atob(encryptedPassword);
    }
    rememberMeCheckbox.checked = true;
  }

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(loginForm);
    const email = formData.get("email");
    const password = formData.get("password");

    if (!password || password.length < 8) {
      alert("Password must be at least 8 characters long.");
      return;
    }

    try {
      const response = await fetch("/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      if (response.ok) {
        window.location.href = "/";
      } else {
        const error = await response.json();
        alert(error.detail || "Login failed. Please check your credentials.");
      }
    } catch (err) {
      console.error("Login error:", err);
      alert("Something went wrong. Please try again.");
    }
  });
});
