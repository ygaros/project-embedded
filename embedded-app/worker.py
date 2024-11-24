import threading
from typing import Callable


class Worker:

    def __init__(self):
        self.continue_work = True
        self.thread = None

    def stop(self) -> None:
        if self.thread is not None:
            self.continue_work = False
            self.thread.join()

    def assign_work(self, work: Callable[[Callable[[], bool]], None]) -> None:
        self.stop()

        self.thread = threading.Thread(
            target=lambda: work(lambda: self.continue_work is False)
        )
        self.continue_work = True
        self.thread.start()

    def assign_work_without_flag(self, work: Callable[[], None]) -> None:
        self.stop()

        self.thread = threading.Thread(
            target=work
        )
        self.continue_work = True
        self.thread.start()
