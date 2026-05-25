let boxes = document.querySelectorAll(".box");
let resetBtn = document.querySelector("#reset");
let ruleBtn = document.querySelector("#rule");
let themeBtn = document.querySelector("#theme");
let newgameBtn = document.querySelector("#new-game");
let msgContainer = document.querySelector(".msg-container");
let msg = document.querySelector(".msg");
let rulePanel = document.querySelector("#rulesPanel");
let clsBtn = document.querySelector("#closeRule");
let header = document.querySelector("header");
let header_text = document.querySelector(".head_text");
let gameBox = document.querySelector(".game_box");
let ruleContent = document.querySelector(".rules-content");
let body = document.querySelector("body");

let playerX = true;

const winningPatterns = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],
  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8],
  [0, 4, 8],
  [2, 4, 6],
];

boxes.forEach((box) => {
  box.addEventListener("click", () => {
    if (playerX) {
      // *player x to play
      box.innerText = "X";
      playerX = false;
    } else {
      // *player o to play
      box.innerText = "O";
      playerX = true;
    }

    box.disabled = true;

    chkWinner();
  });
});

const disableBoxes = () => {
  for (let box of boxes) {
    box.disabled = true;
  }
};

const enableBoxes = () => {
  for (let box of boxes) {
    box.disabled = false;
    box.innerText = "";
  }
};

const showWinner = (winner) => {
  msg.innerText = `Winner is: ${winner}`;
  msgContainer.classList.remove("hide");
  disableBoxes();
};
const chkWinner = () => {
  for (let pattern of winningPatterns) {
    let pos1val = boxes[pattern[0]].innerText;
    let pos2val = boxes[pattern[1]].innerText;
    let pos3val = boxes[pattern[2]].innerText;

    if (pos1val != "" && pos2val != "" && pos3val != "") {
      if (pos1val == pos2val && pos2val == pos3val) {
        showWinner(pos1val);
      }
    }
  }
};

newgameBtn.addEventListener("click", () => {
  msgContainer.classList.add("hide");
  enableBoxes();
  playerX = true;
});

resetBtn.addEventListener("click", () => {
  msgContainer.classList.add("hide");
  enableBoxes();
  playerX = true;
});

// ? open rule panel
ruleBtn.addEventListener("click", () => {
  rulePanel.style.display = "flex";
});

clsBtn.addEventListener("click", () => {
  rulePanel.style.display = "none";
});

let themeState = 0;

themeBtn.addEventListener("click", () => {
  msgContainer.classList.add("hide"); // hides before theme override
  themeState++;

  if (themeState === 1) {
    body.className = "frostbite";
  } else if (themeState === 2) {
    body.className = "cyberArcade";
  } else {
    body.className = "";
    themeState = 0;
  }
});
