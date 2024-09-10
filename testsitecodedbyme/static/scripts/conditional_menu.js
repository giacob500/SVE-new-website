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

function updateProductImage() {
    // Get the selected product type
    var selectedProductType = document.getElementById("product_type").value;
    
    // Define the image source based on the selected product type
    var imageMap = {
        "Coasters": "static/imgs/product_types/coaster.jpg",
        "WineStopper": "static/imgs/product_types/bookend10x10x10cm.jpg",
        "Magnet": "static/imgs/product_types/magnet.jpg",
        "Paperweight": "static/imgs/product_types/paperweight.jpg",
        "RustHook": "static/imgs/product_types/hook.jpg",
        "TripleHook": "static/imgs/product_types/triple_hook.jpg",
        "PotSticker": "static/imgs/product_types/pot_sticker.jpg"
    };

    // Get the image element
    var productImage = document.getElementById("product_image");

    
    // Show the image if a different product type is selected
    if (imageMap[selectedProductType]) {
        productImage.src = imageMap[selectedProductType];
        productImage.style.display = "block"; // Make the image visible
    } else {
        productImage.style.display = "none"; // Hide the image if no matching product type
    }
    
}
