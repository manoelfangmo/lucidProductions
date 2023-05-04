const guestAccountNavigation = '     <div class = "accountMenu">\n' +
    '            <input type="checkbox" id="checkbox_toggle"/>\n' +
    '             <label for="checkbox_toggle" class="hamburger">&#9776;</label>\n' +
    '            <div class="left">\n' +
    '\n' +
    '\n' +
    '        <a href="/"><img src="/static/images/lucidLogo.png" id="menuLogo"></a>\n' +
    '\n' +
    '        <div class="leftContent">\n' +
    '            <img src="/static/images/user.png">\n' +
    '            <label style="color: blue"> <a href="/account"> Personal Information </a> </label> <br> <br>\n' +
    '            <img src="/static/images/folder.png">\n' +
    '            <label style="color: blue"> <a href="/guest/guestFlag"> Flagged Events </a> </label> <br> <br>\n' +

    '        </div>\n' +
    '\n' +
    '        <a href="/logout"><button class="button" type="button"> Sign Out</button></a>\n' +
    '    </div>\n' +
    '    </div>';
class guestNavigation extends HTMLElement {

  constructor() {
    super();
    this.innerHTML = guestAccountNavigation;
  }
}
t
customElements.define("guest-navigation-component", guestNavigation);