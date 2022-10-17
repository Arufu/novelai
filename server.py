import json
import os
import random
from sys import path
from os import environ as env
from os.path import join, abspath, dirname
from novelai_api import NovelAI_API
from aiohttp import ClientSession
from logging import Logger, StreamHandler
import requests
import base64
import asyncio
import threading
import re
import json
from types import SimpleNamespace

from sanic import Sanic

from imgGenReq import ImgGenReq
from imgGenStatus import ImgGenStatus
from messages import MeowMsgs
from constants import Const

google_colab_endpoint = 'https://accent-pixel-base-twins.trycloudflare.com/generate-stream'

app = Sanic('qqbot')

const = Const()

path.insert(0, abspath(join(dirname(__file__), '..')))
required_env_var = ['NAI_USERNAME', 'NAI_PASSWORD', 'NAI_IMG_GEN_ENDPOINT']

if any(env_var not in env for env_var in required_env_var):
    raise RuntimeError('Please ensure that all environment variables are set')

NAI_username = env['NAI_USERNAME']
NAI_password = env['NAI_PASSWORD']
img_gen_endpoint = env['NAI_IMG_GEN_ENDPOINT']
subscription_endpoint = env['NAI_SUB_ENDPOINT']

logger = Logger('NAIBot')
logger.addHandler(StreamHandler())

OUTPUT_PATH = os.path.dirname(__file__) + '/output/'

FORBIDDEN_WORDS = const.forbidden_words

H_W = const.H_W

IMG_GEN_SHAPE_PATTERN = const.img_gen_shape_pattern
IMG_GEN_TAG_PATTERN = const.img_gen_tag_pattern
IMG_GEN_NUM_PAGE_PATTERN = const.img_gen_num_page_pattern
IMG_GEN_NUM_STEPS_PATTERN = const.img_gen_num_steps_pattern
IMG_GEN_SAMPLER_PATTERN = const.img_gen_sampler_pattern
IMG_GEN_SCALE_PATTERN = const.img_gen_scale_pattern
IMG_GEN_UC_PATTERN = const.img_gen_uc_pattern
IMG_GEN_SEED_PATTERN = const.img_gen_seed_pattern
IMG_GEN_HIGH_QUALITY_PATTERN = const.high_quality_pattern
IMG_GEN_SAFE_PATTERN = const.img_gen_safe_pattern

IMG_GEN_PRESET_TAGS = const.tag_presets

IMG_GEN_PRESETS = IMG_GEN_PRESET_TAGS.keys()

AT_ME = const.at_me
MASTER_ID = const.master_id
MAX_NUM_PAGES = const.max_num_pages


