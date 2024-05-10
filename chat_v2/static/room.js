// chat/static/room.js

console.log("Sanity check from room.js.");
const roomName = JSON.parse(document.getElementById('roomName').textContent);

let chatLog = document.querySelector("#chatLog");
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");
let onlineUsersSelector = document.querySelector("#onlineUsersSelector");
let chatSocket = null;
let directory = JSON.parse(document.getElementById('directory'));

// adds a new option to 'onlineUsersSelector'
function onlineUsersSelectorAdd(value) {
    if (document.querySelector("option[value='" + value + "']")) return;
    let newOption = document.createElement("option");
    newOption.value = value;
    newOption.innerHTML = value;
    onlineUsersSelector.appendChild(newOption);
}

// removes an option from 'onlineUsersSelector'
function onlineUsersSelectorRemove(value) {
    let oldOption = document.querySelector("option[value='" + value + "']");
    if (oldOption !== null) oldOption.remove();
}

// focus 'chatMessageInput' when user opens the page
chatMessageInput.focus();

// submit if the user presses the enter key
chatMessageInput.onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter key
        chatMessageSend.click();
    }
};

// clear the 'chatMessageInput' and forward the message
chatMessageSend.onclick = function() {
    if (chatMessageInput.value.length === 0) return;
    if (directory === '' || directory === null) directory = './'
    chatSocket.send(JSON.stringify({
        "message": chatMessageInput.value,
        "channel": roomName,
        "command": chatMessageInput.value,
        "directory": directory,
    }));

    console.log('sending message: '+chatMessageInput.value+" to channel: "+roomName+" and command: "+chatMessageInput.value+" Current Directory: "+directory)
    chatMessageInput.value = "";
};

// Function to set the directory selection window
const setDirectorySelectionWindow = async () => {
    console.log('Select Server side folder');
    // alert("Implement logic to set directory interface");
    directory = document.getElementById('setDirectory').value;
    console.log("Selected directory:", directory);
   
};

// Attach click event listener to the set directory button
const setDirectoryBtn = document.getElementById('setDirectoryBtn');
// Attach click event listener to the select directory button
setDirectoryBtn.addEventListener('click', setDirectorySelectionWindow);

function connect() {
    console.log('checking host: '+window.location.host+" room name: "+roomName)

    chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat_v2/'
        + roomName
        + '/'
    );

    chatSocket.onopen = function(e) {
        console.log("Successfully connected to the WebSocket.");
    }

    chatSocket.onclose = function(e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    };

    chatSocket.onmessage = function(e) {
        try {
            const data = JSON.parse(e.data);
            // console.log(data);

            switch (data.type) {
                case "chat_message":
                    chatLog.value += "> " + data.message + "\n";
                    chatLog.value += data.results + "\n";
                    chatLog.value += "Time taken: " + data.processing_time.toFixed(4) + " seconds\n";
                    break;
                default:
                    console.error("Unknown message type!");
                    break;
            }

            // console.log(chatLog);
        } catch (error) {
            console.error('Error parsing or processing message:', error);
        }
        
        // scroll 'chatLog' to the bottom
        chatLog.scrollTop = chatLog.scrollHeight;
    };

    chatSocket.onerror = function(err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        chatSocket.close();
    }

}
connect();