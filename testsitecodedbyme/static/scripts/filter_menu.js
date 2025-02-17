function applyFilters() {
    let selected = [];
    document.querySelectorAll('#filterForm input[type="checkbox"]:checked').forEach((checkbox) => {
        selected.push(checkbox.value);
    });
    document.getElementById('selectedFilters').textContent = selected.length ? selected.join(', ') : "None";
}