@app.websocket('/qqbot')
async def qqbot(request, ws):
    async with ClientSession() as session:

        # Login nai and get login auth.
        # api = NovelAI_API(session, logger=logger)
        # auth = await api.high_level.login(NAI_username, NAI_password)
        # logger.info(auth)
        auth = None

        gen_status = ImgGenStatus()
        gen_status.ws = ws
        gen_status.auth = auth

        threading.Thread(target=asyncio.run, args=[gen_and_send(gen_status)], daemon=True).start()

        while True:
            data = await ws.recv()
            data = json.loads(data)
            print(json.dumps(data, indent=4, ensure_ascii=False))
            # Check if message is from group and not empty.
            if data.get('message_type') == 'group' and data.get('raw_message'):
                raw_message = data['raw_message']
                raw_message = raw_message.replace('，', ',')
                raw_message = raw_message.replace('\n', '')
                group_id = data['group_id']
                sender_id = data['sender']['user_id']
                if any(at_me in raw_message for at_me in AT_ME):
                    if raw_message.strip() in AT_ME:
                        if sender_id == MASTER_ID:
                            reply_msg = '主人大人您找我有什么事喵？(乖巧)'
                        else:
                            reply_msg = '嗯嗯？你这家伙戳我做什么喵？'
                        await send_text_with_at(ws, group_id, sender_id, reply_msg)
                    elif any(kw in raw_message for kw in ['求助', '帮助', '功能', '自我介绍', '喵']):
                        if sender_id == MASTER_ID:
                            reply_msg = '喵喵嗯~(翻滚)'
                        else:
                            reply_msg = '\n' + '\n'.join([
                                '我是聪明的画师日和大姐姐喵！',
                                '1. 找我画画：先@大姐姐我，然后求画<形状>, 写上<标签>就行了喵！形状可以是<竖图>, <横图>和<方图>喵！',
                                '\t比如：@日和大姐姐，求画<竖图>，标签是<corpse, gothic, guro>',
                                '2. 问聪明的我问题，先@大姐姐我，然后打上问题喵！',
                                '\t比如：@日和大姐姐，群里最伟大的人是谁？',
                            ])
                        await send_text_with_at(ws, group_id, sender_id, reply_msg)
                    elif '群里最伟大的人是谁' in raw_message:
                        if sender_id == MASTER_ID:
                            reply_msg = '当当当然是主人大人您了喵！(卑微)'
                        else:
                            reply_msg = '当然是鸽子啊这还用问喵'
                        await send_text_with_at(ws, group_id, sender_id, reply_msg)
                    elif any(kw in raw_message for kw in ['重复', '再来', '重画', '重新', '重来', '再来']):
                        if sender_id in gen_status.prev_reqs:
                            req = gen_status.prev_reqs[sender_id]
                            if sender_id == MASTER_ID:
                                reply_msg = '这就马上再画一次上次的喵！(卑微)'
                                gen_status.jump_the_queue(req)
                            else:
                                reply_msg = '竟然让大姐姐重新画上次的喵？那就只好画了喵！但是该排队还是要排的喵！'
                                gen_status.enqueue(req)
                            await send_text_with_at(ws, group_id, sender_id, reply_msg)
                        else:
                            if sender_id == MASTER_ID:
                                reply_msg = '对不起主人，我忘了上次画的是什么了喵...请原谅我这个笨蛋喵...(哭哭)'
                            else:
                                reply_msg = '大姐姐想不起来你上次要画的是什么了喵！重新说一下吧喵！'
                            await send_text_with_at(ws, group_id, sender_id, reply_msg)
                    elif IMG_GEN_SHAPE_PATTERN.search(raw_message) and \
                            (IMG_GEN_TAG_PATTERN.search(raw_message) or
                             any(preset in raw_message for preset in IMG_GEN_PRESETS)):
                        ###############################
                        # Start generate.
                        ###############################
                        # Get shape.
                        shape_m = IMG_GEN_SHAPE_PATTERN.search(raw_message)
                        groups = shape_m.groups()
                        shape = groups[0]
                        if shape not in H_W.keys():
                            if sender_id == MASTER_ID:
                                reply_msg = '主人大人您说的形状对我来说还太早了喵>_<(颤抖)'
                            else:
                                reply_msg = '我看不懂你要画什么图喵！'
                            await send_text_with_at(ws, group_id, sender_id, reply_msg)
                            continue

                        # Get tags.
                        tags = None
                        tags_m = IMG_GEN_TAG_PATTERN.search(raw_message)
                        # Find explicit tags.
                        if tags_m:
                            groups = tags_m.groups()
                            tags = groups[0]
                        else:
                            # If no explicit tags, find the first presents.
                            for preset in IMG_GEN_PRESETS:
                                if preset in raw_message:
                                    tags = IMG_GEN_PRESET_TAGS[preset]
                                    break

                        if (not tags) or (not tags.strip().split(const.tags_delimiter)):
                            if sender_id == MASTER_ID:
                                reply_msg = '主人大人您说的标签对我来说太高深了喵>_<(颤抖)'
                            else:
                                reply_msg = '这...这是什么标签来着喵！看不懂喵！'
                            await send_text_with_at(ws, group_id, sender_id, reply_msg)
                            continue
                        else:
                            # Check number of pages.
                            num_pages = 1
                            num_page_m = IMG_GEN_NUM_PAGE_PATTERN.search(raw_message)
                            if num_page_m:
                                num_pages = int(num_page_m.groups()[0])
                                if num_pages > MAX_NUM_PAGES and sender_id != MASTER_ID:
                                    await send_text_with_at(ws, group_id, sender_id, '想一次画' + str(num_pages) +
                                                            '张？人类真是太贪心了喵！本大姐姐最多一次只接' + str(MAX_NUM_PAGES) +
                                                            '张画喵！作为贪心的惩罚，这次只给你画一张喵！')
                                    num_pages = 1
                            height = H_W[shape][0]
                            width = H_W[shape][1]
                            req = ImgGenReq(group_id, sender_id, tags, height, width)

                            msg = []
                            add_at(sender_id, msg)
                            if gen_status.generating:
                                if sender_id == MASTER_ID:
                                    reply_msg = '喵喵喵！这就插队给主人大人您画' + str(num_pages) + '张喵！马上马上喵！(振奋)'
                                else:
                                    reply_msg = str(num_pages) + '张是吧喵？记在小本子上啦喵！不过正在画别的喵！慢慢等喵！'
                                add_text(reply_msg, msg)
                            else:
                                if sender_id == MASTER_ID:
                                    reply_msg = '喵喵喵！请主人大人稍等喵！这就开始画喵！(慌乱)(抽出' + str(num_pages) + '张纸)'
                                else:
                                    reply_msg = '嘛~正好现在比较有空喵，就给你画' + str(num_pages) + '张吧喵！(悠闲)'
                                add_text(reply_msg, msg)
                            await send_group_msg(ws, group_id, msg)

                            ######################################
                            # Request modification
                            ######################################

                            # Add high quality tags.
                            hq_m = IMG_GEN_HIGH_QUALITY_PATTERN.search(raw_message)
                            if hq_m:
                                req.tags += ','
                                req.tags += const.high_quality_tags

                            # Modify steps.
                            steps_m = IMG_GEN_NUM_STEPS_PATTERN.search(raw_message)
                            if steps_m:
                                req.steps = int(steps_m.groups()[0])

                            # Modify scale.
                            scale_m = IMG_GEN_SCALE_PATTERN.search(raw_message)
                            if scale_m:
                                req.scale = int(scale_m.groups()[0])

                            # Modify sampler.
                            sampler_m = IMG_GEN_SAMPLER_PATTERN.search(raw_message)
                            if sampler_m:
                                req.sampler = sampler_m.groups()[0]

                            # Modify uc.
                            uc_m = IMG_GEN_UC_PATTERN.search(raw_message)
                            if uc_m:
                                uc = uc_m.groups()[0]
                                req.uc = req.uc + ',' + uc

                            # Modify seed.
                            seed_m = IMG_GEN_SEED_PATTERN.search(raw_message)
                            if seed_m:
                                req.seed = seed_m.groups()[0]

                            # Modify model.
                            # if sender_id in const.full_model_ids:
                            #     req.model = const.full_model

                            model_m = IMG_GEN_SAFE_PATTERN.search(raw_message)
                            if model_m:
                                req.model = const.safe_model

                            for _ in range(num_pages):
                                if sender_id == MASTER_ID:
                                    gen_status.jump_the_queue(req)
                                else:
                                    gen_status.enqueue(req)
                    else:
                        if sender_id == MASTER_ID:
                            reply_msg = '主主主人大人，这么深奥的话语我听不懂喵T_T我真是个笨蛋喵！(惊慌)'
                        else:
                            reply_msg = '虽然聪明的我知道你在说什么喵，但是冷酷的大姐姐是不会回答这种问题的喵！'
                        await send_text_with_at(ws, group_id, sender_id, reply_msg)
            await asyncio.sleep(0.1)


