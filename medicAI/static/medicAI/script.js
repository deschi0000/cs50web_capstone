$(document).ready(function() {
    console.log("jello");

    $(".list-group-item-action").click(function(){
        $(this).find(".panel").slideToggle("slow");
    });

    // Prevent the panel from closing when clicking on links inside the panel
    $(".panel a").click(function(event){
        event.stopPropagation(); // Prevent event bubbling
    });

    // To delete tests in the database on the edit patient page
    $('.btn.btn-primary.btn-sm.test-delete').click(function(e) {
        e.preventDefault();
        e.stopPropagation();
        console.log("trying to delete a test!");

        console.log(e.target.parentElement)
        // Hide the element that was clicked
        var test;
        if (e.target.parentElement.tagName == "LI"){
            console.log('it is a list item')
            e.target.parentElement.style.display = 'none';
            test = e.target.parentElement.innerText;
        } else if (e.target.parentElement.tagName =="BUTTON") {
            console.log('it is a button')
            e.target.parentElement.parentElement.style.display = 'none';
            test = e.target.parentElement.parentElement.innerText;
        }
        // e.target.style.display = 'none';

        console.log(`The test:${test}`);
        fetch('/delete-test-edit-page/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
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
            console.log("I have a reponse!");
            console.log(data);
        })
        .catch(error => {
            // Handle error response if needed
            console.error('Error:', error);
        });

    });

    // To add or remove tests from the diagnosis page
    $('.test-item').click(function(e) {
        e.stopPropagation();
        // console.log("clicking buttons");

        // var test = "heyo"; // Get the text of the clicked li
        var test = e.target.innerText;
        // Send the test data to the backend
        fetch('/add-test/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
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
            console.log("I have a reponse!");
            console.log(data);
            // Toggle the clicked class
            if (!$(e.target).hasClass("clicked")) {
                // Add CSS class to change color
                $(e.target).addClass("clicked");
            } else {
                $(e.target).toggleClass("clicked");
            }

            // Toggle the plus/minus icon
            if ($(e.target).find('i.fa-solid').hasClass('fa-plus')) {
                $(e.target).find('i.fa-solid').removeClass('fa-plus').addClass('fa-minus');
                showNotification("Test added");
            } else {
                $(e.target).find('i.fa-solid').removeClass('fa-minus').addClass('fa-plus');
                showNotification("Test removed");
            }
            // console.log('Test added to backend:', test);
            // console.log("changing class!");


            // $(e.target).toggleClass("clicked");
            // if (!$(e.target).hasClass("clicked")) {
            //     // Add CSS class to change color
            //     $(e.target).addClass("clicked");
            // }
        })
        .catch(error => {
            // Handle error response if needed
            console.error('Error:', error);
        });
    });
    // Function to show notification bar
    function showNotification(message) {
        console.log("trying to show notification!");
        var notificationBar = $('.alert').text(message);
        notificationBar.removeAttr('hidden'); // Remove the 'hidden' attribute

        // After 3 seconds, fade out and remove the notification bar
        setTimeout(function() {
            notificationBar.attr('hidden', true); // Add the 'hidden' attribute back
        }, 2000);
    }
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

