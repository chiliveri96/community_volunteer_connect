function validateForm() {
  let fields = [
    "activity_name",
    "purpose",
    "activity_date",
    "activity_time",
    "address",
    "volunteers_required",
    "contact"
  ];

  for (let f of fields) {
    if (document.getElementById(f).value.trim() === "") {
      alert("All fields are required!");
      return false;
    }
  }

  let volunteers = document.getElementById("volunteers_required").value;
  if (volunteers <= 0) {
    alert("Volunteers required must be greater than 0");
    return false;
  }

  return true;
}
