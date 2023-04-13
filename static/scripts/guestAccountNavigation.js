const accountNavigation = '     <div class = "accountMenu">\n' +
    '            <input type="checkbox" id="checkbox_toggle"/>\n' +
    '             <label for="checkbox_toggle" class="hamburger">&#9776;</label>\n' +
    '            <div class="left">\n' +
    '\n' +
    '\n' +
    '        <img src="/static/images/lucidLogo.png" id="menuLogo">\n' +
    '\n' +
    '        <div class="leftContent">\n' +
    '            <img src="/static/images/user.png">\n' +
    '            <label style="color: blue"> <a href="/management"> Personal Information </a> </label> <br> <br>\n' +
    '            <img src="/static/images/folder.png">\n' +
    '            <label style="color: blue"> <a href="/events"> Flagged Events </a> </label> <br> <br>\n' +

    '        </div>\n' +
    '\n' +
    '        <button class="button" type="buttom"> Sign Out</button>\n' +
    '    </div>\n' +
    '    </div>';
class navigation extends HTMLElement {
  constructor() {
    super();
    this.innerHTML = accountNavigation;
  }
}

customElements.define("navigation-component", navigation);