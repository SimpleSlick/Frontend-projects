/* ---------- SHAPES ---------- */
const shapes = [
  [[1, 1, 1, 1]],
  [
    [1, 0, 0],
    [1, 1, 1],
  ],
  [
    [0, 0, 1],
    [1, 1, 1],
  ],
  [
    [1, 1],
    [1, 1],
  ],
  [
    [0, 1, 1],
    [1, 1, 0],
  ],
  [
    [1, 1, 0],
    [0, 1, 1],
  ],
  [
    [0, 1],
    [1, 0],
  ],
  [
    [1, 1],
    [1, 0],
  ],
  [
    [0, 1, 0],
    [1, 1, 1],
  ],
];

const colors = [
  "#000",
  "#E7ECEF",
  "#EF8A17",
  "#EF2917",
  "#034732",
  "#540D6E",
  "#172A3A",
  "#550527",
  "#688E26",
  "#02182B",
];

/* ---------- CONFIG ---------- */
const rows = 16;
const cols = 10;
const BLOCK_SIZE = 30;

let score = 0;
let isGameOver = false;

/* ---------- CANVAS ---------- */
const canvas = document.getElementById("tetris");
const ctx = canvas.getContext("2d");
ctx.scale(BLOCK_SIZE, BLOCK_SIZE);

const nextCanvas = document.getElementById("next");
const nextCtx = nextCanvas.getContext("2d");
nextCtx.scale(BLOCK_SIZE, BLOCK_SIZE);

const scoreBoard = document.getElementById("score");

/* ---------- GAME OVER UI ---------- */
const gameOverPanel = document.getElementById("gameOverPanel");
const finalScoreText = document.getElementById("finalScore");
const restartBtn = document.getElementById("restartBtn");

/* ---------- GRID ---------- */
function generateGrid() {
  return Array.from({ length: rows }, () => Array(cols).fill(0));
}

let grid = generateGrid();

/* ---------- PIECES ---------- */
let current = null;
let nextPiece = createPiece();

function createPiece() {
  const index = Math.floor(Math.random() * shapes.length);
  return {
    piece: shapes[index],
    x: Math.floor(cols / 2) - 1,
    y: 0,
    color: index + 1,
  };
}

/* ---------- GAME LOOP ---------- */
let dropCounter = 0;
let dropInterval = 400;
let lastTime = 0;

function update(time = 0) {
  if (isGameOver) return;

  const delta = time - lastTime;
  lastTime = time;
  dropCounter += delta;

  if (dropCounter > dropInterval) {
    drop();
    dropCounter = 0;
  }

  draw();
  requestAnimationFrame(update);
}
update();

/* ---------- DRAW ---------- */
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  grid.forEach((row, y) => {
    row.forEach((value, x) => {
      if (value) {
        ctx.fillStyle = colors[value];
        ctx.fillRect(x, y, 1, 1);
      }
    });
  });

  drawPiece(current);
}

function drawPiece(piece) {
  if (!piece) return;
  piece.piece.forEach((row, y) => {
    row.forEach((value, x) => {
      if (value) {
        ctx.fillStyle = colors[piece.color];
        ctx.fillRect(piece.x + x, piece.y + y, 1, 1);
      }
    });
  });
}

/* ---------- NEXT ---------- */
function drawNext() {
  nextCtx.clearRect(0, 0, nextCanvas.width, nextCanvas.height);
  nextPiece.piece.forEach((row, y) => {
    row.forEach((value, x) => {
      if (value) {
        nextCtx.fillStyle = colors[nextPiece.color];
        nextCtx.fillRect(x + 1, y + 1, 1, 1);
      }
    });
  });
}

/* ---------- MOVEMENT ---------- */
function drop() {
  if (!current) {
    current = nextPiece;
    nextPiece = createPiece();
    drawNext();
    return;
  }

  if (!collide(current, 0, 1)) {
    current.y++;
  } else {
    merge();

    // ✅ GAME OVER (overlay, not alert)
    if (current.y === 0) {
      isGameOver = true;
      finalScoreText.textContent = score;
      gameOverPanel.classList.remove("hidden");
      return;
    }

    clearLines();
    current = null;
  }
}

/* ---------- COLLISION ---------- */
function collide(piece, dx, dy, shape = piece.piece) {
  for (let y = 0; y < shape.length; y++) {
    for (let x = 0; x < shape[y].length; x++) {
      if (shape[y][x]) {
        const nx = piece.x + x + dx;
        const ny = piece.y + y + dy;

        if (nx < 0 || nx >= cols || ny >= rows) return true;
        if (ny >= 0 && grid[ny][nx]) return true;
      }
    }
  }
  return false;
}

/* ---------- MERGE ---------- */
function merge() {
  current.piece.forEach((row, y) => {
    row.forEach((value, x) => {
      if (value) {
        grid[current.y + y][current.x + x] = current.color;
      }
    });
  });
}

/* ---------- CLEAR ---------- */
function clearLines() {
  let cleared = 0;

  outer: for (let y = rows - 1; y >= 0; y--) {
    for (let x = 0; x < cols; x++) {
      if (!grid[y][x]) continue outer;
    }
    grid.splice(y, 1);
    grid.unshift(Array(cols).fill(0));
    cleared++;
    y++;
  }

  if (cleared) {
    score += cleared * 10;
    scoreBoard.textContent = score;
  }
}

/* ---------- CONTROLS ---------- */
document.addEventListener("keydown", (e) => {
  if (!current || isGameOver) return;

  if (e.code === "ArrowLeft" && !collide(current, -1, 0)) current.x--;
  if (e.code === "ArrowRight" && !collide(current, 1, 0)) current.x++;
  if (e.code === "ArrowDown") drop();
  if (e.code === "ArrowUp") rotate();
});

function rotate() {
  const rotated = current.piece[0].map((_, i) =>
    current.piece.map((row) => row[i]).reverse()
  );

  if (!collide(current, 0, 0, rotated)) {
    current.piece = rotated;
  }
}

/* ---------- RESTART ---------- */
restartBtn.addEventListener("click", () => {
  grid = generateGrid();
  score = 0;
  scoreBoard.textContent = score;

  current = null;
  nextPiece = createPiece();
  drawNext();

  isGameOver = false;
  gameOverPanel.classList.add("hidden");

  dropCounter = 0;
  lastTime = 0;
  update();
});
