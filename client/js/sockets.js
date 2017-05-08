var ws = new WebSocket("ws://96.239.90.68:25565");

ws.onmessage = function(event) {
    console.log(event);
};

ws.onopen = function(event) {
    console.log("closing")
    ws.send("register");
};

function abc() {
    ws.send("click");
    console.log("click");
}