from collections import deque
from imgGenReq import ImgGenReq


class ImgGenStatus:
    def __init__(self):
        self.generating = False
        self.counter = 0
        self.request_queue = deque()
        self.low_priority_request_queue = deque()
        self.ws = None
        self.auth = None
        self.prev_reqs = {}

    def enqueue(self, req: ImgGenReq):
        self.request_queue.append(req)

    def clear_queue(self):
        self.request_queue.clear()

    def jump_the_queue(self, req: ImgGenReq):
        self.request_queue.appendleft(req)

    def enqueue_low_priority(self, req: ImgGenReq):
        self.low_priority_request_queue.append(req)

    def clear_low_priority_queue(self):
        self.low_priority_request_queue.clear()

    def jump_the_queue_low_priority(self, req: ImgGenReq):
        self.low_priority_request_queue.appendleft(req)


