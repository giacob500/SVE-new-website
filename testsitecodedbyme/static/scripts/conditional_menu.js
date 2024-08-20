function showOptions() {
    var productType = document.getElementById("product_type").value;
    var additionalOptions = document.getElementById("additional_options");

    if (productType === "Coasters 10x10 cm" || productType === "Coasters 15x15 cm") {
        // Show the additional options dropdown when 10x10 or 15x15 is selected
        additionalOptions.style.display = "block";
    } else {
        // Hide the additional options for magnets (5x5 cm)
        additionalOptions.style.display = "none";
    }
}
