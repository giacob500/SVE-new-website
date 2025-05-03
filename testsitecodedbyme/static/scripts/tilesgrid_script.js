// Code below regulates behaviour of grid selection in product page

window.addEventListener('DOMContentLoaded', (event) => {
    var counter = 0;
    var counterElement = document.getElementById('product_counter');
    var cells = document.getElementsByTagName('td');
    var selectedList = document.getElementById('selectedList');
    var hiddenInput = document.querySelector('input[name="product_counter"]');
    var hiddenInputTiles = document.querySelector('input[name="selected_tiles"]');

    // Initialize with the default value of 4 (all tiles) when the page loads
    hiddenInput.value = 4;

    for (var i = 0; i < cells.length; i++) {
        cells[i].addEventListener('click', function() {
            if (!this.classList.contains('selected')) {
                counter++;
                counterElement.innerText = counter;
                this.classList.add('selected');
                this.classList.add('clicked');
                
                var cellText = this.innerText;
                var listItem = document.createElement('li');
                listItem.innerText = cellText;
                selectedList.appendChild(listItem);
                
            } else {
                counter--;
                counterElement.innerText = counter;
                this.classList.remove('selected');
                this.classList.remove('clicked');
                
                var cellText = this.innerText;
                var listItems = selectedList.getElementsByTagName('li');
                for (var j = 0; j < listItems.length; j++) {
                    if (listItems[j].innerText === cellText) {
                        selectedList.removeChild(listItems[j]);
                        break;
                    }
                }
                
            }
            
            // If no tiles are selected (counter is 0), set product_counter to 4
            // as per the requirement "If you don't select any tiles, all tiles will be included by default"
            if (counter === 0) {
                hiddenInput.value = 4;
            } else {
                hiddenInput.value = counter;
            }
            
            hiddenInputTiles.value = getSelectedTiles();
        });
    }

    function getSelectedTiles() {
        var selectedTiles = [];
        var listItems = selectedList.getElementsByTagName('li');
        for (var i = 0; i < listItems.length; i++) {
            selectedTiles.push(listItems[i].innerText);
        }
        return selectedTiles.join(', ');
    }
});