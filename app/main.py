from flask import Flask, render_template, request
from fake_useragent import UserAgent
from requests import get as r_get
from json import load, dump
from pathlib import Path
import os


APP_PATH: Path = Path(__file__).parent
print(f'Running in {APP_PATH} directory.')
CFG_FILE = APP_PATH/"config.json"
IMAGE_FOLDER = APP_PATH/'images/'
userAgent: UserAgent = UserAgent()

app = Flask(__name__)

if not os.path.exists(CFG_FILE):
    with open(CFG_FILE, "w") as f:
        dump({"pic_per_page": 20,
              "tape_scale": 1,
              "tags": ["female"],
              "neg_tags": ["zoophilia", "mlp"],
              "path": ".homework",
              "font_size": 18,
              "clear_cache": False,
              "shuffle_on_load": True,
              "from_folder": False,
              "autoload": True,
              "reputation": 0}, f)

with open(CFG_FILE, "r") as f:
    jloaa = load(f)
    items_count = jloaa["pic_per_page"]
    img_smaller = jloaa["tape_scale"]
    tags = set((*jloaa["tags"], *[f"-{i}" for i in jloaa["neg_tags"]]))
    font_size = jloaa["font_size"]
    uncacher = jloaa["clear_cache"]
    load_shuffle = jloaa["shuffle_on_load"]
    load_local = jloaa["from_folder"]
    minimal_rep = jloaa["reputation"]
    autonextpage = jloaa["autoload"]
    imagedir = jloaa["path"]


@app.route('/', methods=['GET'])
def index():
    images = []  # os.listdir(IMAGE_FOLDER)

    link34 = f"https://api.r34.app/booru/rule34.xxx/posts?baseEndpoint=rule34.xxx&" + '&'.join((f"{i}={j}" for i, j in request.args.items()))
    res = r_get(link34, headers={'User-Agent': userAgent.ff}).json()
    # links = [res["links"]['first'], res["links"]['prev'], res["links"]['self'], res["links"]['next'], res["links"]['last']]

    for messag in res["data"]:
        images.append(messag['low_res_file']['url'])

    return render_template('index.html', images=images)


@app.route('/images', methods=['GET'])
def tag_filter():
    print(request.args['tags'])
    return '200 OK'
