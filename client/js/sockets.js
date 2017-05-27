var ws = new WebSocket("ws://96.239.90.68:25565");

ws.onmessage = function(event) {
    console.log(event);
    if (event.data == '{"auth": false}') return false;
    if (event.data == '{"auth": true}') startGame();
};

ws.onopen = function(event) {
    console.log("connected");
}

function onSignIn(googleUser) {
    console.log("signed in");
    ws.send(JSON.stringify( {"login":googleUser.getAuthResponse().id_token}) );
}

function startGame() {
    $.getScript("js/game.js");
    $(".g-signin2").hide();
}
