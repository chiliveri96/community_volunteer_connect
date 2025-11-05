function openEditModal(id, name, purpose, date, time, address, volunteers, skills, contact) {
    document.getElementById("editModal").classList.remove("hidden");

    document.getElementById("title").value = name;
    document.getElementById("description").value = purpose;
    document.getElementById("date").value = date;
    document.getElementById("time").value = time;
    document.getElementById("location").value = address;
    document.getElementById("volunteers").value = volunteers;
    document.getElementById("skills").value = skills;  // ✅ correct field name
    document.getElementById("contact").value = contact;

    document.getElementById("editForm").action = "/organization/update_activity/" + id;
}