async def send_text_with_at(ws, group_id, sender_id, text):
    msg = []
    add_at(sender_id, msg)
    add_text(text, msg)
    await send_group_msg(ws, group_id, msg)


async def send_group_msg(ws, group_id: str, msg: list):
    ret = {
        'action': 'send_group_msg',
        'params': {
            'group_id': group_id,
            'message': msg,
        }
    }
    await ws.send(json.dumps(ret))


async def gen_and_send(status: ImgGenStatus):
    while True:
        # Skip when queue is empty
        if not status.request_queue:
            await asyncio.sleep(1)
            continue

        # Get and remove an item from the left.
        req: ImgGenReq = status.request_queue.popleft()
        status.generating = True

        # Skip the request with forbidden tags.
        tags = re.split(const.tags_delimiter, req.tags)
        has_forbidden_words = (req.sender_id not in const.full_model_ids) and any(
            tag.strip().lower() in FORBIDDEN_WORDS for tag in tags)
        if has_forbidden_words:
            msg = []
            add_at(req.sender_id, msg)
            if req.sender_id == MASTER_ID:
                reply_msg = '主人大人，这种标签' + req.tags + '请私底下找我偷偷画喵...(羞涩)'
            else:
                reply_msg = '仔细看了一下才发现你的图<' + req.tags + '>太糟糕了喵！摔笔喵！不可以色色喵！生气气喵！'
            add_text(reply_msg, msg)
            await send_group_msg(status.ws, req.group_id, msg)
            status.generating = False
            continue

        img_path = ''
        # Attempt a few times if failed to generate an image.
        for _ in range(3):
            img_path = generate_img(req, status.auth)
            if img_path:
                break

        msg = []
        add_at(req.sender_id, msg)
        if not img_path or (os.path.getsize(img_path) < 1000):
            if req.sender_id == MASTER_ID:
                reply_msg = '竟竟竟然手滑了没画出来...主人大人请原谅我喵...(翻滚)'
            else:
                reply_msg = '手滑了没画出来喵...(抠鼻孔)'
            # reply_msg += ' ...我这就重新画喵！'
            add_text(reply_msg, msg)
            await send_group_msg(status.ws, req.group_id, msg)
            status.generating = False
            # Retry on fail (may cause repeatedly sending messages).
            # status.jump_the_queue(req)
            continue

        add_img(img_path, msg)
        # Obtain seed.
        seed_p = re.compile(r's-(\d+)')
        seed_m = seed_p.search(img_path)
        seed = seed_m.groups()[0]
        reply_msg = MeowMsgs.get_finished_draw(req, seed, req.sender_id == MASTER_ID)
        add_text(reply_msg, msg)
        await send_group_msg(status.ws, req.group_id, msg)
        # Record last request for each user.
        status.prev_reqs[req.sender_id] = req
        status.generating = False
        status.counter += 1

        await asyncio.sleep(0.1)


