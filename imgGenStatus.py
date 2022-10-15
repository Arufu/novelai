from collections import deque
from imgGenReq import ImgGenReq


class ImgGenStatus:
    def __init__(self):
        self.generating = False
        self.counter = 0
        self.request_queue = deque()
        self.ws = None
        self.auth = None
        self.prev_reqs = {}

    def enqueue(self, req: ImgGenReq):
        self.request_queue.append(req)

    def jump_the_queue(self, req: ImgGenReq):
        self.request_queue.appendleft(req)
