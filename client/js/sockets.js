var ws = new WebSocket("ws://96.239.90.68:25565");

ws.onmessage = function(event) {
    console.log(event);
    //$.getScript("js/game.js")
};

function login() {
    user = $('[name="user"]')[0].value;
    pass = $('[name="passwd"]')[0].value;

    data =  JSON.stringify( {"login": {"user": user, "pass": pass}} );
    ws.send(data);
}
