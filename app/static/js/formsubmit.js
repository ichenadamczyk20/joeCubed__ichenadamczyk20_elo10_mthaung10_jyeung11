function submitThis(form) {
    if (window.XMLHttpRequest) {
        //Firefox, Opera, IE7, and other browsers will use the native object
        var xhttp = new XMLHttpRequest();
    } else {
        //IE 5 and 6 will use the ActiveX control
        var xhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    var submitButton = form.querySelector('[type=submit]'); //finds the submit button to disable it so people can't spam the form
    submitButton.disabled = true;
    xhttp.onreadystatechange = function() { //handles the response from the submit target
        //var json = JSON.parse(xhttp.responseText)
        document.querySelector('#thingGoesHere').innerHTML = xhttp.responseText;
        submitButton.disabled = false;
    };
    xhttp.open(form.method, form.action, true); //sends form to the form action by form method
    var data = new FormData(form); //gets the form's data
    xhttp.send(data); //sends the form's data
};

function submitThisFavorite(form) {
    if (window.XMLHttpRequest) {
        //Firefox, Opera, IE7, and other browsers will use the native object
        var xhttp = new XMLHttpRequest();
    } else {
        //IE 5 and 6 will use the ActiveX control
        var xhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    var submitButton = form.querySelector('[type=submit]'); //finds the submit button to disable it so people can't spam the form
    submitButton.disabled = true;
    //the readystatechange fxn is redefined here. when flask returns a new value, this fxn gets triggered.
    console.log("submitting")
    xhttp.onreadystatechange = function() { //handles the response from the submit target
        if (this.readyState === this.DONE) {
            var response = xhttp.responseText;
            console.log(response)
            if (response == "unfavorited") submitButton.value = "Favorite 💕";
            if (response == "favorited") submitButton.value = "Unfavorite 💔"
            submitButton.disabled = false;
        }
    };
    xhttp.open(form.method, form.action, true); //sends form to the form action by form method
    var data = new FormData(form); //gets the form's data
    xhttp.send(data); //sends the form's data
};

function submitThisWiki(form) {
    if (window.XMLHttpRequest) {
        //Firefox, Opera, IE7, and other browsers will use the native object
        var xhttp = new XMLHttpRequest();
    } else {
        //IE 5 and 6 will use the ActiveX control
        var xhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    var submitButton = form.querySelector('[type=submit]'); //finds the submit button to disable it so people can't spam the form
    submitButton.disabled = true;
    xhttp.onreadystatechange = function() { //handles the response from the submit target
        if (this.readyState === this.DONE) {
            document.querySelector('#wikiImage').src = xhttp.responseText.split("!!!")[0];
            document.querySelector('#wikiTitle').innerHTML = xhttp.responseText.split("!!!")[1];
            submitButton.disabled = false;
        }
    };
    xhttp.open(form.method, form.action, true); //sends form to the form action by form method
    var data = new FormData(form); //gets the form's data
    xhttp.send(data); //sends the form's data
};