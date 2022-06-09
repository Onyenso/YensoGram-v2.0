// When the document is loaded
document.addEventListener("DOMContentLoaded", () => {

    // Get friend's username from the DOM
    var friend_username = document.querySelector("#friend_username").innerHTML

    // Load previous messages with friend
    load(friend_username)

    // Check for new messages every second
    setInterval(() => load_latest(friend_username), 1000)

    // Every time the message form is submitted
    // document.querySelector("#message-form").onsubmit = () => send(friend_username)
})





// Function for loading previous messages
function load(friend_username) {
    // Send a request to get messages
    fetch(`/messages_API/${friend_username}`)
    // Turn response to json
    .then(response => response.json())
    
    .then(data => {
        console.log(data)
        var read_messages = data.read_messages
        var unread_messages = data.unread

        // If no read and unread messages, show "No conversation yet"
        if (read_messages.length == 0 && unread_messages.length == 0) {
            document.querySelector("#no-conversation").style.display = "block"
        }
        // If there are read messages
        if (read_messages.length > 0) {
            // For each read message
            read_messages.forEach(read_message => {
                
                div = document.createElement("div")
                div.className = "m-2 row"
                div.innerHTML = `
                                <div class="col-8">
                                    <span class="d-inline-block p-1 messages" id="id${read_message.id}"><a style="text-decoration: none;" data-toggle="modal" data-target="#a${read_message.id}" href="#">${read_message.message}</a></span>
                                    <div style="font-size: xx-small">${read_message.time}</div>
                                </div>
                                
                                
                                <!-- Modal for sent message -->
                                <div class="modal fade" id="a${read_message.id}" tabindex="-1" aria-labelledby="a${read_message.id}Label" aria-hidden="true">
                                    <div class="modal-dialog modal-dialog-centered">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h5 class="modal-title" id="a${read_message.id}Label">Delete Message</h5>
                                                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                                <span aria-hidden="true">&times;</span>
                                                </button>
                                            </div>
                                            <div class="modal-body" style="text-align: left">
                                                ${read_message.message}
                                            </div>
                                            <div class="modal-footer">
                                                <a class="btn btn-primary" href="#">Delete for everyone</a>
                                                <a class="btn btn-primary" href="#">Delete for me</a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                `
                if (read_message.sent == 1) {
                    div.className = "m-2 row justify-content-end"
                    div.style.textAlign = "right"
                }
                else {
                    div.className = "m-2 row justify-content-start"
                    div.style.textAlign = "left"
                }
                if (document.querySelector(`id${read_message.id}`) == null){
                    document.querySelector("#messages").append(div)
                }
            })
        }
    })
}






// Function for loading latest messages
function load_latest(friend_username) {

    // Get messages
    fetch(`/messages_API/${friend_username}`)
    .then(response => response.json())
    .then(data => {

        //console.log(data)
        var unread_messages = data.unread

        // If there are new messages
        if (unread_messages.length > 0) {
            
            // Remove the "No conversation yet" <p>
            document.querySelector("#no-conversation").style.display = "none"
            // For each new message
            unread_messages.forEach(unread_message => {
                
                div = document.createElement("div")
                div.className = "m-2"
                div.style.textAlign = "left"
                div.innerHTML = `<span class="d-inline-block p-1 messages" id="id${unread_message.id}"><a style="text-decoration: none;" data-toggle="modal" data-target="#a${unread_message.id}" href="#">${unread_message.message}</a></span>
                                <div style="font-size: xx-small">${unread_message.time}</div>
                                
                                <!-- Modal for sent message -->
                                <div class="modal fade" id="a${unread_message.id}" tabindex="-1" aria-labelledby="a${unread_message.id}Label" aria-hidden="true">
                                    <div class="modal-dialog modal-dialog-centered">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h5 class="modal-title" id="a${unread_message.id}Label">Delete Message</h5>
                                                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                                <span aria-hidden="true">&times;</span>
                                                </button>
                                            </div>
                                            <div class="modal-body" style="text-align: left">
                                                ${unread_message.message}
                                            </div>
                                            <div class="modal-footer">
                                                <a class="btn btn-primary" href="#">Delete for everyone</a>
                                                <a class="btn btn-primary" href="#">Delete for me</a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                `
                if (document.querySelector(`id${unread_message.id}`) == null) {
                    document.querySelector("#messages").append(div)
                }
            })
        }
    })
}




// Fuction for sending messages
document.addEventListener("DOMContentLoaded", () => {
    // Get friend's username from the DOM
    var friend_username = document.querySelector("#friend_username").innerHTML
    // When the form is submitted
    document.querySelector("#message-form").onsubmit = () => {

        // Get what was typed in
        var message = document.querySelector("#message").value
        // Send the message to the server
        fetch(`/messages_API/${friend_username}`,{
            method: "POST",
            body: JSON.stringify({message: message})
        })
        .then(response => response.json())
        // This data is the message object
        .then(data => {
            console.log(data)
            data = data.message
            var new_div = document.createElement("div")
                    new_div.className = "m-2"
                    new_div.style.textAlign = "right"
                    new_div.innerHTML = `<span class="d-inline-block p-1 messages" id="id${data.id}"><a style="text-decoration: none;" data-toggle="modal" data-target="#a${data.id}" href="#">${data.message}</a></span>
                                    <div style="font-size: xx-small">${data.time}</div>
                                    
                                    <!-- Modal for sent message -->
                                    <div class="modal fade" id="a${data.id}" tabindex="-1" aria-labelledby="a${data.id}Label" aria-hidden="true">
                                        <div class="modal-dialog modal-dialog-centered">
                                            <div class="modal-content">
                                                <div class="modal-header">
                                                    <h5 class="modal-title" id="a${data.id}Label">Delete Message</h5>
                                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                                    <span aria-hidden="true">&times;</span>
                                                    </button>
                                                </div>
                                                <div class="modal-body" style="text-align: left">
                                                    ${data.message}
                                                </div>
                                                <div class="modal-footer">
                                                    <a class="btn btn-primary" href="#">Delete for everyone</a>
                                                    <a class="btn btn-primary" href="#">Delete for me</a>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                    `

            // Clear out field
            document.querySelector("#message").value = ""
            // Remove the "No conversation yet" <p>
            if (document.querySelector("#no-conversation").style.display == "block") {
                document.querySelector("#no-conversation").style.display = "none"
            }
            
            // Add message to DOM
            if (document.querySelector(`id${data.id}`) == null){
                document.querySelector("#messages").append(new_div)
            }
            
        });

        return false
    }
})




