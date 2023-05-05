function redirect(select) {
  var value = select.value;
  if (value) {
    var url = "/events?value=" + encodeURIComponent(value);
    window.location.href = url;

  }
}
document.addEventListener("DOMContentLoaded", function() {
  var select = document.getElementById("occurance");
  var params = new URLSearchParams(window.location.search);
  var value = params.get("value");
  if (value) {
    var option = select.querySelector('option[value="' + value + '"]');
    if (option) {
      option.selected = true;
    }
  }
});