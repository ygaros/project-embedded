import time
from typing import Callable

from gpiozero import PWMLED, RGBLED

from mocks.pwmled_mock import PWMLEDMOCK
from mocks.rgbled_mock import RGBLEDMOCK
from util_func import add_or_sub, check_counter


class LedController:

    def __init__(self):
        try:
            self.led1 = PWMLED(17)
            self.led2 = PWMLED(27)
            self.led3 = PWMLED(22)
            self.led4 = PWMLED(5)
            self.led5 = PWMLED(6)
            self.led6 = PWMLED(13)
            self.led_rgb = RGBLED(9, 11, 10)
        except Exception as error:
            self.led1 = PWMLEDMOCK(17)
            self.led2 = PWMLEDMOCK(27)
            self.led3 = PWMLEDMOCK(22)
            self.led4 = PWMLEDMOCK(5)
            self.led5 = PWMLEDMOCK(6)
            self.led6 = PWMLEDMOCK(13)
            self.led_rgb = RGBLEDMOCK(9, 11, 10)

    def run_stop(self):
        self.led1.value = 0
        self.led2.value = 0
        self.led3.value = 0
        self.led4.value = 0
        self.led5.value = 0
        self.led6.value = 0
        print("stop was called")

    def run_wave(self, stop: Callable[[], bool]):
        self.led1.value = 1
        self.led2.value = 1
        self.led3.value = 1
        self.led4.value = 1
        self.led5.value = 1
        self.led6.value = 1

        going_down1 = False
        going_down2 = False
        going_down3 = True
        going_down4 = True
        going_down5 = True
        going_down6 = True

        counter1 = 0.64
        counter2 = 0.80
        counter3 = 0.96
        counter4 = 0.80
        counter5 = 0.64
        counter6 = 0.48

        while not stop():
            print("wave is running")
            counter1 = add_or_sub(counter1, going_down1)
            counter1, going_down1 = check_counter(counter1, going_down1)
            self.led1.value = counter1

            counter2 = add_or_sub(counter2, going_down2)
            counter2, going_down2 = check_counter(counter2, going_down2)
            self.led2.value = counter2

            counter3 = add_or_sub(counter3, going_down3)
            counter3, going_down3 = check_counter(counter3, going_down3)
            self.led3.value = counter3

            counter4 = add_or_sub(counter4, going_down4)
            counter4, going_down4 = check_counter(counter4, going_down4)
            self.led4.value = counter4

            counter5 = add_or_sub(counter5, going_down5)
            counter5, going_down5 = check_counter(counter5, going_down5)
            self.led5.value = counter5

            counter6 = add_or_sub(counter6, going_down6)
            counter6, going_down6 = check_counter(counter6, going_down6)
            self.led6.value = counter6

    def run_side_to_side(self, stop: Callable[[], bool]):
        self.led1.value = 1
        self.led2.value = 1
        self.led3.value = 1
        self.led4.value = 1
        self.led5.value = 1
        self.led6.value = 1

        going_down1 = False
        going_down2 = False
        going_down3 = True
        going_down4 = True
        going_down5 = True
        going_down6 = True

        counter1 = 0.64
        counter2 = 0.80
        counter3 = 0.96
        counter4 = 0.80
        counter5 = 0.64
        counter6 = 0.48

        counter = 0
        while not stop():
            print("side to side is running")
            if counter1 == 0 and counter % 2 == 0:
                counter = counter + 1
                going_down2 = not going_down2
                going_down3 = not going_down3
                going_down4 = not going_down4
                going_down5 = not going_down5
                going_down6 = not going_down6

            if counter6 == 0 and counter % 2 == 1:
                counter = counter + 1
                going_down1 = not going_down1
                going_down2 = not going_down2
                going_down3 = not going_down3
                going_down4 = not going_down4
                going_down5 = not going_down5

            counter1 = add_or_sub(counter1, going_down1)
            counter1, going_down1 = check_counter(counter1, going_down1)
            self.led1.value = counter1

            counter2 = add_or_sub(counter2, going_down2)
            counter2, going_down2 = check_counter(counter2, going_down2)
            self.led2.value = counter2

            counter3 = add_or_sub(counter3, going_down3)
            counter3, going_down3 = check_counter(counter3, going_down3)
            self.led3.value = counter3

            counter4 = add_or_sub(counter4, going_down4)
            counter4, going_down4 = check_counter(counter4, going_down4)
            self.led4.value = counter4

            counter5 = add_or_sub(counter5, going_down5)
            counter5, going_down5 = check_counter(counter5, going_down5)
            self.led5.value = counter5

            counter6 = add_or_sub(counter6, going_down6)
            counter6, going_down6 = check_counter(counter6, going_down6)
            self.led6.value = counter6

    def run_full_bright(self, stop: Callable[[], bool]):
        self.led1.value = 1
        self.led2.value = 1
        self.led3.value = 1
        self.led4.value = 1
        self.led5.value = 1
        self.led6.value = 1

        while not stop():
            print("full bright is running")
            time.sleep(1)

    def run_blinking(self, stop: Callable[[], bool]):
        off = 0
        on = 1
        self.led1.value = off
        self.led2.value = off
        self.led3.value = off
        self.led4.value = off
        self.led5.value = off
        self.led6.value = off

        while not stop():
            print("blinking is running")
            self.led1.value = on
            self.led2.value = on
            self.led3.value = on
            self.led4.value = on
            self.led5.value = on
            self.led6.value = on
            time.sleep(0.1)

            self.led1.value = off
            self.led2.value = off
            self.led3.value = off
            self.led4.value = off
            self.led5.value = off
            self.led6.value = off
            time.sleep(1)

    def set_rbg_led(self, red: float, green: float, blue: float) -> None:
        print(f"SET RGB to RED: {red}, GREEN: {green}, BLUE: {blue}")
        self.led_rgb.value = (red, green, blue)

    def get_style_for_mode_id(self, mode_id: int) -> Callable[[Callable[[], bool]], None]:
        match mode_id:
            case 0:
                return self.run_side_to_side
            case 1:
                return self.run_wave
            case 2:
                return self.run_blinking
            case 3:
                return self.run_full_bright
            case _:
                return self.run_full_bright
