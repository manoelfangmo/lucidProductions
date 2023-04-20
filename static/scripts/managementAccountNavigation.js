const managementAccountNavigation = '     <div class = "accountMenu">\n' +
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
    '            <img src="/static/images/review.png">\n' +
    '            <label style="color: blue"> <a href="/management/reviews">Reviews</a> </label> <br> <br>\n' +
    '            <img src="/static/images/data.png">\n' +
    '            <label style="color: blue"> <a href="/management/analytics">Analytics</a> </label> <br> <br>\n' +
    '            <img src="/static/images/add.png">\n' +
    '            <label style="color: blue"> <a href="/management/users"> Management Accounts </a> </label> <br> <br>\n' +
    '            <img src="/static/images/hello.webp">\n' +
    '            <label style="color: blue"> <a href="/management/inquiries">Inquiries</a> </label> <br> <br>\n' +
    '            <img src="/static/images/event.png">\n' +
    '            <label style="color: blue"> <a href="/management/events">Events</a> </label> <br> <br>\n' +
    '        </div>\n' +

    '        <button class="button" type="button"> Sign Out</button>\n' +
    '    </div>\n' +
    '    </div>';
class managementNavigation extends HTMLElement {
  constructor() {
    super();
    this.innerHTML = managementAccountNavigation;
  }
}

customElements.define("navigation-component", managementNavigation);

