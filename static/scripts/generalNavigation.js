const navBar = '   <div class="navDiv">\n' +
    '\n' +
    '    <nav class="navbar">\n' +
    '\n' +
    '\n' +
    '        <div class="logo"><img src="/static/images/lucidLogo.png" id="logo" alt="logo"></div>\n' +
    '\n' +
    '\n' +
    '        <!-- USING CHECKBOX HACK -->\n' +
    '\n' +
    '        <input type="checkbox" id="checkbox_toggle"/>\n' +
    '\n' +
    '        <label for="checkbox_toggle" class="hamburger">&#9776;</label>\n' +
    '\n' +
    '        <!-- NAVIGATION MENUS -->\n' +
    '\n' +
    '        <div class="menu">\n' +
    '            <ul>\n' +
    '                <li><a href="/">Home</a></li>\n' +
    '\n' +
    '                <li><a href="/events">Events</a></li>\n' +
    '\n' +
    '                <li><a href="/collaborations">Collaborations</a></li>\n' +
    '\n' +
    '                <li><a href="/about">About</a></li>\n' +
    '                <li><a href="/account/login">Account</a></li>\n' +
    '\n' +
    '\n' +
    '            </ul>\n' +
    '\n' +
    '\n' +
    '        </div>\n' +
    '\n' +
    '\n' +
    '    </nav>\n' +
    '</div>';
class navigationBar extends HTMLElement {
  constructor() {
    super();
    this.innerHTML = navBar;
  }
}

customElements.define("navbar-component", navigationBar);

const footer = '        <footer>\n' +
    '        <h6 class="underdog">Website by 407 Underdogs</h6>\n' +
    '        <p class="copyright">&copy; 2023 407UnderDogs. All Rights Reserved.</p>\n' +
    '        </footer>';
class footerBar extends HTMLElement {
  constructor() {
    super();
    this.innerHTML = footer;
  }
}


 customElements.define("footer-component", footerBar);