//adds a logout button to the home page
var addLogoutButton = function() {
    let navbar = document.getElementById("nav"); //reference the nav tag to put new stuff into
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

//ADD A PROFILE BUTTON LATER
//ADD A PROFILE BUTTON LATER
//ADD A PROFILE BUTTON LATER
//ADD A PROFILE BUTTON LATER
//ADD A PROFILE BUTTON LATER
//ADD A PROFILE BUTTON LATER



//adds a login button to the home page, same logic as logout but redirects to diff route
var addLoginButton = function() {
    let navbar = document.getElementById("nav");
    let loginBtn = document.createElement("form");
    loginBtn.setAttribute("action", "/login");
    loginBtn.setAttribute("method", "POST");
    loginBtn.innerHTML = '<input name="login" type="submit" value="Log In"/>';
    navbar.appendChild(loginBtn);
}

//adds a register button to the home page, same logic as logout but redirects to diff route
var addRegButton = function() {
    let navbar = document.getElementById("nav");
    let regBtn = document.createElement("form");
    regBtn.setAttribute("action", "/register");
    regBtn.setAttribute("method", "POST");
    regBtn.innerHTML = '<input name="register" type="submit" value="Register"/>';
    navbar.appendChild(regBtn);
}


if (loggedIn) addLogoutButton(); //uses loggedIn, provided by flask/jinja var in the script above this one in home.html, to determine what buttons to add
else {
    addLoginButton();
    addRegButton();
}