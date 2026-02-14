function joinRoom() {
  const userId = document.getElementById("userId").value;

  fetch("/assign", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId }),
  })
    .then((res) => res.json())
    .then((data) => {
      const resultDiv = document.getElementById("result");

      if (data.link) {
        resultDiv.innerHTML = `
          <p><strong>${data.room_name}</strong></p>
          <p><a href="${data.link}" target="_blank">Click here to join</a></p>
        `;
      } else {
        resultDiv.innerHTML = `<p style="color:red;">${data.error}</p>`;
      }
    });
}
