document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("loginForm");
  const rememberMeCheckbox = document.getElementById("remember");

  if (localStorage.getItem("rememberMe") === "true") {
    document.getElementById("email").value = localStorage.getItem("email") || "";
    document.getElementById("password").value = localStorage.getItem("password") || "";
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
        body: formData,
      });

      if (response.ok) {
        window.location.href = "/chat";

        if (rememberMeCheckbox.checked) {
          localStorage.setItem("email", email);
          localStorage.setItem("password", password);
          localStorage.setItem("rememberMe", "true");
        } else {
          localStorage.removeItem("email");
          localStorage.removeItem("password");
          localStorage.removeItem("rememberMe");
        }
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
