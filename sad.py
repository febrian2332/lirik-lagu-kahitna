
import os
import random
import shutil
import sys
import time

os.system("")  # aktifkan warna ANSI di Windows
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

LYRICS_FILE = "lirik.txt"
HOLD_FRAMES = 50 # lama tiap baris ditahan (makin besar = makin lama)
TYPE_SPEED = 1        # huruf per frame (naikin biar ngetiknya lebih cepet)
FPS_DELAY = 0.06      # delay antar frame

RESET = "\033[0m"
BLUE = "\033[34m"
CYAN = "\033[96m"
PINK = "\033[1;95m"
GREY = "\033[90m"

TITLE = "♪ Kahitna - Cinta Sudah Lewat ♪"


def load_lyrics():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), LYRICS_FILE)
    if not os.path.exists(path):
        print(f"File '{LYRICS_FILE}' belum ada. Bikin dulu di folder yang sama, "
              "terus isi dengan liriknya.")
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        lines = [ln.strip() for ln in f.read().splitlines()]
    if not any(lines):
        print(f"File '{LYRICS_FILE}' masih kosong.")
        sys.exit(1)
    return lines


def put(grid, row, text, color, w, h):
    if not (0 <= row < h):
        return
    start = max(0, (w - len(text)) // 2)
    for i, ch in enumerate(text):
        if 0 <= start + i < w:
            grid[row][start + i] = (ch, color)


def main():
    lyrics = load_lyrics()
    w, h = shutil.get_terminal_size()
    h -= 1
    drops = [[random.randrange(w), random.randrange(h), random.choice((1, 1, 2))]
             for _ in range(max(10, w // 4))]

    idx, shown, hold, prev = 0, 0, 0, ""
    typing = True
    sys.stdout.write("\033[?25l\033[2J")

    try:
        while True:
            grid = [[(" ", "") for _ in range(w)] for _ in range(h)]

            # hujan
            for d in drops:
                x, y, s = d
                if 0 <= y < h and 0 <= x < w:
                    grid[y][x] = ("│", CYAN) if s == 2 else ("╎", BLUE)
                d[1] += s
                if d[1] >= h:
                    d[0], d[1], d[2] = random.randrange(w), 0, random.choice((1, 1, 2))

            # judul, baris sebelumnya (redup), baris sekarang (nyala)
            put(grid, 1, TITLE, GREY, w, h)
            put(grid, h // 2 - 2, prev, GREY, w, h)
            current = lyrics[idx]
            put(grid, h // 2, current[:shown], PINK, w, h)

            # render
            lines = []
            for r in grid:
                line, cur = "", ""
                for ch, c in r:
                    if c != cur:
                        line += RESET + c
                        cur = c
                    line += ch
                lines.append(line + RESET)
            sys.stdout.write("\033[H" + "\n".join(lines))
            sys.stdout.flush()

            # ngetik -> tahan -> baris berikutnya
            if typing:
                shown += TYPE_SPEED
                if shown >= len(current):
                    shown, typing = len(current), False
                    hold = HOLD_FRAMES if current else HOLD_FRAMES // 2
            else:
                hold -= 1
                if hold <= 0:
                    if current:
                        prev = current
                    idx = (idx + 1) % len(lyrics)
                    shown, typing = 0, True

            time.sleep(FPS_DELAY)

    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\033[?25h" + RESET + "\033[2J\033[H")
        print("Udah ya... hujannya reda. Semangat, bro.")


if __name__ == "__main__":
    main()