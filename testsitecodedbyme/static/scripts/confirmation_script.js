// Code below regulates behaviour of pop-up confirmation message in basket page

function showConfirmation() {
    var result = confirm("Are you sure you want to continue?");
    return result;
}

function showConfirmation(message) {
    var result = confirm(message);
    return result;
}