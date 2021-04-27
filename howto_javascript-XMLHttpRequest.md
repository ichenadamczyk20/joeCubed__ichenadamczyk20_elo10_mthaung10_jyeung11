# how-to :: JavaScript XMLHttpRequest
---
## Overview
After working with HTML forms, you might be wondering if it's possible to send a POST or GET request and get the returned data without reloading the page or going to a different page. The simplest way to do that without jQuery is with JavaScript XMLHttpRequests. This tutorial will go over how to send an XMLHttpRequest with the data in an HTML form (for ease of configuration).

### Estimated Time Cost: 30 minutes

### Prerequisites:

- You'll want some experience with JavaScript to do this.
- You won't need to install anything or include anything in your HTML file to use XMLHttpRequests. 
- To easily convert your form into a JavaScript friendly object to send with XMLHttpRequests, you will probably want to use FormData. FormData is also included automatically with JavaScript.

1. Set up your Flask app to have two endpoints: one that returns the template that renders the form with the JavaScript, and another that returns the data you want. It will probably look like this:
```
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/form-submit')
def handleFormSubmission(json):
    if "input-data" in request.form:
        return "successfully received input: " + request.form["input-data"]
    else:
        return "did not receive input"

if __name__ == '__main__':
    app.run()
```
2. Set up the HTML form. It will be set up almost exactly like how you would set up a normal HTML form, but also with the `onsubmit="..."` part. When the submit button is pressed, the JavaScript code in `onsubmit` will be executed. First, it calls the JavaScript function `submitThis`, sending the DOM object for that HTML form to `submitThis`. Then, `return false` is executed, telling the HTML form not to do the default action it would do when submitted, which is to submit the form and redirect the browser to the URL in `action`.
```
<form action="/form-submit" onsubmit="submitThis(this); return false;" method="POST">
    <input type="text" name="input-data" value="this is the input data sent" required>
    <input type="submit" name="submit" value="send it!"/>
</form>
```

3. Finally, set up the JavaScript functionality by adding this script element. It can go anywhere in your HTML file.
```
<script>
    function submitThis(formElement) {
        var xhttp = new XMLHttpRequest();

        xhttp.onreadystatechange = function() {
            //this function is called when the response is received from the form's endpoint
            responseText = xhttp.responseText; //handle this variable however you like
            //if you want to treat as JSON data, you can use this line
            //var json = JSON.parse(xhttp.responseText)
            console.log("Response received: " + responseText);
        };

        //opens a request to send the data to the URL form.action via form.method
        //note the false at the end of the xhttp.open call
        //if set to true, no javascript code will be run after the form is submitted, until the reponse from the form is returned
        //if set to false, other javascript code will run while the xhttp object waits for the response
        xhttp.open(form.method, form.action, false); 
        
        var data = new FormData(form); //gets the form's data as a FormData object
        xhttp.send(data); //sends the FormData object with the same encoding as an HTML form element would send its data
    }
</script>
```
4. You now have a working Flask app that uses XMLHttpRequest to submit a form without reloading/redirecting! If you worry about support for IE5 or IE6, you can include this code snippet at the beginning of the function in place of `var xhttp = new XMLHttpRequest();`:
```
if (window.XMLHttpRequest) {
    //For Chrome, Firefox, Opera, IE7, and others
    var xhttp = new XMLHttpRequest();
} else {
    //For IE5 and IE6
    var xhttp = new ActiveXObject("Microsoft.XMLHTTP");
}
```


### Resources
* XMLHttpRequest documentation: https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest
* FormData documentation: https://developer.mozilla.org/en-US/docs/Web/API/FormData

---

Accurate as of (last update): 2021-04-27

#### Contributors:  
Ian Chen-Adamczyk, pd1  
Eric Lo, pd1  
Michelle Thaung, pd1  
Jessica Yeung, pd1  
