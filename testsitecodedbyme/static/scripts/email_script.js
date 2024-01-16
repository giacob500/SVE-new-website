// Code below regulates behaviour of email generation in basket page

document.getElementById('emailForm').addEventListener('submit', function (event) {
    event.preventDefault();

    var formElements = document.getElementById('emailForm').elements;
    var bodyContent = '—————————————————\n';
    
    for (var i = 0; i < formElements.length; i++) {
        var element = formElements[i];
        
        if (element.type === 'hidden') {
            bodyContent += element.name + ': ' + element.value + '\n';
            if (element.name === 'Quantity') {
                bodyContent += '\n';
            }
        }
    }

    bodyContent += '—————————————————';

    var name = document.getElementById('name').value;
    var email = document.getElementById('email').value;
    var phone = document.getElementById('phone').value;
    if (document.getElementById('comments').value == ''){
        var comments = null;
    } else {
        var comments = document.getElementById('comments').value;
    }

    var mailtoLink = 'mailto:lorenzi@lorenzi.net?subject=New%20Order%20from%20SVE%20website%20-%20'
    + encodeURIComponent(name) + '&body=Hi%2C%0D%0Aplease%20check%20out%20the%20order%20below%3A%0D%0A%0D%0A' + encodeURIComponent(bodyContent) + '%0D%0A';
    
    if (comments !== null) {
        mailtoLink += 'Additional%20comments%3A%0D%0A' + encodeURIComponent(comments) + '%0D%0A';
    }

    mailtoLink += '%0D%0AMany%20thanks%2C%0D%0A' + encodeURIComponent(name) + '%0D%0A%0D%0A' + encodeURIComponent(email)
    + '%0D%0A' + encodeURIComponent(phone);

    window.location.href = mailtoLink;
});