const password = document.getElementById("password");
  const confirmPassword = document.getElementById("confirm-password");

  confirmPassword.addEventListener("input", () => {
    if (confirmPassword.value === password.value) {
      confirmPassword.setCustomValidity("");
    } else {
      confirmPassword.setCustomValidity("Passwords do not match");
    }
  });