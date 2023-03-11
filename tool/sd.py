import json
import shutil
import time
from random import Random

from requests.auth import HTTPBasicAuth

from config import conf
import requests
frp_file_host = conf().get('frp_file_url')
pre_progress_api = conf().get('sd_remote_host') + '/internal/progress'
sd_fn_index = int(conf().get('sd_fn_index'))
sd_relate_scale = int(conf().get('sd_relate_scale'))
sd_batch_size = int(conf().get('sd_batch_size'))
sd_step = int(conf().get('sd_step'))

call_api = conf().get('sd_remote_host') + '/run/predict/'
frp_file_path = 'frp_file_host'
progress_body = {"id_task": None,
                 "id_live_preview": 0}
fixed_negative_prompt = "(extremely detailed CG 8k wallpaper), (an extremely delicate and beautiful), (masterpiece), (best quality:1.0), (ultra highres:1.0),best quality,(ultra-detailed),1girl, beautiful,wading, medium breasts, "
fixed_positive_prompt = "nsfw,(worst quality:2), (low quality:2), (normal quality:2), (mutated hands and fingers:1.5 ), (long body :1.3), (mutation, poorly drawn :1.2) , black-white, bad anatomy, liquid body, liquid tongue, disfigured, malformed, mutated, anatomical nonsense, text font ui, error, malformed hands, long neck, blurred, lowers, lowres, bad anatomy, bad proportions, bad shadow, uncoordinated body, unnatural body, fused breasts, bad breasts, huge breasts, poorly drawn breasts, extra breasts, liquid breasts, heavy breasts, missing breasts, huge haunch, huge thighs, huge calf, bad hands, fused hand, missing hand,"
predict_body = {
    "fn_index": sd_fn_index,
    "data": [
        "",
        "",
        "",
        [

        ],
        sd_step,
        "Euler a",
        False,
        False,
        1,
        sd_batch_size,
        sd_relate_scale,
        -1,
        -1,
        0,
        0,
        0,
        False,
        800,
        800,
        False,
        0.7,
        2,
        "Latent",
        0,
        0,
        0,
        [

        ],
        "None",
        False,
        "none",
        "None",
        1,
        None,
        False,
        "Scale to Fit (Inner Fit)",
        False,
        False,
        64,
        64,
        64,
        0.9,
        5,
        "0.0001",
        False,
        "None",
        "",
        0.1,
        False,
        False,
        False,
        "positive",
        "comma",
        0,
        False,
        False,
        "",
        "Seed",
        "",
        "Nothing",
        "",
        "Nothing",
        "",
        True,
        False,
        False,
        False,
        0,
        "Not set",
        True,
        True,
        "",
        "",
        "",
        "",
        "",
        1.3,
        "Not set",
        "Not set",
        1.3,
        "Not set",
        1.3,
        "Not set",
        1.3,
        1.3,
        "Not set",
        1.3,
        "Not set",
        1.3,
        "Not set",
        1.3,
        "Not set",
        1.3,
        "Not set",
        1.3,
        "Not set",
        False,
        "None",
        [
            {
                "name": "H:\\program\\stable-diffusion-webui_23-02-17\\outputs\\txt2img-grids\\2023-03-11\\grid-0001.png",
                "data": "file=H:\\program\\stable-diffusion-webui_23-02-17\\outputs\\txt2img-grids\\2023-03-11\\grid-0001.png",
                "is_file": True
            },
            {
                "name": "H:\\program\\stable-diffusion-webui_23-02-17\\outputs\\txt2img-images\\2023-03-11\\00004-1385186721.png",
                "data": "file=H:\\program\\stable-diffusion-webui_23-02-17\\outputs\\txt2img-images\\2023-03-11\\00004-1385186721.png",
                "is_file": True
            },
            {
                "name": "H:\\program\\stable-diffusion-webui_23-02-17\\outputs\\txt2img-images\\2023-03-11\\00005-1385186722.png",
                "data": "file=H:\\program\\stable-diffusion-webui_23-02-17\\outputs\\txt2img-images\\2023-03-11\\00005-1385186722.png",
                "is_file": True
            },
            {
                "name": "H:\\program\\stable-diffusion-webui_23-02-17\\outputs\\txt2img-images\\2023-03-11\\00006-1385186723.png",
                "data": "file=H:\\program\\stable-diffusion-webui_23-02-17\\outputs\\txt2img-images\\2023-03-11\\00006-1385186723.png",
                "is_file": True
            },
            {
                "name": "H:\\program\\stable-diffusion-webui_23-02-17\\outputs\\txt2img-images\\2023-03-11\\00007-1385186724.png",
                "data": "file=H:\\program\\stable-diffusion-webui_23-02-17\\outputs\\txt2img-images\\2023-03-11\\00007-1385186724.png",
                "is_file": True
            }
        ],
        "{\"prompt\": \"(extremely detailed CG 8k wallpaper), (an extremely delicate and beautiful), (masterpiece), (best quality:1.0), (ultra highres:1.0),best quality,(ultra-detailed),1girl, beautiful,wading, medium breasts, <hypernet:vaporwave by\\u6db2\\u4f53:1>\", \"all_prompts\": [\"(extremely detailed CG 8k wallpaper), (an extremely delicate and beautiful), (masterpiece), (best quality:1.0), (ultra highres:1.0),best quality,(ultra-detailed),1girl, beautiful,wading, medium breasts, <hypernet:vaporwave by\\u6db2\\u4f53:1>\", \"(extremely detailed CG 8k wallpaper), (an extremely delicate and beautiful), (masterpiece), (best quality:1.0), (ultra highres:1.0),best quality,(ultra-detailed),1girl, beautiful,wading, medium breasts, <hypernet:vaporwave by\\u6db2\\u4f53:1>\", \"(extremely detailed CG 8k wallpaper), (an extremely delicate and beautiful), (masterpiece), (best quality:1.0), (ultra highres:1.0),best quality,(ultra-detailed),1girl, beautiful,wading, medium breasts, <hypernet:vaporwave by\\u6db2\\u4f53:1>\", \"(extremely detailed CG 8k wallpaper), (an extremely delicate and beautiful), (masterpiece), (best quality:1.0), (ultra highres:1.0),best quality,(ultra-detailed),1girl, beautiful,wading, medium breasts, <hypernet:vaporwave by\\u6db2\\u4f53:1>\"], \"negative_prompt\": \"(worst quality:2), (low quality:2), (normal quality:2), (mutated hands and fingers:1.5 ), (long body :1.3), (mutation, poorly drawn :1.2) , black-white, bad anatomy, liquid body, liquid tongue, disfigured, malformed, mutated, anatomical nonsense, text font ui, error, malformed hands, long neck, blurred, lowers, lowres, bad anatomy, bad proportions, bad shadow, uncoordinated body, unnatural body, fused breasts, bad breasts, huge breasts, poorly drawn breasts, extra breasts, liquid breasts, heavy breasts, missing breasts, huge haunch, huge thighs, huge calf, bad hands, fused hand, missing hand,\", \"all_negative_prompts\": [\"(worst quality:2), (low quality:2), (normal quality:2), (mutated hands and fingers:1.5 ), (long body :1.3), (mutation, poorly drawn :1.2) , black-white, bad anatomy, liquid body, liquid tongue, disfigured, malformed, mutated, anatomical nonsense, text font ui, error, malformed hands, long neck, blurred, lowers, lowres, bad anatomy, bad proportions, bad shadow, uncoordinated body, unnatural body, fused breasts, bad breasts, huge breasts, poorly drawn breasts, extra breasts, liquid breasts, heavy breasts, missing breasts, huge haunch, huge thighs, huge calf, bad hands, fused hand, missing hand,\", \"(worst quality:2), (low quality:2), (normal quality:2), (mutated hands and fingers:1.5 ), (long body :1.3), (mutation, poorly drawn :1.2) , black-white, bad anatomy, liquid body, liquid tongue, disfigured, malformed, mutated, anatomical nonsense, text font ui, error, malformed hands, long neck, blurred, lowers, lowres, bad anatomy, bad proportions, bad shadow, uncoordinated body, unnatural body, fused breasts, bad breasts, huge breasts, poorly drawn breasts, extra breasts, liquid breasts, heavy breasts, missing breasts, huge haunch, huge thighs, huge calf, bad hands, fused hand, missing hand,\", \"(worst quality:2), (low quality:2), (normal quality:2), (mutated hands and fingers:1.5 ), (long body :1.3), (mutation, poorly drawn :1.2) , black-white, bad anatomy, liquid body, liquid tongue, disfigured, malformed, mutated, anatomical nonsense, text font ui, error, malformed hands, long neck, blurred, lowers, lowres, bad anatomy, bad proportions, bad shadow, uncoordinated body, unnatural body, fused breasts, bad breasts, huge breasts, poorly drawn breasts, extra breasts, liquid breasts, heavy breasts, missing breasts, huge haunch, huge thighs, huge calf, bad hands, fused hand, missing hand,\", \"(worst quality:2), (low quality:2), (normal quality:2), (mutated hands and fingers:1.5 ), (long body :1.3), (mutation, poorly drawn :1.2) , black-white, bad anatomy, liquid body, liquid tongue, disfigured, malformed, mutated, anatomical nonsense, text font ui, error, malformed hands, long neck, blurred, lowers, lowres, bad anatomy, bad proportions, bad shadow, uncoordinated body, unnatural body, fused breasts, bad breasts, huge breasts, poorly drawn breasts, extra breasts, liquid breasts, heavy breasts, missing breasts, huge haunch, huge thighs, huge calf, bad hands, fused hand, missing hand,\"], \"seed\": 1385186721, \"all_seeds\": [1385186721, 1385186722, 1385186723, 1385186724], \"subseed\": 1904636448, \"all_subseeds\": [1904636448, 1904636449, 1904636450, 1904636451], \"subseed_strength\": 0, \"width\": 608, \"height\": 600, \"sampler_name\": \"Euler a\", \"cfg_scale\": 7, \"steps\": 30, \"batch_size\": 4, \"restore_faces\": false, \"face_restoration_model\": null, \"sd_model_hash\": \"168144a879\", \"seed_resize_from_w\": 0, \"seed_resize_from_h\": 0, \"denoising_strength\": null, \"extra_generation_params\": {}, \"index_of_first_image\": 1, \"infotexts\": [\"(extremely detailed CG 8k wallpaper), (an extremely delicate and beautiful), (masterpiece), (best quality:1.0), (ultra highres:1.0),best quality,(ultra-detailed),1girl, beautiful,wading, medium breasts, <hypernet:vaporwave by\\u6db2\\u4f53:1>\\nNegative prompt: (worst quality:2), (low quality:2), (normal quality:2), (mutated hands and fingers:1.5 ), (long body :1.3), (mutation, poorly drawn :1.2) , black-white, bad anatomy, liquid body, liquid tongue, disfigured, malformed, mutated, anatomical nonsense, text font ui, error, malformed hands, long neck, blurred, lowers, lowres, bad anatomy, bad proportions, bad shadow, uncoordinated body, unnatural body, fused breasts, bad breasts, huge breasts, poorly drawn breasts, extra breasts, liquid breasts, heavy breasts, missing breasts, huge haunch, huge thighs, huge calf, bad hands, fused hand, missing hand,\\nSteps: 30, Sampler: Euler a, CFG scale: 7, Seed: 1385186721, Size: 608x600, Model hash: 168144a879, Model: anyhentai_18, Clip skip: 2, ENSD: 31337\", \"(extremely detailed CG 8k wallpaper), (an extremely delicate and beautiful), (masterpiece), (best quality:1.0), (ultra highres:1.0),best quality,(ultra-detailed),1girl, beautiful,wading, medium breasts, <hypernet:vaporwave by\\u6db2\\u4f53:1>\\nNegative prompt: (worst quality:2), (low quality:2), (normal quality:2), (mutated hands and fingers:1.5 ), (long body :1.3), (mutation, poorly drawn :1.2) , black-white, bad anatomy, liquid body, liquid tongue, disfigured, malformed, mutated, anatomical nonsense, text font ui, error, malformed hands, long neck, blurred, lowers, lowres, bad anatomy, bad proportions, bad shadow, uncoordinated body, unnatural body, fused breasts, bad breasts, huge breasts, poorly drawn breasts, extra breasts, liquid breasts, heavy breasts, missing breasts, huge haunch, huge thighs, huge calf, bad hands, fused hand, missing hand,\\nSteps: 30, Sampler: Euler a, CFG scale: 7, Seed: 1385186721, Size: 608x600, Model hash: 168144a879, Model: anyhentai_18, Clip skip: 2, ENSD: 31337\", \"(extremely detailed CG 8k wallpaper), (an extremely delicate and beautiful), (masterpiece), (best quality:1.0), (ultra highres:1.0),best quality,(ultra-detailed),1girl, beautiful,wading, medium breasts, <hypernet:vaporwave by\\u6db2\\u4f53:1>\\nNegative prompt: (worst quality:2), (low quality:2), (normal quality:2), (mutated hands and fingers:1.5 ), (long body :1.3), (mutation, poorly drawn :1.2) , black-white, bad anatomy, liquid body, liquid tongue, disfigured, malformed, mutated, anatomical nonsense, text font ui, error, malformed hands, long neck, blurred, lowers, lowres, bad anatomy, bad proportions, bad shadow, uncoordinated body, unnatural body, fused breasts, bad breasts, huge breasts, poorly drawn breasts, extra breasts, liquid breasts, heavy breasts, missing breasts, huge haunch, huge thighs, huge calf, bad hands, fused hand, missing hand,\\nSteps: 30, Sampler: Euler a, CFG scale: 7, Seed: 1385186722, Size: 608x600, Model hash: 168144a879, Model: anyhentai_18, Clip skip: 2, ENSD: 31337\", \"(extremely detailed CG 8k wallpaper), (an extremely delicate and beautiful), (masterpiece), (best quality:1.0), (ultra highres:1.0),best quality,(ultra-detailed),1girl, beautiful,wading, medium breasts, <hypernet:vaporwave by\\u6db2\\u4f53:1>\\nNegative prompt: (worst quality:2), (low quality:2), (normal quality:2), (mutated hands and fingers:1.5 ), (long body :1.3), (mutation, poorly drawn :1.2) , black-white, bad anatomy, liquid body, liquid tongue, disfigured, malformed, mutated, anatomical nonsense, text font ui, error, malformed hands, long neck, blurred, lowers, lowres, bad anatomy, bad proportions, bad shadow, uncoordinated body, unnatural body, fused breasts, bad breasts, huge breasts, poorly drawn breasts, extra breasts, liquid breasts, heavy breasts, missing breasts, huge haunch, huge thighs, huge calf, bad hands, fused hand, missing hand,\\nSteps: 30, Sampler: Euler a, CFG scale: 7, Seed: 1385186723, Size: 608x600, Model hash: 168144a879, Model: anyhentai_18, Clip skip: 2, ENSD: 31337\", \"(extremely detailed CG 8k wallpaper), (an extremely delicate and beautiful), (masterpiece), (best quality:1.0), (ultra highres:1.0),best quality,(ultra-detailed),1girl, beautiful,wading, medium breasts, <hypernet:vaporwave by\\u6db2\\u4f53:1>\\nNegative prompt: (worst quality:2), (low quality:2), (normal quality:2), (mutated hands and fingers:1.5 ), (long body :1.3), (mutation, poorly drawn :1.2) , black-white, bad anatomy, liquid body, liquid tongue, disfigured, malformed, mutated, anatomical nonsense, text font ui, error, malformed hands, long neck, blurred, lowers, lowres, bad anatomy, bad proportions, bad shadow, uncoordinated body, unnatural body, fused breasts, bad breasts, huge breasts, poorly drawn breasts, extra breasts, liquid breasts, heavy breasts, missing breasts, huge haunch, huge thighs, huge calf, bad hands, fused hand, missing hand,\\nSteps: 30, Sampler: Euler a, CFG scale: 7, Seed: 1385186724, Size: 608x600, Model hash: 168144a879, Model: anyhentai_18, Clip skip: 2, ENSD: 31337\"], \"styles\": [], \"job_timestamp\": \"20230311001932\", \"clip_skip\": 2, \"is_using_inpainting_conditioning\": false}",
        "<p>(extremely detailed CG 8k wallpaper), (an extremely delicate and beautiful), (masterpiece), (best quality:1.0), (ultra highres:1.0),best quality,(ultra-detailed),1girl, beautiful,wading, medium breasts, &lt;hypernet:vaporwave by液体:1&gt;<br>\nNegative prompt: (worst quality:2), (low quality:2), (normal quality:2), (mutated hands and fingers:1.5 ), (long body :1.3), (mutation, poorly drawn :1.2) , black-white, bad anatomy, liquid body, liquid tongue, disfigured, malformed, mutated, anatomical nonsense, text font ui, error, malformed hands, long neck, blurred, lowers, lowres, bad anatomy, bad proportions, bad shadow, uncoordinated body, unnatural body, fused breasts, bad breasts, huge breasts, poorly drawn breasts, extra breasts, liquid breasts, heavy breasts, missing breasts, huge haunch, huge thighs, huge calf, bad hands, fused hand, missing hand,<br>\nSteps: 30, Sampler: Euler a, CFG scale: 7, Seed: 1385186721, Size: 608x600, Model hash: 168144a879, Model: anyhentai_18, Clip skip: 2, ENSD: 31337</p>",
        "<p></p><div class='performance'><p class='time'>Time taken: <wbr>10.43s</p><p class='vram'>Torch active/reserved: 2841/3738 MiB, <wbr>Sys VRAM: 6012/12288 MiB (48.93%)</p></div>"
    ],
    "session_hash": "9zlacr3glj"
}

