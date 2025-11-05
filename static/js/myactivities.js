document.getElementById("year").textContent = new Date().getFullYear();

const container = document.getElementById("myActivitiesContainer");

// Load activities from server-rendered Jinja variable
const myActivities = {{ activities | tojson }};

if (myActivities.length === 0) {
  container.innerHTML = `
    <div style="text-align:center; padding:50px;">
      <h3>No activities joined yet!</h3>
      <p>Go to <a href="{{ url_for('vol_post') }}" style="color:#007bff; text-decoration:none;">All Activities</a> to join one.</p>
    </div>
  `;
} else {
  myActivities.forEach(activity => {
    const card = document.createElement("div");
    card.classList.add("activity-card");
    card.innerHTML = `
      <h3>${activity.activity_name}</h3>
      <p><strong>Organization:</strong> ${activity.org_name}</p>
      <p><strong>Date:</strong> ${activity.activity_date}</p>
      <p><strong>Time:</strong> ${activity.activity_time}</p>
      <p><strong>Location:</strong> ${activity.address}</p>
      <p><strong>Purpose:</strong> ${activity.purpose}</p>
      <button class="btn" onclick="cancelActivity(${activity.activity_id}, this)">Cancel Participation</button>
    `;
    container.appendChild(card);
  });
}

// Cancel participation
function cancelActivity(activityId, btn) {
  fetch(`/myactivities/cancel/${activityId}`, { method: 'POST' })
    .then(res => res.json())
    .then(data => {
      alert(data.message);
      if (data.status === "success") btn.closest('.activity-card').remove();
    })
    .catch(err => {
      console.error(err);
      alert("Error canceling participation.");
    });
}
function confirmLeave() {
  return confirm("Are you sure you want to leave this activity?\nYou will lose your participation.");
}
