## 源码不可使用及改编，允许者可行


import re

echotag={
    "echo": {"start": "```ansi\n", "end": "\n```\n"}, 
    "b": {"start": "**", "end": "**"},  
    "i": {"start": "*", "end": "*"},  
    "u": {"start": "__", "end": "__"},
    "hd": {"start": "||", "end": "||"},
    "s": {"start": "~~", "end": "~~"},
    "code": {"start": "`", "end": "`"},
    "style": lambda param, content: f"[{param}m{content}[0m",
    "codespace": lambda param, content: f"```{param}\n{content}\n```\n",
    "sp":{"start": " ", "end":""},
    "br":{"start": "\n", "end":""},
    "tb":{"start": "\t", "end":""},
    "nl":{"start": "", "end":""}
}

localtag={
    "sp":{"start": " ", "end":""},
    "br":{"start": "\n", "end":""},
    "tb":{"start": "\t", "end":""},
    "nl":{"start": "", "end":""}
}

idstag={
    "sp":{"start": " ", "end":""},
    "br":{"start": "\n", "end":""},
    "tb":{"start": "\t", "end":""},
    "nl":{"start": "", "end":""},
    
    "_lr":{"start": "⿰", "end":""},
    "_ll":{"start": "⿲", "end":""},
    "_ud":{"start": "⿱", "end":""},
    "_uu":{"start": "⿳", "end":""},
    "_rd":{"start": "⿸", "end":""},
    "_ld":{"start": "⿹", "end":""},
    "_ru":{"start": "⿺", "end":""},
    "_od":{"start": "⿵", "end":""},
    "_or":{"start": "⿷", "end":""},
    "_ou":{"start": "⿶", "end":""},
    "_oc":{"start": "⿴", "end":""},
    "_xx":{"start": "⿻", "end":""},
    "_mi":{"start": "⿾", "end":""},
    "_ro":{"start": "⿿", "end":""},
    "_su":{"start": "㇯", "end":""},
    "_tf":{"start": "!", "end":""},
}


def parse_bbcode(text,tagrule):
    
    TAG_RULES = tagrule
    
    # 正则表达式匹配BBCode标签
    pattern = re.compile(r'\[(\w+)(?:=([^\]]+))?\](.*?)(?=\[\/\1\]|\Z)|\[\/(\w+)\]', re.DOTALL)

    # 替换函数
    def replace(match):
        # 开始标签
        if match.group(1):
            tag_name = match.group(1)
            param = match.group(2)
            content = match.group(3)
            rule = TAG_RULES.get(tag_name)
            if callable(rule):
                # 参数化标签，直接处理内容
                return rule(param, content)
            elif isinstance(rule, dict):
                # 普通标签，递归解析内容
                return f"{rule['start']}{parse_bbcode(content,tagrule)}{rule['end']}"
        # 闭合标签
        elif match.group(4):
            return ""  # 删除闭合标签
        return match.group(0)  # 未知标签或错误

    # 使用正则替换所有BBCode标签
    result = re.sub(pattern, replace, text)
    return result

# --------------------------------

# 初始化bot

import discord, os, time
from discord.ext import commands
from urllib.parse import quote, unquote
from math import *
from random import randint

token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=">", intents=intents)


@bot.event
async def on_ready():
    print(f'[] Bot Logged in as {bot.user.name}')
    await bot.tree.sync()

@bot.hybrid_command()
async def ids(ctx, idscode: str = ""):
    """使用组字功能组字"""
    if idscode == "":
        await ctx.send("""
    ```ansi
    /ids [33m<idscode>[0m              

    Use IDS-code to make character (No Alphabet-IDS-code Format)               

    Format:    
        [31mLR[0m ↔ ⿰ 
        [31mLL[0m ↔ ⿲ 
        [31mUD[0m ↔ ⿱ 
        [31mUU[0m ↔ ⿳ 
        [31mRD[0m ↔ ⿸ 
        [31mLD[0m ↔ ⿹ 
        [31mRU[0m ↔ ⿺ 
        [31mOD[0m ↔ ⿵ 
        [31mOR[0m ↔ ⿷ 
        [31mOU[0m ↔ ⿶ 
        [31mOC[0m ↔ ⿴
        [31mXX[0m ↔ ⿻
        [31mMI[0m ↔ ⿾
        [31mRO[0m ↔ ⿿
        [31mSU[0m ↔ ㇯
        [31mTF[0m ↔ !
    ```
                       """)
    else:
        print(idscode)
        idscode=parse_bbcode(idscode,idstag)
        avalue = quote(idscode, 'utf-8')
        print(avalue)
        imageurl = f"http://zu.zi.tools/{avalue}.png"
        embed = discord.Embed()
        embed.set_image(url=imageurl)
        await ctx.send(f"[] Format: {idscode}")
        await ctx.send(embed=embed)

