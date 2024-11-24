import signal
import sys

from fastapi import FastAPI
from fastapi import Request
from pydantic import BaseModel
from starlette.templating import Jinja2Templates

from led_controller import LedController
from worker import Worker

app = FastAPI()
led_controller: LedController = LedController()
background_thread: Worker = Worker()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/led/{mode_id}")
def led_start(mode_id: int):
    background_thread.stop()
    background_thread.assign_work(
        led_controller.get_style_for_mode_id(mode_id)
    )

    return {"thread": "started"}


class RGBValues(BaseModel):
    red: str
    green: str
    blue: str


@app.post("/rgb")
def rgb(rgb_values: RGBValues):
    red = int(rgb_values.red, 16) / 256
    green = int(rgb_values.green, 16) / 256
    blue = int(rgb_values.blue, 16) / 256

    led_controller.set_rbg_led(
        red, green, blue
    )

    return {"status": "LED RGB set"}


@app.get("/stop")
def stop():
    background_thread.assign_work_without_flag(
        led_controller.run_stop
    )
    background_thread.stop()

    return {"status": "stopped"}


def cleaner(signum, frame):
    print("CLEANER FUNCTION FIRED")
    background_thread.stop()

    sys.exit(0)


signal.signal(signal.SIGINT, cleaner)

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
