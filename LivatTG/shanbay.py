import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
print(os.path.dirname(os.getcwd()))
from common.models.dao import FsaDao
from common.models.msgs import ShanbayMsg
import telegram
import asyncio
BotNanme = "TranslatorBot"
from utils.env_utils import init_custom_env, root_dir
init_custom_env(flag="prod", botname=BotNanme)

from utils.logger_utils import get_logger
logger = get_logger()

from utils.env_utils import tg_token, chat_id
bot = telegram.Bot(token=tg_token)
from common.models.msgs import db, app
fsa_dao = FsaDao(db=db, app=app)

import execjs

# https://twitter.com/yihong0618/status/1649433890032082944
# 解密 https://github.com/yihong0618/shanbay_remember/blob/main/shanbay.js
js_code = '''
class Func {
static loop(cnt, func) {
    "v"
    .repeat(cnt)
    .split("")
    .map((_, idx) => func(idx));
}
}

class Num {
static get(num) {
    return num >>> 0;
}

static xor(a, b) {
    return this.get(this.get(a) ^ this.get(b));
}

static and(a, b) {
    return this.get(this.get(a) & this.get(b));
}

static mul(a, b) {
    const high16 = ((a & 0xffff0000) >>> 0) * b;
    const low16 = (a & 0x0000ffff) * b;
    return this.get((high16 >>> 0) + (low16 >>> 0));
}

static or(a, b) {
    return this.get(this.get(a) | this.get(b));
}

static not(a) {
    return this.get(~this.get(a));
}

static shiftLeft(a, b) {
    return this.get(this.get(a) << b);
}

static shiftRight(a, b) {
    return this.get(a) >>> b;
}

static mod(a, b) {
    return this.get(this.get(a) % b);
}
}

const MIN_LOOP = 8;
const PRE_LOOP = 8;

const BAY_SH0 = 1;
const BAY_SH1 = 10;
const BAY_SH8 = 8;
const BAY_MASK = 0x7fffffff;

class Random {
constructor() {
    this.status = [];
    this.mat1 = 0;
    this.mat2 = 0;
    this.tmat = 0;
}

seed(seeds) {
    Func.loop(4, (idx) => {
    if (seeds.length > idx) {
        this.status[idx] = Num.get(seeds.charAt(idx).charCodeAt());
    } else {
        this.status[idx] = Num.get(110);
    }
    });

    [, this.mat1, this.mat2, this.tmat] = this.status;

    this.init();
}

init() {
    Func.loop(MIN_LOOP - 1, (idx) => {
    this.status[(idx + 1) & 3] = Num.xor(
        this.status[(idx + 1) & 3],
        idx +
        1 +
        Num.mul(
            1812433253,
            Num.xor(
            this.status[idx & 3],
            Num.shiftRight(this.status[idx & 3], 30)
            )
        )
    );
    });

    if (
    (this.status[0] & BAY_MASK) === 0 &&
    this.status[1] === 0 &&
    this.status[2] === 0 &&
    this.status[3] === 0
    ) {
    this.status[0] = 66;
    this.status[1] = 65;
    this.status[2] = 89;
    this.status[3] = 83;
    }

    Func.loop(PRE_LOOP, () => this.nextState());
}

nextState() {
    let x;
    let y;

    [, , , y] = this.status;
    x = Num.xor(
    Num.and(this.status[0], BAY_MASK),
    Num.xor(this.status[1], this.status[2])
    );
    x = Num.xor(x, Num.shiftLeft(x, BAY_SH0));
    y = Num.xor(y, Num.xor(Num.shiftRight(y, BAY_SH0), x));
    [, this.status[0], this.status[1]] = this.status;
    this.status[2] = Num.xor(x, Num.shiftLeft(y, BAY_SH1));
    this.status[3] = y;
    this.status[1] = Num.xor(
    this.status[1],
    Num.and(-Num.and(y, 1), this.mat1)
    );
    this.status[2] = Num.xor(
    this.status[2],
    Num.and(-Num.and(y, 1), this.mat2)
    );
}

generate(max) {
    this.nextState();

    let t0;

    [, , , t0] = this.status;
    const t1 = Num.xor(this.status[0], Num.shiftRight(this.status[2], BAY_SH8));
    t0 = Num.xor(t0, t1);
    t0 = Num.xor(Num.and(-Num.and(t1, 1), this.tmat), t0);

    return t0 % max;
}
}

class Node {
constructor() {
    this.char = ".";
    this.children = {};
}

getChar() {
    return this.char;
}

getChildren() {
    return this.children;
}

setChar(char) {
    this.char = char;
}

setChildren(k, v) {
    this.children[k] = v;
}
}

const B32_CODE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";
const B64_CODE =
"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
const CNT = [1, 2, 2, 2, 2, 2];

class Tree {
constructor() {
    this.random = new Random();
    this.sign = "";
    this.inter = {};
    this.head = new Node();
}

init(sign) {
    this.random.seed(sign);
    this.sign = sign;

    Func.loop(64, (i) => {
    this.addSymbol(B64_CODE[i], CNT[parseInt((i + 1) / 11, 10)]);
    });
    this.inter["="] = "=";
}

addSymbol(char, len) {
    let ptr = this.head;
    let symbol = "";

    Func.loop(len, () => {
    let innerChar = B32_CODE[this.random.generate(32)];
    while (
        innerChar in ptr.getChildren() &&
        ptr.getChildren()[innerChar].getChar() !== "."
    ) {
        innerChar = B32_CODE[this.random.generate(32)];
    }

    symbol += innerChar;
    if (!(innerChar in ptr.getChildren())) {
        ptr.setChildren(innerChar, new Node());
    }

    ptr = ptr.getChildren()[innerChar];
    });

    ptr.setChar(char);
    this.inter[char] = symbol;
    return symbol;
}

decode(enc) {
    let dec = "";
    for (let i = 4; i < enc.length; ) {
    if (enc[i] === "=") {
        dec += "=";
        i++;
        continue; // eslint-disable-line
    }
    let ptr = this.head;
    while (enc[i] in ptr.getChildren()) {
        ptr = ptr.getChildren()[enc[i]];
        i++;
    }
    dec += ptr.getChar();
    }

    return dec;
}
}

const getIdx = (c) => {
const x = c.charCodeAt();
if (x >= 65) {
    return x - 65;
}
return x - 65 + 41;
};

const VERSION = 1;

const checkVersion = (s) => {
const wi = getIdx(s[0]) * 32 + getIdx(s[1]);
const x = getIdx(s[2]);
const check = getIdx(s[3]);

return VERSION >= (wi * x + check) % 32;
};

const decode = (enc) => {
if (!checkVersion(enc)) {
    return "";
}

const tree = new Tree();
tree.init(enc.substr(0, 4));
const rawEncode = tree.decode(enc);
let buff = Buffer.from(rawEncode, "base64");
return JSON.parse(buff.toString("utf8"));
};
function shanbay_decode(str) {
    return decode(str);
}
'''

