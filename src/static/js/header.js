document.addEventListener("DOMContentLoaded", () => {
  const guestView = document.getElementById("guest-view");
  const userView = document.getElementById("user-view");
  const headerUsername = document.getElementById("header-username");

  // Function to parse JWT token
  function parseJwt(token) {
    try {
      const base64Url = token.split(".")[1];
      const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split("")
          .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
          .join("")
      );
      return JSON.parse(jsonPayload);
    } catch (e) {
      return null;
    }
  }

  // Check if the user is logged in
  const token = document.cookie
    .split("; ")
    .find((row) => row.startsWith("access_token="))
    ?.split("=")[1];

  if (token) {
    const userData = parseJwt(token);
    if (userData && userData.sub) {
      // User is logged in
      guestView.style.display = "none";
      userView.style.display = "flex";
      headerUsername.textContent = userData.username || "User";
    }
  } else {
    // User is not logged in
    guestView.style.display = "flex";
    userView.style.display = "none";
  }

  // Logout functionality
  const logoutBtn = document.getElementById("logout-btn");
  logoutBtn.addEventListener("click", () => {
    document.cookie = "access_token=; Max-Age=0; path=/";
    window.location.href = "/";
  });
});