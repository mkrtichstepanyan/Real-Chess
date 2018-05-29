let board, game;
let socket;
let sid;
let token = x;

socket = io.connect("http://192.168.16.100:8000/");

socket.on('connect', function () {
    sid = socket.id;
    socket.emit("getGame", {"token": token, "sid": sid});
    document.getElementById("copyDiv").innerHTML = "<button onclick='leave()'>Leave</button>";
    document.getElementById("copyDiv").style.display = "block";

});

socket.on("sendGame", function (serverGame) {
    game = new Chess();

});
socket.on("move", function (move) {
    game.move(move);
    board.position(game.fen());
});

socket.on('redirect', function (data) {
    window.location = data.url;
});

function leave() {
    socket.emit("leave", token)
}

// do not pick up pieces if the game is over
// only pick up pieces for the side to move
let onDragStart = function (source, piece, position, orientation) {
    if (game.turn() === "w") {
        return false;
    }
    if (game.game_over() === true ||
        (game.turn() === 'w' && piece.search(/^b/) !== -1) ||
        (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
        return false;
    }
};

let onDrop = function (source, target) {
    // see if the move is legal
    let move = game.move({
        from: source,
        to: target,
        promotion: 'q' // NOTE: always promote to a queen for example simplicity
    });

    // illegal move

    if (move === null) {
        return "snapback";
    } else {
        let data = {"move": move, "sid": sid, "token": token};
        console.log(data);
        socket.emit('move', data);

    }

};

// update the board position after the piece snap
// for castling, en passant, pawn promotion
let onSnapEnd = function () {
    board.position(game.fen());
};


let cfg = {
    draggable: true,
    position: 'start',
    onDragStart: onDragStart,
    onDrop: onDrop,
    onSnapEnd: onSnapEnd,

};
board = ChessBoard('gameBoard', cfg);
board.flip();


