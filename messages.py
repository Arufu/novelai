import random
from imgGenReq import ImgGenReq
from constants import Const
import utils

const = Const()


class MeowMsgs:
    def __init__(self):
        pass

    @staticmethod
    def get_finished_draw(req: ImgGenReq, seed: str, is_master: bool):
        steps = str(req.steps)
        complexity = '复杂' if utils.check_if_pay(req) else '简单'
        if is_master:
            msgs = [
                '主人大人，您的' + steps + '步画风' + str(req.scale) + complexity + '图已经完成了喵！(心心眼)',
                '主人大人，' + steps + '步画风' + str(req.scale) + complexity + '图真的很难喵，我这个笨蛋只能画出这种样子了喵...(沮丧)',
                steps + '步画风' + str(req.scale) + complexity + '图的话...这样可以吗喵？(小心)',
            ]
        else:
            msgs = [
                '你的' + steps + '步画风' + str(req.scale) + complexity + '图画好了喵！心怀对大姐姐的感激收下图吧喵！(高高在上)',
                '嘛...总之' + steps + '步画风' + str(req.scale) + complexity + '图就画成这样了喵！不要有怨言喵！(哈欠)',
                '来被我对' + steps + '步画风' + str(req.scale) + complexity + '图的天才般的创意震撼吧喵！',
            ]
        msg = random.choice(msgs)
        msg += (' 顺便一提种子是' + seed + '喵！')

        pay = False
        pay_item = []
        if req.steps > const.max_free_steps:
            pay_item.append('\n' + steps + '步的图')
            pay = True
        if utils.check_if_large(req):
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

        if pay and req.sender_id != const.master_id:
            if len(pay_item) == 1:
                msg += pay_item[0]
            else:
                msg += '和'.join(pay_item)
                msg += '都'
            msg += '是很复杂的喵!复杂图我是记在另一个小本子上用爪子画的喵!想快点看到图的话就让我画简单图喵!简单图我顺便用尾巴抽空就画出来了喵!'

        return msg
