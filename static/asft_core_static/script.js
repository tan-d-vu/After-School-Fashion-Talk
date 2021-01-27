function searchFunction() {
    var input, filter, ul, option, i, txtValue;
    input = document.getElementById("query");
    filter = input.value.toUpperCase();
    ul = document.getElementById("id_favorite_designers");
    option = ul.getElementsByTagName("li");

    if (filter.length == 0) {
        ul.style.display = "none";
    } else {
        ul.style.display = "block";
        let found = 0;

        for (i = 0; i < option.length; i++) {
            txtValue = option[i].textContent || option[i].innerText;

            /* Limit to showing 10 results */
            if (txtValue.toUpperCase().indexOf(filter) > -1 && found < 10) {
                option[i].style.display = "";
                found++;
            } else {
                option[i].style.display = "none";
            }
        }
    }
}


window.addEventListener("click", function() {
    /* If clicked on the label, add to list */
    if (event.target.tagName == "LABEL") {
        let elementClassList = event.target.classList;
        /* If already selected, remove from the list */
        if (elementClassList.contains("selected")) {
            elementClassList.remove("selected");
            document.querySelector("#selected-" + event.target.getAttribute("for")).remove();

        }
        /* If not already selected, add to list */
        else {
            /* Add .selected to its class */
            event.target.classList.add("selected");

            let designerId = event.target.getAttribute("for");

            /* Create desginer's button */
            let selectedDesignerButton = document.createElement('button');
            let selectedButtonId = "selected-" + designerId;
            selectedDesignerButton.innerText = event.target.innerText;

            selectedDesignerButton.setAttribute('id', selectedButtonId);

            /* Clicking the button removes the designer */
            selectedDesignerButton.onclick = function() {
                /* Removing .selected from class and uncheck */
                document.querySelector("[for='" + designerId + "']").classList.remove("selected");
                document.querySelector("#" + designerId).checked = false;

                /* Removing the selectedDesignerButton */
                document.querySelector("#" + selectedButtonId).remove();
            }

            document.getElementById("selected_designers").appendChild(selectedDesignerButton);

        }
    }
})


function closeNav() {
    document.getElementById("menu").style.width = "0";
    document.getElementById("menuContainer").style.width = "0";

}
window.addEventListener("click", function(event) {
    if (event.target == document.getElementById("menuContainer")) {
        document.getElementById("menu").style.width = "0";
        document.getElementById("menuContainer").style.width = "0";
    }
});


let menuButton = document.getElementById("menu-button");
menuButton.addEventListener("click", function() {
    document.getElementById("menu").style.width = "33.333333333%";
    document.getElementById("menuContainer").style.width = "100%";
});