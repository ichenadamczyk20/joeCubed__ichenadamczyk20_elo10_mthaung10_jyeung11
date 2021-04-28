var addLoadButton = function() {
    let div = document.getElementById("loadMoreButtonGoesHere");
    let loadBtn = document.createElement("form");
    loadBtn.setAttribute("action", "/loadMoreDogs");
    loadBtn.setAttribute("method", "POST");
    loadBtn.innerHTML = '<input name="load" type="submit" value="Load More Dogs"/>';
    div.appendChild(loadBtn);
}

console.log(isDogs);
if (isDogs) {
    addLoadButton();
}