import base64
import requests

# def decode(data):
#     return base64.b64decode(data).decode()

root_url = 'https://apiv3.shanbay.com'
from utils.env_utils import shanbay_cookie
shanbay_cookie = shanbay_cookie
import json

def get_materialbookid():
    """
    获取当前的materialbookid
    """
    current_pth = '/wordsapp/user_material_books/current'
    resp = requests.get(
        f"{root_url}{current_pth}",
        cookies={'cookie': shanbay_cookie}
        )
    # print(resp.json())
    return resp.json()["data"]

def get_data(materialbookId="rkvzi", page=1, typeof="NEW"):
    """
    获取数据, 按page请求
    """
    pth = f"/wordsapp/user_material_books/{materialbookId}/learning/words/today_learning_items?ipp=10&page={page}&type_of={typeof}"
    resp = requests.get(
        f"{root_url}{pth}",
        cookies={'cookie': shanbay_cookie}
        )
    return resp.json()["data"]

ctx = execjs.compile(js_code)
def decode(data):
    """
    调用js代码解析数据
    """
    result = ctx.call('shanbay_decode', data)
    return result

def get_words(json_data):
    """
    解析json数据，获取单词
    :param json_data: json data
    """
    words = []
    for obj in json_data["objects"]:
        words.append(obj["vocab_with_senses"]["word"])
    return "\n".join(words)

from utils.openai_utils import Openai
def get_story(words):
    """
    调用openai生成故事
    words: 单词 str
    """
    logger.debug(f"openai input: {words}")
    messages =[
            {"role": "system", "content": "You are a writer, you are writing a story."},
            {"role": "user", "content": f"Please write a short story which is less than 300 words, the story should use simple words and these special words must be included: {words}. Also surround every special word with a single '*' character at the beginning and the end."},
        ]
    openai_obj = Openai()
    result = []
    resp = openai_obj.chat_complete(messages)
    for r in resp:
        one = r.choices[0].delta.content if 'content' in r.choices[0].delta else ''
        # print(one)
        result.append(one)
    res = "".join(result)
    logger.debug(f"openai output: {res}")
    return res

from utils.trans_text_audio import edge_tts

async def pipeline():
    try:
        data = get_data()
        json_data = decode(data=data)
        words = get_words(json_data=json_data)
        story = get_story(words=words)
        async with bot:
            await bot.send_message(text=words, chat_id=chat_id, parse_mode="Markdown")
        async with bot:
            await bot.send_message(text=story, chat_id=chat_id, parse_mode="Markdown")
        fsa_dao.save_obj(ShanbayMsg(words=words, story= story))
        article_name="review"
        voice_pth = f"{root_dir}/data/{article_name}_article.mp3"
        edge_tts(text=story, voice_pth=voice_pth)
        async with bot:
            with open(voice_pth, 'rb') as audio:
                await bot.send_voice(chat_id=chat_id, voice=audio)
    except Exception as e:
        logger.error(e)
        async with bot:
             await bot.send_message(text="shanbay_generate_error", chat_id=chat_id, parse_mode="Markdown")

if __name__ == "__main__":
    asyncio.run(pipeline())
