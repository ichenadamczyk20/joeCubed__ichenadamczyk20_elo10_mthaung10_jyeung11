function submitThis(formElement) {
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if (this.readyState === this.DONE) {
            var responseText = xhttp.responseText;
            alert("Response received: " + responseText);
        }
    };

    xhttp.open(formElement.method, formElement.action, false); 
    
    var data = new FormData(formElement);
    xhttp.send(data);
    return false;
}