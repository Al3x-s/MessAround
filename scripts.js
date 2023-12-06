const canvas = document.getElementById("myCanvas");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = 1920

const SCREEN_WIDTH = canvas.width;
const SCREEN_HEIGHT = canvas.height;
const DOT_SIZE = 6;
const DOT_COLOR = "black";
const LINE_COLOR = "black";
const MAX_CONNECTION_DISTANCE = 150;

function randomPosition() {
    return {
        x: Math.random() * SCREEN_WIDTH,
        y: Math.random() * SCREEN_HEIGHT,
    };
}

function distance(point1, point2) {
    const { x: x1, y: y1 } = point1;
    const { x: x2, y: y2 } = point2;
    return Math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2);
}

const dots = Array.from({ length: 110 }, () => ({
    pos: randomPosition(),
    velocity: [
        Math.random() * (Math.random() > 0.5 ? 1 : -1),
        Math.random() * (Math.random() > 0.5 ? 1 : -1),
    ],
}));

function draw() {
    ctx.clearRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);

    dots.forEach((dot) => {
        const { x, y } = dot.pos;

        ctx.beginPath();
        ctx.arc(x, y, DOT_SIZE, 0, 2 * Math.PI);
        ctx.fillStyle = DOT_COLOR;
        ctx.fill();
        ctx.closePath();

        dot.pos.x += dot.velocity[0];
        dot.pos.y += dot.velocity[1];

        if (dot.pos.x < 0 || dot.pos.x > SCREEN_WIDTH) {
            dot.velocity[0] *= -1;
        }
        if (dot.pos.y < 0 || dot.pos.y > SCREEN_HEIGHT) {
            dot.velocity[1] *= -1;
        }

        for (const otherDot of dots) {
            if (dot !== otherDot) {
                const dist = distance(dot.pos, otherDot.pos);
                if (dist < MAX_CONNECTION_DISTANCE) {
                    ctx.beginPath();
                    ctx.moveTo(x, y);
                    ctx.lineTo(otherDot.pos.x, otherDot.pos.y);
                    ctx.strokeStyle = LINE_COLOR;
                    ctx.lineWidth = 1;
                    ctx.stroke();
                    ctx.closePath();
                }
            }
        }
    });

    requestAnimationFrame(draw);
}

draw();