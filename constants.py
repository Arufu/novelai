import re


class Const:
    def __init__(self):
        self.tags_delimiter = '[,，]'
        self.full_model = 'nai-diffusion'
        self.safe_model = 'safe-diffusion'
        self.default_model = self.safe_model
        self.default_sampler = 'ddim'
        self.default_steps = 28
        self.default_scale = 7
        self.H_W = {
            '横图': [512, 768],
            '竖图': [768, 512],
            '方图': [640, 640],
            # '大横图': [512, 1024],
            # '大竖图': [1024, 512],
            '大横图': [768, 1280],
            '大竖图': [1280, 768],
            '大方图': [960, 960],
        }
        self.forbidden_words = [
            # 'sexy',
            'sex',
            'nude',
            'nsfw',
            'penis',
            'pussy',
            'vaginal',
            'dick',
            'nipples',
            'questionable',
            'naked',
        ]
        self.at_me = ['[CQ:at,qq=2356429990]', '@日和小萝莉']
        self.master_id = 304029882
        self.full_model_ids = [
            self.master_id,
            # i佬
            2015667807,
            # poi
            1972742583,
            # 清
            1322019544,
            # ky
            694009079,
        ]
        self.max_num_pages = 4

        self.img_gen_shape_pattern = re.compile(r'.*?(?:画|做|来|弄|搞|生成).*?(横图|竖图|方图|大横图|大竖图|大方图).*')
        self.img_gen_tag_pattern = re.compile(r'.*标签.*?[<《]([^<《]+)[>》].*')
        self.img_gen_num_page_pattern = re.compile(r'.*?(\d+)[张幅个].*')
        self.img_gen_num_steps_pattern = re.compile(r'.*?\D+(\d+)[步].*')
        self.img_gen_sampler_pattern = re.compile(r'.*(?:sampler|采样|取样).*?(k_euler_ancestral|k_euler|k_lms|plms|ddim).*')
        self.img_gen_scale_pattern = re.compile(r'.*(?:画风|scale).*?(\d+).*')
        self.img_gen_uc_pattern = re.compile(r'.*?(?:不要|去除|排除|扣掉)[^标]*?[<《]([^<《]+)[>》].*')
        self.img_gen_seed_pattern = re.compile(r'.*?种子.*?(\d+).*')
        self.img_gen_safe_pattern = re.compile(r'.*?全年龄.*')
        self.img_gen_full_pattern = re.compile(r'.*?(完整图库|色图|瑟图|涩图|全图库).*')
        self.img_gen_low_priority_pattern = re.compile(r'.*?低优先.*')
        self.img_gen_extra_tag_pattern = re.compile(r'.*(?:附加|额外|另外|加上).*?[<《]([^<《]+)[>》].*')
        self.img_gen_clear_low_priority_queue_pattern = re.compile(r'.*?清空低优先.*')
        self.img_gen_clear_queue_pattern = re.compile(r'.*?清空队列.*')
        self.img_gen_queue_query_pattern = re.compile(r'.*?(队列情况|队列数|排队数|请求数).*')

        self.high_quality_pattern = re.compile(r'.*?高画质.*')

        self.blue_dragon_tags = 'Depth of field,highres,4k,high quality,delicate face,masterpiece,Cream white hair,Light blue eyes,twintails,lolita,Small crown,Gorgeous clothes,Black and red clothes,White and blue clothes, medium breasts,Princess Dress,Blue rose hair ornament,Full body portrait,Boots,White stockings, slender,couch,Hemline,lace,{{{{sexy}}}},'

        self.alic_tags = '((alice)),alice in wonderland,(((solo))),1girl,((delicate face)),vely long hair,blunt_bangs,(((full body))),(floating hair),(looking_at_viewer),open mouth,(looking_at_viewer),open mouth,blue eyes,Blonde_hair,Beautiful eyes,gradient hair,((white_frilled_dress)),((white pantyhose)), (long sleeves),(juliet_sleeves),(puffy sleeves),white hair bow,Skirt pleats,blue dress bow,blue_large_bow,(((stading))),(((arms behind back))),sleeves past wrists,sleeves past fingers,(forest),flowering hedge,scenery,Flowery meadow,clear sky,(delicate grassland),(blooming white roses),flying butterfly,shadow,beautiful sky,cumulonimbus,((absurdres)),incredibly_absurdres,huge_filesize,(best quality),(masterpiece),delicate details,refined rendering,original,official_art,10s,'
        self.hugging_a_o_l_tags = '{{{{masterpiece}}}}, best quality, illustration, 2girls,  beautiful detailed eyes,beautiful detailed sky, beautiful detailed water, cinematic lighting,dramatic angle,lace,sunshine, angel, blonde hair, small breasts, long hair, ahoge, white wings, halo, blue eyes, twin braids,wet clothes,lace, sad, {{crying}}, {{{{{twins}}}}}, mutual hug,'
        self.demi_god_mec = 'blasphemy,misterious,sacred,holy,divine,antichrist,illustration,{{Mechanical Monster}},{extremely detailed cg},non-humanoid,{{Remus GOD machine-Fenrir}},{masterpiece},powerful,extremely detailed CG unity 8K wallpaper,art of light,artist style,hyper machine,Tranformation by mechanization,Mechanical weapon,'
        self.demi_god_mec_girl = 'misterious,sacred,holy,divine,antichrist,illustration,{{Mechanical Monster}},non-humanoid,{{Remus GOD machine-Fenrir}},masterpiece,powerful,extremely detailed CG unity 8K wallpaper,art of light,artist style,hyper machine,Tranformation by mechanization,Mechanical weapon,{{{{{{{a girl}}}}}}}}，{{{{{{{solo}}}}}}},'
        self.ukiyoe_water_loli = '(ukiyoe style), loli, 1girl, solo, facing to the side, watercolor (medium), (hime_cut), black hair, butterfly hair ornament, long hair, red eyes, japanese clothes, small breasts, sakura, japan, blood, expressionless,bare shoulders, sexy,'

        self.high_quality_tags = 'masterpiece,highly detailed, {highres}, extremely detailed 8K wallpaper, {an extremely delicate and beautiful},masterpiece, best quality, illustration, beautifully detailed eyes, cinematic lighting, dramatic angles, high contrast,'

        self.tag_presets = {
            '青龙': self.blue_dragon_tags,
            '爱丽丝': self.alic_tags,
            '光水奶抱抱': self.hugging_a_o_l_tags,
            '机甲': self.demi_god_mec,
            '机娘': self.demi_god_mec_girl,
            '和风萝莉': self.ukiyoe_water_loli,
        }

        self.default_uc = 'malformed hands,worst quality,low quality,{{{{ugly}}}},{{{duplicate}}},{{{trans}}},{{trannsexual}},{out of frame},extra fingers,mutated hands,{{{more than 2 nipples}}},out of frame,ugly,extra limbs,{bad anatomy},grossproportions,{malformed limbs},{{missing arms}},{{missinglegs}},{{{extra arms}}},{{{extra legs}}},mutated hands,{fusedfingers},{too many fingers},{{{long neck}}},fingers,extra digit,cropped,bad feet,{{poorly drawnhands}},{{poorly drawn face}},{{{mutation}}},{{deformed}},blurry,{{bad anatomy}},{{{bad proportions}}},{{extralimbs}},{{{disfigured}}}.bad anatomy disfigured,malformed mutated,missing limb,normal quality,too many fingers,long neck,bad finglegs,cropped,bad feet,bad anatomy disfigured,malformed mutated,{{morbid}},{{mutilated}},{{{tranny}}},missing limb,malformed hands,'
