import json
from secrets import choice

import random
import requests

from pyAyiin import cmdHelp
from pyAyiin.decorator import ayiinCmd
from pyAyiin.utils import eod, eor

from . import cmd


category = ["classic", "kids", "party", "hot", "mixed"]


async def get_task(mode, choice):
    url = "https://psycatgames.com/api/tod-v2/"
    data = {
        "id": "truth-or-dare",
        "language": "id",
        "category": category[choice],
        "type": mode,
    }
    headers = {
        "referer": "https://psycatgames.com/app/truth-or-dare/?utm_campaign=tod_website&utm_source=tod_id&utm_medium=website"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()["results"]
    return random.choice(result)


@ayiinCmd(pattern="(task|truth|dare)(?: |$)([1-5]+)?$")
async def tod(event):
    tod = event.pattern_match.group(1)
    if tod == "task":
        xxnx = await eor(event, "`Processing...`")
        tod = choice(["truth", "dare"])
    else:
        xxnx = await eor(event, f"`Tugas {tod} acak untuk Anda...`")
    category = event.pattern_match.group(2)
    category = int(choice(category)) if category else random.choice([1, 2])
    try:
        task = await get_task(tod, category)
        if tod == "truth":
            await xxnx.edit(f"**Tugas Truth untuk Anda adalah**\n`{task}`")
        else:
            await xxnx.edit(f"**Tugas Dare untuk Anda adalah**\n`{task}`")
    except Exception as e:
        await eod(xxnx, f"**ERROR: `{e}`")


cmdHelp.update(
    {
        "games": f"**Plugin : **`games`\
        \n\n  »  **Perintah :** `{cmd}truth`\
        \n  »  **Kegunaan : **Memberikan anda tantangan kejujuran secara random.\
        \n\n  »  **Perintah :** `{cmd}dare`\
        \n  »  **Kegunaan : **Memberikan anda tantangan Keberanian secara random.\
        \n\n  »  **Perintah :** `{cmd}task`\
        \n  »  **Kegunaan : **Untuk Memberikan anda tantangan secara random.\
    "
    }
)
