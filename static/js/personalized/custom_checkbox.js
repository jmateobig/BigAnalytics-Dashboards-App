function filterCheckboxes(name) {
    var input, filter, container, checkboxes, label, i;
    input = document.querySelector(`input[name="${name}"].search-input`);
    filter = input.value.toUpperCase();
    container = document.querySelector(`div.checkbox-list`);
    checkboxes = container.getElementsByClassName('form-check');
    
    for (i = 0; i < checkboxes.length; i++) {
        label = checkboxes[i].getElementsByTagName("label")[0];
        if (label) {
            if (label.innerHTML.toUpperCase().indexOf(filter) > -1) {
                checkboxes[i].style.display = "";
            } else {
                checkboxes[i].style.display = "none";
            }
        }       
    }
}