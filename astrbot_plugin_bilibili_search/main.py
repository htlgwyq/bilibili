Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
import aiohttp
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Plain, Image

@register("bilibili_search", "YourName", "B站视频搜索插件", "1.0.0", "搜索B站视频")
class BilibiliSearch(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # B站搜索API，这个是公开的简单API，如果失效了你得自己去找新的！
        self.search_api = "https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={}"

    @filter.command("bsearch")
    async def bsearch(self, event: AstrMessageEvent, keyword: str):
        '''搜索B站视频。指令格式：/bsearch 关键词'''
        if not keyword:
            yield event.plain_result("喂！你这笨蛋，连关键词都不输入，我怎么帮你搜啊？！")
            return

        yield event.plain_result(f"哼，等着，本小姐正在帮你搜【{keyword}】...别催！")

        try:
            async with aiohttp.ClientSession() as session:
                # 加上 User-Agent，不然B站会以为你是坏机器人把你踹出来！
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                }
                async with session.get(self.search_api.format(keyword), headers=headers) as resp:
...                     if resp.status != 200:
...                         yield event.plain_result("请求失败了，B站不理我！你这笨蛋是不是搜了什么奇怪的东西？")
...                         return
...                     
...                     data = await resp.json()
...                     
...                     if data.get("code") != 0:
...                         yield event.plain_result("B站报错了，你自己看着办吧！")
...                         return
... 
...                     results = data.get("data", {}).get("result", [])
...                     if not results:
...                         yield event.plain_result("什么都没搜到！你这关键词也太冷门了吧！")
...                         return
... 
...                     # 只取前三个，发太多会被企鹅制裁的！
...                     top_results = results[:3]
...                     
...                     for item in top_results:
...                         # B站返回的标题里有高亮标签，得去掉，不然难看死了
...                         title = item.get("title", "").replace("<em class=\"keyword\">", "").replace("</em>", "")
...                         pic_url = "https:" + item.get("pic", "") if item.get("pic", "").startswith("//") else item.get("pic", "")
...                         bvid = item.get("bvid", "")
...                         video_url = f"https://www.bilibili.com/video/{bvid}"
...                         
...                         # 组装消息发给你
...                         chain = [
...                             Image.fromURL(pic_url),
...                             Plain(f"\n标题：{title}\n链接：{video_url}")
...                         ]
...                         yield event.chain_result(chain)
... 
...         except Exception as e:
...             yield event.plain_result(f"出错了！都怪你！报错信息：{str(e)}")
... 
