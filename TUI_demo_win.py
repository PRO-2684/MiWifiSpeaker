import keyboard, ctypes
from queue import Queue
from threading import Thread
from rich.console import Console
from rich.progress_bar import ProgressBar
from MiWifiSpeakerV3 import WifiSpeakerV3, PlayStatus
from time import sleep
from os import system
from json import load, dump

HANDLE = ctypes.windll.kernel32.GetStdHandle(-11)
FULL_UPDATE_INTERVAL = 5
VOLUMN_WAIT_TIME = 1
TITLE_LINE = 0
BAR_LINE = 1
TIME_DETAIL_LINE = 2
EXTRA_LINE = 3
CONSOLE = Console()
tasks = Queue()


class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    def __init__(self, x, y):
        self.X = x
        self.Y = y


class Line:
    def __init__(self, renderable: str, y: int) -> None:
        self.renderable = renderable
        self.y = y


def goto(y) -> None:
    ctypes.windll.kernel32.SetConsoleCursorPosition(HANDLE, COORD(0, y))


def seconds_to_str(seconds: int) -> str:
    s = seconds % 60
    m = (seconds % 3600) // 60
    h = seconds // 3600
    return f"{h:02}:{m:02}:{s:02}" if h else f"{m:02}:{s:02}"


def count_none_ascii(s: str) -> int:
    n = 0
    for ch in s:
        if ord(ch) >= 127:
            n += 1
    return n


def update_title() -> None:
    title = f"{status.song_path[1:-4]} - {status.play_status.name}"
    title = title.center(CONSOLE.width - count_none_ascii(title))
    tasks.put(Line(f"[bold]{title}[/bold]", TITLE_LINE))


def update_bar(seconds: int = 0) -> None:
    if seconds:
        bar.update(bar.completed + seconds * 1000)
    else:
        bar.update(status.position, status.duration)
    tasks.put(Line(bar, BAR_LINE))


def update_time_detail(seconds: int = 0) -> None:
    time_detail = f"{seconds_to_str((bar.completed // 1000 + seconds) if seconds else status.position // 1000) } / {seconds_to_str(status.duration // 1000)}".center(
        CONSOLE.width
    )
    tasks.put(Line(time_detail, TIME_DETAIL_LINE))


def full_update() -> None:
    global status
    status = wifi_speaker.status
    update_title()
    update_bar()
    update_time_detail()


def printer() -> None:
    while True:
        task = tasks.get()
        goto(task.y)
        CONSOLE.print(task.renderable, end="", highlight=False)


def time_updater() -> None:
    global status
    while True:
        sleep(1)
        if status.play_status == PlayStatus.Playing:
            if bar.completed >= bar.total:
                full_update()
            else:
                update_bar(1)
                update_time_detail(1)


def on_space(event: keyboard.KeyboardEvent):
    global status
    if event.event_type == "up":
        if status.play_status == PlayStatus.Paused:
            status.play_status = PlayStatus.Playing
            update_title()
            wifi_speaker.play()
        else:
            status.play_status = PlayStatus.Paused
            update_title()
            wifi_speaker.pause()
        full_update()


def vol_up(event: keyboard.KeyboardEvent):
    global volumn, volumn_waiting, volumn_printed
    if event.event_type == "down":
        volumn_printed = True
        volumn_waiting = int(VOLUMN_WAIT_TIME * 100)
        volumn += 1
        tasks.put(Line(f"Volumn: {volumn}%".center(CONSOLE.width), EXTRA_LINE))


def vol_down(event: keyboard.KeyboardEvent):
    global volumn, volumn_waiting, volumn_printed
    if event.event_type == "down":
        volumn_printed = True
        volumn_waiting = int(VOLUMN_WAIT_TIME * 100)
        volumn -= 1
        tasks.put(Line(f"Volumn: {volumn}%".center(CONSOLE.width), EXTRA_LINE))


def volumn_timer() -> None:
    global volumn_waiting, volumn_printed
    while True:
        sleep(0.01)
        if volumn_waiting > 0:
            volumn_waiting -= 1
        else:
            if volumn != status.volume:
                tasks.put(
                    Line(
                        "[italic dim]"
                        + f"Setting volumn to {volumn}%...".center(CONSOLE.width),
                        EXTRA_LINE,
                    )
                )
                status.volume = volumn
                wifi_speaker.set_volume(volumn)
                tasks.put(
                    Line(
                        "[italic dim]"
                        + f"Volumn set to {volumn}%".center(CONSOLE.width),
                        EXTRA_LINE,
                    )
                )
                sleep(1)
            elif volumn_printed:
                volumn_printed = False
                tasks.put(Line(" " * CONSOLE.width, EXTRA_LINE))


def next_song(event: keyboard.KeyboardEvent):
    if event.event_type == "up":
        tasks.put(Line("[italic dim]" + "Loading...".center(CONSOLE.width), EXTRA_LINE))
        status.play_status = PlayStatus.Paused
        wifi_speaker.next_song()
        full_update()
        tasks.put(Line(" " * CONSOLE.width, EXTRA_LINE))


def prev_song(event: keyboard.KeyboardEvent):
    if event.event_type == "up":
        tasks.put(Line("[italic dim]" + "Loading...".center(CONSOLE.width), EXTRA_LINE))
        wifi_speaker.prev_song()
        full_update()
        tasks.put(Line(" " * CONSOLE.width, EXTRA_LINE))


def manual_refresh(event: keyboard.KeyboardEvent):
    if event.event_type == "up":
        tasks.put(
            Line("[italic dim]" + "Refreshing...".center(CONSOLE.width), EXTRA_LINE)
        )
        status.play_status = PlayStatus.Paused
        full_update()
        tasks.put(Line(" " * CONSOLE.width, EXTRA_LINE))


try:
    with open("cookie") as f:
        wifi_speaker = WifiSpeakerV3(cookie=load(f))
        status = wifi_speaker.status
except:
    print("Refreshing cookie...")
    wifi_speaker = WifiSpeakerV3("***", "***")
    status = wifi_speaker.status
    with open("cookie", "w") as f:
        dump(wifi_speaker.cookie.get_dict(), f)
bar = ProgressBar(complete_style="cyan", finished_style="cyan")
volumn_waiting = 0
volumn = status.volume
volumn_printed = False
system("cls")
print("\033[?25l")  # Hide cursor
full_update()
Thread(target=printer, daemon=True).start()
Thread(target=time_updater, daemon=True).start()
Thread(target=volumn_timer, daemon=True).start()
keyboard.hook_key("space", on_space, suppress=True)
keyboard.hook_key("up", vol_up, suppress=True)
keyboard.hook_key("down", vol_down, suppress=True)
keyboard.hook_key("left", prev_song, suppress=True)
keyboard.hook_key("right", next_song, suppress=True)
keyboard.hook_key("f5", manual_refresh, suppress=True)
keyboard.wait("esc")
print("\033[?25h")
system("cls")
