var ws = new WebSocket("ws://96.239.90.68:25565");

ws.onmessage = function(event) {
    if (event.data == '{"auth": false}') return false;
    console.log(event);
    //$.getScript("js/game.js")
};

ws.onopen = function(event) {
    console.log("connected");
}

function onSignIn(googleUser) {
    console.log("signed in");
    ws.send(JSON.stringify( {"login":googleUser.getAuthResponse().id_token}) );
}