def download_file(url, file_name):
    # create response object
    r = requests.get(url, auth=HTTPBasicAuth('abc', 'abc'))
    # download started
    with open(file_name, 'wb') as f:
        f.write(r.content)
# 生成12位随机字符串
def random_str(randomlength=12):
    str = ''
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def query_progress(task_id, preview_id):
    body = json.loads(json.dumps(progress_body))
    id_task = 'task({})'.format(task_id)
    body['id_task'] = id_task
    body['id_live_preview'] = preview_id
    response = requests.post(pre_progress_api, json=body)
    print(response.text)
    return response.json()


def preprocess():
    task_id = random_str()
    id_task = 'task({})'.format(task_id)
    res = query_progress(id_task, 0)
    if not res['queued']:
        return task_id
    return None


def query_status_when_complete(task_id):
    while True:
        time.sleep(2)
        response = query_progress(task_id, -1)
        print(json.dumps(response, indent=4))


def call_predict(negative_prompt, positive_prompt=''):
    task_id = preprocess()
    if task_id is None:
        return None
    id_task = 'task({})'.format(task_id)
    body = json.loads(json.dumps(predict_body))
    data = body['data']
    data[0] = id_task
    data[1] = fixed_negative_prompt + negative_prompt
    data[2] = fixed_positive_prompt + positive_prompt
    response = requests.post(call_api, json=body)
    response_data = response.json()['data']
    paths = response_data[0]
    grid_path = paths[0]['name']
    # 拷贝文件到本地
    download_url = calc_path(grid_path)
    print(download_url)
    return download_url
    # download_file(download_url, '{}.png'.format(task_id))



def calc_path(path):
    # find the index of 'outputs' in the path
    index = path.find('outputs')
    # get the path after 'outputs'
    path = path[index:]
    # 把\ 替换成/
    path = path.replace('\\', '/')
    return frp_file_host + path


if __name__ == '__main__':
    call_predict('a beautiful girl walking in water, wear a new white skirt,looking at viewer', '')