@bot.hybrid_command()
async def output(ctx, value: str = ""):
    """输出文本"""
    if value == "":
        await ctx.send("""
        ```ansi
    /output [33m<value>[0m
                       
    Print content
        ```
                       """)
    else:
        a=parse_bbcode(value,echotag)
        await ctx.send(a)

@bot.hybrid_command()
async def random(ctx, min: int = None, max: int = None):
    """给予大小值输出随机数字"""
    if min == None or max == None:
        await ctx.send("""
        ```ansi
    /random [33m<min=0>[0m [33m<max=100>[0m               

    Create a random number              
    ```
                       """)
    else:
        await ctx.send(randint(min, max))

@bot.hybrid_command()
async def uniint(ctx, char: str = ""):
    """将字符转换成数字"""
    if char == "":
        await ctx.send("""
        ```ansi
    /uniint [33m<char(1 Char)>[0m              

    Change character to number            
    ```
                       """)
    else:
        await ctx.send(ord(parse_bbcode(char,localtag)))


@bot.hybrid_command()
async def unihex(ctx, char: str = ""):
    """将字符转换成十六进制"""
    if char == "":
        await ctx.send("""
        ```ansi
    /unihex [33m<char(1 Char)>[0m              

    Change character to hex             
    ```
                       """)
    else:
        await ctx.send(hex(ord(parse_bbcode(char,localtag))))


@bot.hybrid_command()
async def unichr(ctx, hex: str = ""):
    """将十六进制转换成字符"""
    if hex == "":
        await ctx.send("""
        ```ansi
    /unichr [33m<hex(Hexcode)>[0m              

    Change hex to character              
    ```
                       """)
    else:
        await ctx.send(chr(int(hex, 16)))

INFO_LST = {"ver": "20250124 (重构)"}


@bot.hybrid_command()
async def info(ctx):
    """bot基本信息"""
    import datetime
    await ctx.send(f"""
    ```ansi
    [31m HaSouldev {INFO_LST["ver"]} [0m

    Make by [35m[1mH.S.S. - 寒沙 [0m
    ```
    """)

@bot.hybrid_command()
async def test(ctx):
    """测试bot基本性能"""
    await ctx.send("测试普通输出")
    await ctx.send("""
    ```ansi
    测试代码块及[33m高亮[0m输出
    ```
    """)
    imageurl = f"http://zu.zi.tools/⿰制图.png"
    embed = discord.Embed()
    embed.set_image(url=imageurl)
    await ctx.send(f"测试制图")
    await ctx.send(embed=embed)


@bot.hybrid_command()
async def charcc(ctx, min: str = "", max: str = ""):
    """输出从给予的最小值到给予的最大值的字符码"""
    plice = 256
    a = ""
    if min == "" or max == "":
        await ctx.send("""
        ```ansi
    /charcc [33m<min(Hex)>[0m [33m<max(Hex)>[0m            

    Character codeplace print          
    ```
                       """)
    else:
        ab = int(max, 16) - int(min, 16)
        if ab <= 0:
            await ctx.send("[] Error: Max must be bigger than min")
        else:
            cmin = int(min, 16)
            cmax = int(max, 16)
            for i in range(ab + 1):
                a += chr(cmin + i)
            await ctx.send(f"""
            ```ansi
{a}```""")


