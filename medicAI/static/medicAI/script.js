$(document).ready(function() {
    console.log("jello")

    $(".list-group-item-action").click(function(){
        $(this).find(".panel").slideToggle("slow");
    });


    $('.my-button').click(function() {
        console.log("clicking buttons");
        var test = "heyo"; // Get the text of the clicked li
        // Send the test data to the backend
        fetch('/add-test/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Assuming you have a function to get CSRF token
            },
            body: JSON.stringify({
                'test': test
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Handle success response if needed
            console.log('Test added to backend:', test);
        })
        .catch(error => {
            // Handle error response if needed
            console.error('Error:', error);
        });
    });
});

// Function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
