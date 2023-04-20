// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];
function clearModal (){
      document.querySelector('[name="event_name"]').value = ""
    document.querySelector('[name="event_date"]').value = ""
      document.querySelector('[name="event_description"]').value = ""
      document.querySelector('[name="event_time"]').value = ""

      document.getElementById("fileLblPrompt").innerHTML = "Add Event Image:"
    document.getElementById("chooseFile").required = true;
    document.getElementById("deleteButton").hidden = false;


}
// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
  clearModal()
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