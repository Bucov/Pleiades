/*
  Text-art renderer based on the "MIKU animation" by Coffka.exe
  (Instagram: @coffka.exe). Used with credit; keep this notice.

  Expects a global `pixelData` (rows of [r, g, b] pixels) defined in
  static/js/pixel-data.js. If it is missing the canvas stays empty.
*/

const DEFAULT_TEXT = 'Pleiades';
const canvas = document.getElementById('mikuCanvas');

// heading typewriter, same character feel as the art
function startTyped() {
    document.querySelectorAll('.typed').forEach((typed) => {
        const text = typed.textContent.trim();
        typed.textContent = '';
        let i = 0;
        (function step() {
            typed.textContent = text.slice(0, ++i);
            if (i < text.length) setTimeout(step, 45);
        })();
    });
}

// reveal the rest of the page once the intro is over
function showPage() {
    document.body.classList.remove('intro');
    startTyped();
}

if (canvas && typeof pixelData !== 'undefined') {
    const ctx = canvas.getContext('2d');
    const rows = pixelData.length;
    const cols = pixelData[0].length;
    const speed = 0.10;

    // pattern: unset -> app name, blank -> random glyphs, anything else -> custom text
    const glyphs = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#%&*+-=<>/|~!?';
    const stored = localStorage.getItem('mikuText');
    const text = stored === null ? DEFAULT_TEXT : stored.trim();
    const random = text === '';
    const pattern = random
        ? Array.from({ length: 4096 }, () => glyphs[Math.floor(Math.random() * glyphs.length)]).join('')
        : text + ' ';

    // the intro hole: one copy of the word in the middle row of the art
    const wordLen = Math.min(random ? DEFAULT_TEXT.length : text.length, cols);
    const holeRow = Math.floor(rows / 2);
    const holeCol = Math.floor((cols - wordLen) / 2);
    // start the pattern so the word begins exactly at holeCol
    const startOffset = random ? 0 : (pattern.length - holeCol % pattern.length) % pattern.length;
    let offset = startOffset;

    function metrics() {
        const box = canvas.parentElement.clientWidth;
        const fontSize = Math.max(4, Math.min(box / cols * 1.5, 14));
        ctx.font = `bold ${fontSize}px 'Courier New', Courier, monospace`;
        return { charWidth: ctx.measureText('M').width, charHeight: fontSize * 0.9 };
    }

    function resize() {
        const m = metrics();
        canvas.width = cols * m.charWidth;
        canvas.height = rows * m.charHeight;
    }

    // intro (ms): blank -> the one word shows through the cover -> cover lifts,
    // the page loads in and the art starts offsetting with the word already in place
    const BLANK = 500;
    const WORD_IN = 600;
    const HOLD = 500;
    const LIFT = 800;
    const liftStart = BLANK + WORD_IN + HOLD;
    const start = performance.now();
    let pageShown = false;

    function ease(x) {
        x = Math.max(0, Math.min(1, x));
        return 1 - Math.pow(1 - x, 3);
    }

    function draw(now) {
        const elapsed = now - start;
        const m = metrics();
        ctx.textBaseline = 'top';
        ctx.fillStyle = '#000';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        const wordAlpha = ease((elapsed - BLANK) / WORD_IN);
        const restAlpha = ease((elapsed - liftStart) / LIFT);

        // the hole follows the word as the text scrolls, so nothing pops
        const shift = Math.floor(offset - startOffset);
        const holeStart = holeCol - shift;

        for (let r = 0; r < rows; r++) {
            if (r !== holeRow && restAlpha <= 0) continue;
            ctx.globalAlpha = restAlpha;
            for (let c = 0; c < cols; c++) {
                if (r === holeRow) {
                    const inHole = c >= holeStart && c < holeStart + wordLen;
                    ctx.globalAlpha = inHole ? wordAlpha : restAlpha;
                    if (ctx.globalAlpha <= 0) continue;
                }
                const p = pixelData[r][c];
                ctx.fillStyle = `rgb(${p[0]}, ${p[1]}, ${p[2]})`;
                // random glyphs get a per-row offset so the stream doesn't line up vertically
                const i = random ? c + r * 37 : c;
                const ch = pattern[Math.floor(i + offset) % pattern.length];
                ctx.fillText(ch, c * m.charWidth, r * m.charHeight);
            }
        }
        ctx.globalAlpha = 1;

        // the art stays paused until the cover starts to lift
        if (elapsed >= liftStart) {
            offset += speed;
            if (!pageShown) {
                pageShown = true;
                showPage();
            }
        }
        requestAnimationFrame(draw);
    }

    window.addEventListener('resize', resize);
    resize();
    requestAnimationFrame(draw);
} else if (document.body.classList.contains('intro')) {
    // no art available: skip the intro after the blank pause
    setTimeout(showPage, 500);
} else {
    startTyped();
}
