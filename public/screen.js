// This file contains NO game rules. It only
//   1) sends key presses to Python, and
//   2) paints the 96 x 68 frame that Python sends back.

const view = document.getElementById("screen");
const vctx = view.getContext("2d");

const lcd = document.createElement("canvas");      // tiny hidden LCD
lcd.width = CFG.w;
lcd.height = CFG.h;
const lctx = lcd.getContext("2d");
const image = lctx.createImageData(CFG.w, CFG.h);

function hexToRgb(h) {
  return [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
}
const BG = hexToRgb(CFG.bg);
const FG = hexToRgb(CFG.fg);

function applyScale() {
  const s = Math.floor(Math.min((window.innerWidth - 130) / CFG.w,
                                (window.innerHeight - 200) / CFG.h));
  const scale = Math.max(3, Math.min(9, s));
  view.width = CFG.w * scale;
  view.height = CFG.h * scale;
  document.documentElement.style.setProperty("--px", scale + "px");
}
applyScale();
window.addEventListener("resize", applyScale);

function paint(frame) {
  const data = image.data;
  for (let i = 0; i < frame.length; i++) {
    const c = frame.charCodeAt(i) === 49 ? FG : BG;      // "1" = dark pixel
    data[i * 4] = c[0];
    data[i * 4 + 1] = c[1];
    data[i * 4 + 2] = c[2];
    data[i * 4 + 3] = 255;
  }
  lctx.putImageData(image, 0, 0);
  vctx.imageSmoothingEnabled = false;                    // keep pixels sharp
  vctx.drawImage(lcd, 0, 0, view.width, view.height);
}

// ---------- keyboard ----------
const held = new Set();
let pressed = [];
const GAME_KEYS = ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Enter", "Escape", " "];

window.addEventListener("keydown", (e) => {
  if (GAME_KEYS.includes(e.key)) e.preventDefault();
  if (!e.repeat) pressed.push(e.key);
  held.add(e.key);
});
window.addEventListener("keyup", (e) => held.delete(e.key));
window.addEventListener("blur", () => held.clear());

// ---------- talk to Python ----------
async function loop() {
  try {
    const body = JSON.stringify({ pressed: pressed, held: [...held] });
    pressed = [];
    const res = await fetch("/api/frame", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: body,
    });
    const json = await res.json();
    paint(json.frame);
  } catch (err) {
    console.error("Cannot reach the Python server:", err);
  }
  setTimeout(loop, 16);
}
loop();