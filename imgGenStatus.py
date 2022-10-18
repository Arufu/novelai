from collections import deque
from imgGenReq import ImgGenReq


class ImgGenStatus:
    def __init__(self):
        self.generating = False
        self.counter = 0
        self.request_queue_self_host = deque()
        self.request_queue_low_priority = deque()
        self.request_queue_nai = deque()
        self.ws = None
        self.auth = None
        self.prev_reqs = {}

    def enqueue_self_host(self, req: ImgGenReq):
        self.request_queue_self_host.append(req)

    def clear_queue_self_host(self):
        self.request_queue_self_host.clear()

    def jump_the_queue_self_host(self, req: ImgGenReq):
        self.request_queue_self_host.appendleft(req)

    def enqueue_low_priority(self, req: ImgGenReq):
        self.request_queue_low_priority.append(req)

    def clear_low_priority_queue(self):
        self.request_queue_low_priority.clear()

    def jump_the_queue_low_priority(self, req: ImgGenReq):
        self.request_queue_low_priority.appendleft(req)

    def enqueue_nai(self, req: ImgGenReq):
        self.request_queue_nai.append(req)

    def clear_queue_nai(self):
        self.request_queue_nai.clear()

    def jump_the_queue_nai(self, req: ImgGenReq):
        self.request_queue_nai.appendleft(req)
