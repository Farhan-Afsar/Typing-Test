import curses
from curses import wrapper
import time
import random



def start(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to Typing Test v1.0 ")
    stdscr.addstr("\nPress any key to start! ")
    stdscr.refresh()
    stdscr.getkey()


def random_text():
    with open("text.txt", "r") as t:
        lines = t.readlines()
        return random.choice(lines).strip()


def display(stdscr, text, curr_text, wpm):
    stdscr.addstr(text)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, j in enumerate(curr_text):
        char = text[i]
        colour = curses.color_pair(1)
        if j != char:
            colour = curses.color_pair(2)
        stdscr.addstr(0, i, j, colour)


def test(stdscr):
    text = random_text()
    curr_text = []
    wpm = 0
    start = time.time()
    stdscr.nodelay(True)

    while True:
        curr_time = max(time.time() - start, 1)
        wpm = round((len(curr_text) / (curr_time / 60)) / 5)
        stdscr.clear()
        display(stdscr, text, curr_text, wpm)
        stdscr.refresh()

        if "".join(curr_text) == text:
            stdscr.nodelay(False)
            break
        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:  # Esc to break
            break
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(curr_text) > 0:
                curr_text.pop()
        elif len(curr_text) < len(text):
            curr_text.append(key)


def main(stdscr):  # standard screen
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start(stdscr)
    while True:
        test(stdscr)

        stdscr.addstr(3, 0, "Completed! Press any key to continue...Esc to Close")
        key = stdscr.getkey()

        if ord(key) == 27:
            break


wrapper(main)
