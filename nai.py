import os
import time
from sys import path
from os import environ as env
from os.path import join, abspath, dirname
from novelai_api import NovelAI_API
from aiohttp import ClientSession
from logging import Logger, StreamHandler
from asyncio import run
import requests
import base64
import random


path.insert(0, abspath(join(dirname(__file__), '..')))
required_env_var = ["NAI_USERNAME", "NAI_PASSWORD", "QQ_USERNAME", "QQ_PASSWORD", "NAI_IMG_GEN_ENDPOINT"]

if any(env_var not in env for env_var in required_env_var):
    raise RuntimeError("Please ensure that all environment variables are set")

NAI_username = env["NAI_USERNAME"]
NAI_password = env["NAI_PASSWORD"]
QQ_username = env["QQ_USERNAME"]
QQ_password = env["QQ_PASSWORD"]
endpoint = env["NAI_IMG_GEN_ENDPOINT"]

logger = Logger("NAIBot")
logger.addHandler(StreamHandler())

OUTPUT_PATH = './output'
os.makedirs(OUTPUT_PATH, exist_ok=True)


async def main():
    async with ClientSession() as session:
        api = NovelAI_API(session, logger=logger)

        login = await api.high_level.login(NAI_username, NAI_password)
        logger.info(login)

        counter = 0
        while True:
            try:
                seed = random.randint(0, 2 ** 32)

                tags = "gothic lolita, facing away, standing on cliff, looking afar, visita, {{{{realistic}}}}, {{{{photorealistic}}}}"

                data = {"input": "masterpiece, best quality, " + tags,
                        "model": "nai-diffusion",
                        "parameters": {
                            "seed": seed,
                            "n_samples": 1,
                            "sampler": "k_euler_ancestral",
                            "width": 768,
                            "height": 512,
                            "scale": 11,
                            "steps": 28,
                            "uc": "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, "
                                  "cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark,"
                                  " username, blurry",
                            "ucPreset": 0,
                        }
                        }

                headers = {"authorization": "Bearer " + login,
                           "content-type": "application/json"}

                req = requests.post(endpoint, json=data, headers=headers)

                output = req.content
                image64 = output[27:-2]
                img = base64.b64decode(image64)

                tag_dir_path = OUTPUT_PATH + '/' + tags
                filename = "s-" + str(seed) + ".png"
                os.makedirs(tag_dir_path, exist_ok=True)
                with open(tag_dir_path + '/' + filename, "wb") as f:
                    f.write(img)
                logger.info(str(counter) + ": " + filename + " generated under path " + tag_dir_path + ".")
                counter = counter + 1

                time.sleep(3 + random.randint(0, 7))
            except Exception as err:
                logger.error(err)

run(main())