def add_at(at_target: str, msg: list):
    msg.append(
        {
            "type": "at",
            "data": {
                "qq": at_target,
            }
        },
    )


def add_text(text: str, msg: list):
    msg.append(
        {
            'type': 'text',
            'data': {
                'text': text,
            }
        },
    )


def add_img(img_path: str, msg: list):
    msg.append(
        {
            'type': 'image',
            'data': {
                'file': 'file:///' + img_path,
            }
        }
    )


def generate_img(req: ImgGenReq, auth):
    seed = random.randint(0, 2 ** 32)
    try:
        # headers = {'authorization': 'Bearer ' + auth,
        #            'content-type': 'application/json'}

        # Generate image.
        img_gen_data = {'input': req.tags,
                        'model': req.model,
                        'parameters': {
                            'seed': req.seed or seed,
                            'n_samples': 1,
                            'sampler': req.sampler,
                            'width': req.width,
                            'height': req.height,
                            'scale': req.scale,
                            'steps': req.steps,
                            'uc': req.uc,
                            'ucPreset': 0,
                        }
                        }

        # Temporary google colab:
        google_colab_img_gen_data = {
            'height': req.height,
            'n_samples': 1,
            'prompt': req.tags,
            'sampler': req.sampler,
            'scale': req.scale,
            'seed': req.seed or seed,
            'steps': req.steps,
            'uc': req.uc,
            'ucPreset': 0,
            'width': req.width,
        }

        # img_gen_api_request = requests.post(img_gen_endpoint, json=img_gen_data, headers=headers)
        img_gen_api_request = requests.post(google_colab_endpoint, json=google_colab_img_gen_data)

        img_gen_output = img_gen_api_request.content
        image64 = img_gen_output[27:-2]
        img = base64.b64decode(image64)
        filename = 's-' + str(seed) + '.png'
        os.makedirs(OUTPUT_PATH, exist_ok=True)
        img_path = OUTPUT_PATH + filename
        with open(img_path, 'wb') as f:
            f.write(img)
        logger.info(filename + ' generated under path ' + OUTPUT_PATH + '.')

        # Obtain points.
        # obtain_points_api_request = requests.get(subscription_endpoint, headers=headers)
        # sub_output = obtain_points_api_request.json()
        # points = sub_output['trainingStepsLeft']
        # points_by_sub = points['fixedTrainingStepsLeft']
        # points_purchased = points['purchasedTrainingSteps']
        # req.points_left = points_by_sub + points_purchased
        req.points_left = 0

        return img_path
    except Exception as err:
        logger.error(err)
        return ''


if __name__ == '__main__':
    app.run(debug=True, auto_reload=True)
