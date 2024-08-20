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
        "WineStopper": "static/imgs/product_types/bookend10x10x10cm.JPG",
        "Magnet": "static/imgs/product_types/magnet_image.jpg",
        "Ornament": "static/imgs/product_types/ornament_image.jpg",
        "RustHook": "static/imgs/product_types/rust_hook_image.jpg",
        "WallTrivet": "static/imgs/product_types/wall_trivet_image.jpg",
        "TrivetWithCork": "static/imgs/product_types/trivet_with_cork_image.jpg"
    };

    // Get the image element
    var productImage = document.getElementById("product_image");

    // Check if the selected product type is "Coasters"
    if (selectedProductType === "Coasters") {
        // Hide the image if "Coasters" is selected
        productImage.style.display = "none";
    } else {
        // Show the image if a different product type is selected
        if (imageMap[selectedProductType]) {
            productImage.src = imageMap[selectedProductType];
            productImage.style.display = "block"; // Make the image visible
        } else {
            productImage.style.display = "none"; // Hide the image if no matching product type
        }
    }
}
