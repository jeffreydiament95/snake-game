const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const gridSize = 16;
let gameOver = false;

let snake = [
    {x: gridSize * 10, y: gridSize * 10},
];
let dx = gridSize;
let dy = 0;

let food = {
    x: gridSize * 5,
    y: gridSize * 5,
};

function update() {
    if (gameOver) {
        return;
    }

    const head = {x: snake[0].x + dx, y: snake[0].y + dy};

    if (head.x === food.x && head.y === food.y) {
        food.x = Math.floor(Math.random() * canvas.width / gridSize) * gridSize;
        food.y = Math.floor(Math.random() * canvas.height / gridSize) * gridSize;
    } else {
        snake.pop();
    }

    snake.unshift(head);

    if (head.x < 0 || head.x >= canvas.width || head.y < 0 || head.y >= canvas.height || snake.slice(1).some(segment => segment.x === head.x && segment.y === head.y)) {
        gameOver = true;
    }
}

function draw() {
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = 'lime';
    for (const segment of snake) {
        ctx.fillRect(segment.x, segment.y, gridSize - 1, gridSize - 1);
    }

    ctx.fillStyle = 'red';
    ctx.fillRect(food.x, food.y, gridSize, gridSize);

    if (gameOver) {
        drawGameOver();
    }
}

document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowUp' && dy === 0) {
        dx = 0;
        dy = -gridSize;
    } else if (e.key === 'ArrowDown' && dy === 0) {
        dx = 0;
        dy = gridSize;
    } else if (e.key === 'ArrowLeft' && dx === 0) {
        dx = -gridSize;
        dy = 0;
    } else if (e.key === 'ArrowRight' && dx === 0) {
        dx = gridSize;
        dy = 0;
    }
});

function drawGameOver() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.75)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.font = '24px sans-serif';
    ctx.fillStyle = 'red';
    ctx.textAlign = 'center';
    ctx.fillText('GAME OVER, LOSER', canvas.width / 2, canvas.height / 2 - 50);

    ctx.fillStyle = 'white';
    ctx.fillText('Replay', canvas.width / 2, canvas.height / 2 + 50);
    ctx.fillText('Quit', canvas.width / 2, canvas.height / 2 + 100);
}

function handleClick(x, y) {
    if (!gameOver) {
        return;
    }

    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;

    if (x >= centerX - 50 && x <= centerX + 50) {
        if (y >= centerY && y <= centerY + 50) {
            gameOver = false;
            snake = [{x: gridSize * 10, y: gridSize * 10}];
            dx = gridSize;
            dy = 0
        } else if (y >= centerY + 50 && y <= centerY + 100) {
            window.close();
        }
    }
}

canvas.addEventListener('click', (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    handleClick(x, y);
});

function loop() {
    update();
    draw();
    setTimeout(loop, 1000 / 15);
}

loop();
