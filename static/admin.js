let savedPassword = "";

function loadAdmin() {
  const password = document.getElementById("adminPassword").value;

  fetch("/admin/data", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password: password }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.error) {
        document.getElementById("adminMessage").innerText = "Wrong password.";
        return;
      }

      savedPassword = password;

      document.getElementById("adminContent").style.display = "block";
      document.getElementById("adminMessage").innerText = "";

      let statsHTML = "<h3>Room Status</h3>";
      for (let room in data.rooms) {
        statsHTML += `<p>${room}: ${data.rooms[room].count} / 8</p>`;
      }

      statsHTML += `<p><strong>Total Assigned Users:</strong> ${data.total_users}</p>`;

      document.getElementById("roomStats").innerHTML = statsHTML;
    });
}

function resetSystem() {
  fetch("/admin/reset", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password: savedPassword }),
  })
    .then((res) => res.json())
    .then((data) => {
      alert(data.message || data.error);
      location.reload();
    });
}
