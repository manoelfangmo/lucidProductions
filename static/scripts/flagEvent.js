const myElements = document.querySelectorAll("#flagIcon");

if (userIsGuest) {
    let currColor
    myElements.forEach((element) => {
        element.addEventListener("click", (event) => {
            currentColor = event.target.style.color;
            let color = currentColor === "yellow" ? "#818488" : "yellow";
            event.target.style.color = color;
            currColor = color
        });
    });
    document.addEventListener("DOMContentLoaded", function () {
        const flagButtons = document.querySelectorAll(".fa-solid");
        flagButtons.forEach(function (button) {
            button.addEventListener("click", function () {
                const eventId = this.closest(".event").dataset.eventid;
                console.log(this.closest(".event").dataset)
                const xhr = new XMLHttpRequest();
                console.log(currColor)
                if (currColor === "#818488") { //delete if flag color switches to gray
                    xhr.open("POST", "/events/flagEvent/deleteFlag");

                } else {
                    xhr.open("POST", "/events/flagEvent");
                }
                xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                xhr.onload = function () {
                    if (xhr.status === 200) {
                        alert("Successful!");
                    } else {
                        alert("Error Occurred");
                    }
                };
                xhr.send("event_id=" + encodeURIComponent(eventId));
            });
        });
    });
}