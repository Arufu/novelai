from constants import Const

const = Const()


class ImgGenReq:
    def __init__(self, group_id: str, sender_id: str, tags: str, height: int, width: int):
        self.group_id = group_id
        self.sender_id = sender_id
        self.tags = tags
        self.height = height
        self.width = width
        self.steps = const.default_steps
        self.scale = const.default_scale
        self.model = const.default_model
        self.sampler = const.default_sampler
        self.seed = None
        self.uc = const.default_uc
        self.points_left = None
