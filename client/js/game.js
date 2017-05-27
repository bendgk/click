PIXI.settings.SCALE_MODE = PIXI.SCALE_MODES.NEAREST;

var Application = PIXI.Application,
    Container = PIXI.Container,
    autoDetectRenderer = PIXI.autoDetectRenderer,
    loader = PIXI.loader,
    resources = PIXI.loader.resources,
    Sprite = PIXI.Sprite;
    TilingSprite = PIXI.extras.TilingSprite;

var app = new Application($(window).width() - 20, $(window).height() - 20, { backgroundColor: 0xAAAAAA });

window.onresize = function (event) {
    app.view.width = $(window).width() - 20;
    app.view.height = $(window).height() - 20;
};
document.body.appendChild(app.view);

var main = TilingSprite.fromImage('res/square.png');

main.anchor.set(0.5);
main.x = 0; main.y = 0;
app.stage.x = app.view.width / 2; app.stage.y = app.view.height / 2;

main.interactive = true;
main.buttonMode = true;

main
    .on('pointerdown', startDrag)
    .on('pointerup', endDrag)
    .on('pointerupoutside', endDrag)
    .on('pointermove', moveDrag);

app.stage.addChild(main);

function click() {
    main.width += 10; main.height += 10;
    ws.send(JSON.stringify( {"click":"1"} ) );
}

function startDrag(event) {
    click();

    this.data = event.data;
    this.dragging = true;

    this.initStagePosition = app.stage.position;
    this.initMousePosition = this.data.getLocalPosition(this.parent);
}

function endDrag() {
    this.data = null;
    this.dragging = false;
}

function moveDrag() {
    if (this.dragging) {
        var dx = this.initMousePosition.x - this.data.getLocalPosition(this.parent).x,
            dy = this.initMousePosition.y + this.data.getLocalPosition(this.parent).y;

        var newX = this.initStagePosition.x + dx/3,
            newY = this.initStagePosition.y + dy/3;

        if (main.width > app.view.width) app.stage.position.x = (newX < main.width / 2 && newX > app.view.width - main.width / 2) ? newX : app.stage.position.x;
        if (main.height > app.view.height) app.stage.position.y = (newY < main.height / 2 && newY > app.view.height - main.height / 2) ? newY : app.stage.position.y;

        this.initMousePosition = this.data.getLocalPosition(this.parent);
    }
}