@bot.hybrid_command()
async def abtl(ctx, style: str = "", value: str = ""):
    """输出指定风格的花式字母"""
    warning_char = 0
    a = ""
    if style == "" or value == "":
        await ctx.send("""
            ```ansi
        /abtl [33m<style>[0m [33m<value>[0m            

        Character style print

        Arguments useful:
            style:
                'roundler' → 'ⓇⓄⓊⓃⒹⓁⒺⓇ'
                'squarer' → '🅂🅀🅄🄰🅁🄴🅁'
                'bold_serif' → '𝐁𝐎𝐋𝐃 𝐒𝐄𝐑𝐈𝐅'
                'italic_serif' → '𝑖𝑡𝑎𝑙𝑖𝑐 𝑠𝑒𝑟𝑖𝑓'
        ```
                           """)
    else:
        datav = list(value)
        if style == "roundler":
            for i in range(len(datav)):
                print(ord(datav[i]))
                if ord(datav[i]) >= 0x41 and ord(datav[i]) <= 0x5a:
                    a += chr(ord(datav[i]) + 0x2475)
                elif ord(datav[i]) >= 0x61 and ord(datav[i]) <= 0x7a:
                    a += chr(ord(datav[i]) + 0x246F)
                elif ord(datav[i]) >= 0x31 and ord(datav[i]) <= 0x39:
                    a += chr(ord(datav[i]) + 0x242f)
                elif ord(datav[i]) == 0x30:
                    a += "⓪"
                else:
                    a += datav[i]
        elif style == "squarer":
            for i in range(len(datav)):
                if ord(datav[i]) >= 0x41 and ord(datav[i]) <= 0x5a:
                    a += chr(ord(datav[i]) + 0x1F0ef)
                else:
                    a += datav[i]
        elif style == "bold_serif":
            for i in range(len(datav)):
                if ord(datav[i]) >= 0x41 and ord(datav[i]) <= 0x5a:
                    a += chr(ord(datav[i]) + 0x1D3BF)
                elif ord(datav[i]) >= 0x61 and ord(datav[i]) <= 0x7a:
                    a += chr(ord(datav[i]) + 0x1D3B9)
                elif ord(datav[i]) >= 0x30 and ord(datav[i]) <= 0x39:
                    a += chr(ord(datav[i]) + 0x1D79E)
                elif ord(datav[i]) >= 0x391 and ord(datav[i]) <= 0x3a1:
                    a += chr(ord(datav[i]) + 0x1D6A8 - 0x391)
                elif ord(datav[i]) >= 0x3A3 and ord(datav[i]) <= 0x3A9:
                    a += chr(ord(datav[i]) + 0x1D6BA - 0x3A3)
                elif ord(datav[i]) >= 0x3B1 and ord(datav[i]) <= 0x3C9:
                    a += chr(ord(datav[i]) + 0x1D6C2 - 0x3B1)
                elif ord(datav[i]) == 0x3F4:
                    a += "𝚹"
                elif ord(datav[i]) == 0x2202:
                    a += "𝛛"
                elif ord(datav[i]) == 0x3F5:
                    a += "𝛜"
                elif ord(datav[i]) == 0x3D1:
                    a += "𝛝"
                elif ord(datav[i]) == 0x3F0:
                    a += "𝛞"
                elif ord(datav[i]) == 0x3D5:
                    a += "𝛟"
                elif ord(datav[i]) == 0x3F1:
                    a += "𝛠"
                elif ord(datav[i]) == 0x3D6:
                    a += "𝛡"
                elif ord(datav[i]) == 0x2207:
                    a += "𝛁"
                elif ord(datav[i]) == 0x3DC:
                    a += "𝟊"
                elif ord(datav[i]) == 0x3DD:
                    a += "𝟋"
                else:
                    a += datav[i]
        elif style == "italic_serif":
            for i in range(len(datav)):
                if ord(datav[i]) >= 0x41 and ord(datav[i]) <= 0x5a:
                    a += chr(ord(datav[i]) + 0x1D434 - 0x41)

                elif ord(datav[i]) >= 0x61 and ord(datav[i]) <= 0x7a:
                    if ord(datav[i]) == 0x68:
                        a += "ℎ"
                    else:
                        a += chr(ord(datav[i]) + 0x1D44E - 0x61)

                elif ord(datav[i]) >= 0x391 and ord(datav[i]) <= 0x3a1:
                    a += chr(ord(datav[i]) + 0x1D6E2 - 0x391)

                elif ord(datav[i]) >= 0x3A3 and ord(datav[i]) <= 0x3A9:
                    a += chr(ord(datav[i]) + 0x1D6F4 - 0x3A3)

                elif ord(datav[i]) >= 0x3B1 and ord(datav[i]) <= 0x3C9:
                    a += chr(ord(datav[i]) + 0x1D6FC - 0x3B1)

                elif ord(datav[i]) == 0x3F4:
                    a += "𝛳"
                elif ord(datav[i]) == 0x2202:
                    a += "𝜕"
                elif ord(datav[i]) == 0x3F5:
                    a += "𝜖"
                elif ord(datav[i]) == 0x3D1:
                    a += "𝜗"
                elif ord(datav[i]) == 0x3F0:
                    a += "𝜘"
                elif ord(datav[i]) == 0x3D5:
                    a += "𝜙"
                elif ord(datav[i]) == 0x3F1:
                    a += "𝜚"
                elif ord(datav[i]) == 0x3D6:
                    a += "𝜛"
                elif ord(datav[i]) == 0x2207:
                    a += "𝛻"
                elif ord(datav[i]) == 0x131:
                    a += "𝚤"
                elif ord(datav[i]) == 0x237:
                    a += "𝚥"

                else:
                    a += datav[i]

        await ctx.send(f"""
                    `{a}`""")


bot.run(token)
