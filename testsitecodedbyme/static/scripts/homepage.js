const translations = [
    {text: "Place your order here. Don't worry, we will send you a confirmation as usual.", lang: "English"},
    {text: "Effettua il tuo ordine qui. Non preoccuparti, ti invieremo una conferma come al solito.", lang: "Italian"},
    {text: "Passez votre commande ici. Ne vous inquiétez pas, nous vous enverrons une confirmation comme d'habitude.", lang: "French"},
    {text: "Bestellen Sie hier. Keine Sorge, wir senden Ihnen wie gewohnt eine Bestätigung.", lang: "German"}
];

let currentIndex = 0;
const textElement = document.getElementById('text');

function changeText() {
    // Fade out
    textElement.classList.add('fade-out');

    setTimeout(() => {
        // Change text after fade-out
        textElement.innerHTML = translations[currentIndex].text;

        // Fade in
        textElement.classList.remove('fade-out');
        textElement.classList.add('fade-in');

        setTimeout(() => {
            // Move to the next translation after fade-in
            currentIndex = (currentIndex + 1) % translations.length;

            // Wait 3 seconds before starting the next transition
            setTimeout(() => {
                textElement.classList.remove('fade-in');
                changeText();
            }, 3000);
        }, 2000); // Duration of fade-in
    }, 2000); // Duration of fade-out
}

// Start the transition after 3 seconds
setTimeout(changeText, 3000);