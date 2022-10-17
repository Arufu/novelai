import random
from imgGenReq import ImgGenReq
from constants import Const

const = Const()


class MeowMsgs:
    @staticmethod
    def get_finished_draw(req: ImgGenReq, seed: str, is_master: bool):
        steps = str(req.steps)
        if is_master:
            msgs = [
                '主人大人，您的' + steps + '步画风' + str(req.scale) + '图已经完成了喵！(心心眼)',
                '主人大人，' + steps + '步画风' + str(req.scale) + '图真的很难喵，我这个笨蛋只能画出这种样子了喵...(沮丧)',
                steps + '步画风' + str(req.scale) + '图的话...这样可以吗喵？(小心)',
            ]
        else:
            msgs = [
                '你的' + steps + '步画风' + str(req.scale) + '图画好了喵！心怀对大姐姐的感激收下图吧喵！(高高在上)',
                '嘛...总之' + steps + '步画风' + str(req.scale) + '图就画成这样了喵！不要有怨言喵！(哈欠)',
                '来被我对' + steps + '步画风' + str(req.scale) + '图的天才般的创意震撼吧喵！',
            ]
        msg = random.choice(msgs)
        msg += (' 顺便一提种子是' + seed + '喵！')

        pay = False
        pay_item = []
        if req.steps > const.default_steps:
            pay_item.append('\n' + steps + '步的图')
            pay = True
        if (req.height == const.H_W['大横图'][0] and req.width == const.H_W['大横图'][1]) or \
                (req.height == const.H_W['大竖图'][0] and req.width == const.H_W['大竖图'][1]) or \
                (req.height == const.H_W['大方图'][0] and req.width == const.H_W['大方图'][1]):
            pay_item.append('大图')
            pay = True

        # if pay:
        #     if len(pay_item) == 1:
        #         msg += pay_item[0]
        #     else:
        #         msg += '和'.join(pay_item)
        #         msg += '都'
        #     msg += '是要扣除点数的喵！嘛虽然扣的是i佬的点数就是了喵！距离i佬被榨干还有'
        #     msg += str(req.points_left)
        #     msg += '点喵！大家加油喵！'

        return msg
