const accountNavigation = '     <div class = "accountMenu">\n' +
    '            <input type="checkbox" id="checkbox_toggle"/>\n' +
    '             <label for="checkbox_toggle" class="hamburger">&#9776;</label>\n' +
    '            <div class="left">\n' +
    '\n' +
    '\n' +
    '        <a href="/"><img src="/static/images/lucidLogo.png" id="menuLogo"></a>\n' +
    '\n' +
    '        <div class="leftContent">\n' +
    '            <img src="/static/images/user.png">\n' +
    '            <label style="color: blue"> <a href="/guest"> Personal Information </a> </label> <br> <br>\n' +
    '            <img src="/static/images/folder.png">\n' +
    '            <label style="color: blue"> <a href="/events"> Flagged Events </a> </label> <br> <br>\n' +

    '        </div>\n' +
    '\n' +
    '        <a href="/logout"><button class="button" type="button"> Sign Out</button>\</a>\n' +
    '    </div>\n' +
    '    </div>';
class navigation extends HTMLElement {
  constructor() {
    super();
    this.innerHTML = accountNavigation;
  }
}

customElements.define("navigation-component", navigation);