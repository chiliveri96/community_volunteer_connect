document.getElementById("year").textContent = new Date().getFullYear();

const container = document.getElementById("activitiesContainer");

// Assuming Flask passes `activities` as a Jinja variable
const activities = {{ activities | tojson }};

activities.forEach(activity => {
  const card = document.createElement("div");
  card.classList.add("activity-card");
  card.innerHTML = `
    <h3>${activity.activity_name}</h3>
    <p><strong>Organization:</strong> ${activity.org_name}</p>
    <p><strong>Purpose:</strong> ${activity.purpose}</p>
    <p><strong>Date:</strong> ${activity.activity_date} | <strong>Time:</strong> ${activity.activity_time}</p>
    <p><strong>Location:</strong> ${activity.address}</p>
    <p><strong>Volunteers Needed:</strong> ${activity.volunteers_required}</p>
    <p><strong>Category:</strong> ${activity.category}</p>
    <button class="btn" onclick="joinActivity(${activity.id}, this)">Join Activity</button>
  `;
  container.appendChild(card);
});

// Join button AJAX
function joinActivity(activityId, btn) {
  fetch(`/volunteer/join/${activityId}`, { method: 'POST' })
    .then(res => res.json())
    .then(data => {
      alert(data.message);
      if (data.status === "success") btn.disabled = true;
    })
    .catch(err => {
      console.error(err);
      alert("Error joining activity.");
    });
}
