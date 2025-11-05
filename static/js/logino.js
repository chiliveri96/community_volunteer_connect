document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("organizationLoginForm");

  form.addEventListener("submit", function (e) {
    const phone = document.getElementById("organizationPhone").value.trim();
    const password = document.getElementById("organizationPassword").value.trim();

    if (!phone || !password) {
      alert("All fields are required!");
      e.preventDefault();
      return;
    }

    if (!/^[0-9]{10}$/.test(phone)) {
      alert("Phone number must be 10 digits.");
      e.preventDefault();
      return;
    }
  });
});
