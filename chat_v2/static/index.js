// chat/static/index.js

console.log("Sanity check from index.js.");

// focus 'roomInput' when user opens the page
document.querySelector("#roomInput").focus();

// submit if the user presses the enter key
document.querySelector("#roomInput").onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter key
        document.querySelector("#roomConnect").click();
    }
};

// Select the radio buttons container
const checkboxContainer = document.querySelector('.checkbox-container');
let selectedValue = 'sync'

// Add event listener for changes to the radio buttons
checkboxContainer.addEventListener('change', function(event) {
    // Check if the changed element is a radio button
    if (event.target.type === 'radio') {
        // Retrieve the selected value
        selectedValue = event.target.value;
        
        // Print the selected value
        console.log('Selected consumer type:', selectedValue);
    }
});

// Function to handle redirection based on selected value and room name
function redirectToPath(selectedValue, roomName) {
    if (selectedValue === 'sync') {
        return "chat_v2/" + roomName + "/";
    } else if (selectedValue === 'async') {
        return "chat_v2/" + roomName + "/";
    }
}

// redirect to '/room/<roomInput>/'
document.querySelector("#roomConnect").onclick = function() {
    console.log('NEW: Selected consumer type:', selectedValue);

    let roomName = document.querySelector("#roomInput").value;
    // window.location.pathname = "chat_v2/" + roomName + "/";
    // Redirect to the constructed path using the reusable function
    window.location.pathname = redirectToPath(selectedValue, roomName);
}

// redirect to '/room/<roomSelect>/'
document.querySelector("#roomSelect").onchange = function() {
    console.log('Existing: Selected consumer type:', selectedValue);

    let roomName = document.querySelector("#roomSelect").value.split(" (")[0];
    // window.location.pathname = "chat_v2/" + roomName + "/";
    // Redirect to the constructed path using the reusable function
    window.location.pathname = redirectToPath(selectedValue, roomName);
}