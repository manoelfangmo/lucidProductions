// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btns = document.getElementsByClassName("eventEditor");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When any button with class "eventEditor" is clicked, open the modal
for (var i = 0; i < btns.length; i++) {
  let name = btns[i].getAttribute('eventName')
  let description = btns[i].getAttribute('eventDescription')
  let date = btns[i].getAttribute('eventDate')
  let time = btns[i].getAttribute('eventTime')
  let id = btns[i].getAttribute('eventId')


  btns[i].onclick = () =>{
    modal.style.display = "block";
    document.querySelector('[name="event_name"]').value = name
    document.querySelector('[name="event_description"]').value = description
    document.querySelector('[name="event_date"]').value = date
    document.querySelector('[name="event_time"]').value = time
    document.querySelector('[name="event_id"]').value = id
    document.getElementById("fileLblPrompt").innerHTML = "Change Event Image:"
    document.getElementById("chooseFile").required = false
  document.getElementById("deleteButton").hidden = false



  }
}


// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}