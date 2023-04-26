const myElements = document.querySelectorAll("#flagIcon");


myElements.forEach((element) => {
  element.addEventListener("click", (event) => {
   let currentColor = event.target.style.color;
    let color = currentColor === "yellow" ? "#818488" : "yellow";
    event.target.style.color = color;
  });
});

document.addEventListener("DOMContentLoaded", function() {
  const flagButtons = document.querySelectorAll(".fa-solid");
  flagButtons.forEach(function(button) {
    button.addEventListener("click", function() {
      const eventId = this.closest(".event").dataset.eventid;
      console.log(this.closest(".event").dataset)
      const xhr = new XMLHttpRequest();
      xhr.open("POST", "/events/flagEvent");
      xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
      xhr.onload = function() {
        if (xhr.status === 200) {
          alert("Event flagged successfully!");
        } else {
          alert("An error occurred while flagging the event.");
        }
      };
      xhr.send("event_id=" + encodeURIComponent(eventId));
    });
  });
});
