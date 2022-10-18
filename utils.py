from imgGenReq import ImgGenReq
from constants import Const

const = Const()


def check_if_large(req: ImgGenReq):
    return req.height * req.width > const.max_free_size


def check_if_pay(req: ImgGenReq):
    return check_if_large(req) or req.steps > const.max_free_steps
