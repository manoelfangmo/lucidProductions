const managementAccountNavigation = '     <div class = "accountMenu">\n' +
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
    '            <img src="/static/images/review.png">\n' +
    '            <label style="color: blue"> <a href="/management/reviews">Reviews</a> </label> <br> <br>\n' +
    '            <img src="/static/images/data.png">\n' +
    '            <label style="color: blue"> <a href="/management/analytics">Analytics</a> </label> <br> <br>\n' +
    '            <img src="/static/images/add.png">\n' +
    '            <label style="color: blue"> <a href="/management/users"> Management Accounts </a> </label> <br> <br>\n' +
    '            <img src="/static/images/hello.webp">\n' +
    '            <label style="color: blue"> <a href="/management/inquiries">Inquiries</a> </label> <br> <br>\n' +
    '            <img src="/static/images/event.png">\n' +
    '            <label style="color: blue"> <a href="/management/event">Events</a> </label> <br> <br>\n' +
    '        </div>\n' +

    '        <a href="/logout"><button class="button" type="button"> Sign Out</button></a>\n' +
    '    </div>\n' +
    '    </div>';
class managementNavigation extends HTMLElement {
  constructor() {
    super();
    this.innerHTML = managementAccountNavigation;
  }
}

customElements.define("management-navigation-component", managementNavigation);

