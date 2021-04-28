//adds a logout button to the home page
var addLogoutButton = function() {
    let navbar = document.getElementById("logout"); //reference the nav tag to put new stuff into
    let logoutBtn = document.createElement("form"); 
    logoutBtn.setAttribute("action", "/logout"); //the attributes of the form tag
    logoutBtn.setAttribute("method", "POST");
    logoutBtn.innerHTML = '<input name="logout" type="submit" value="Log Out"/>'; //what goes in bt the tags. doesn't have to be just plaintxt!
    navbar.appendChild(logoutBtn);

/*would be equivalent to putting this inside the home.html
        <nav id="nav">
            <form action='/logout' method='POST'>
                <input name="logout" type="submit" value="Log Out"/>
            </form>
        </nav>
*/
}

//adds a profile button to the home page, same logic as logout but redirects to diff route
var addProfileButton = function() {
    let navbar = document.getElementById("profile");
    let profileBtn = document.createElement("a");
    profileBtn.setAttribute("href", "/profile");
    profileBtn.innerHTML = 'Profile';
    profileBtn.classList += "nav-item nav-link";
    navbar.appendChild(profileBtn);
}



//adds a login button to the home page, same logic as logout but redirects to diff route
var addLoginButton = function() {
    let navbar = document.getElementById("login");
    let loginBtn = document.createElement("form");
    loginBtn.setAttribute("action", "/login");
    loginBtn.setAttribute("method", "POST");
    loginBtn.innerHTML = '<input name="login" type="submit" value="Log In/Register"/>';
    navbar.appendChild(loginBtn);
}

//adds a register button to the home page, same logic as logout but redirects to diff route
//deprecated
var addRegButton = function() {
    let navbar = document.getElementById("register");
    let regBtn = document.createElement("form");
    regBtn.setAttribute("action", "/register");
    regBtn.setAttribute("method", "POST");
    regBtn.innerHTML = '<input name="register" type="submit" value="Register"/>';
    navbar.appendChild(regBtn);
}

console.log(loggedIn);
if (loggedIn) {
    addProfileButton();
    addLogoutButton(); //uses loggedIn, provided by flask/jinja var in the script above this one in home.html, to determine what buttons to add
}
else {
    addLoginButton();
    addRegButton();
}

