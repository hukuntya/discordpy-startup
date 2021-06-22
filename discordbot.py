from discord.ext import commands
import os
import traceback
import time
import random
bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


class Nko():
    async def __init__(self):
        self.round = 1
        self.umc = [0, 0, 0]
        self.diceleft = 3
        self.nudges = 5
        self.dice = 5
        self.hiscore = 0
    
    async def reset(self):
        self.round = 1
        self.umc = [0, 0, 0]
        self.diceleft = 3
        self.nudges = 5
        self.dice = 5

    async def roll(self):
        self.round += 1
        self.diceleft -= 1
        result = []
        core = ["う", "ま", "ち", "ん", "こ", "お"]
        for _ in range(self.dice):
            if random.randrange(100) < 970:
                result.append(core[random.randrange(6)])
            else:
                result.append("・")
        return result
    
    async def nudge(self):
        self.nudges -= 1
        result = []
        core = ["う", "ま", "ち", "ん", "こ", "お"]
        for _ in range(self.dice):
            if random.randrange(1000) < 968:
                result.append(core[random.randrange(6)])
            else:
                result.append("・")
        return result

    async def check(self, result, ctx):
        self.umc[0] += result.count("う") * 500
        self.umc[1] += result.count("ま") * 500
        self.umc[2] += result.count("ち") * 500
        self.umc = list(map(lambda n: n + result.count("ん") * 50, self.umc))
        self.umc = list(map(lambda n: n + result.count("こ") * 100, self.umc))
        self.umc = list(map(lambda n: n + result.count("お") * 300, self.umc))
        self.umc = list(map(lambda n: n - result.count("・") * 500, self.umc))
    
        next = -1

        # うんち
        if result.count("う") >= 1 and result.count("ん") >= 1 and result.count("ち") >= 1:
            ctx.send("UNCHI")
            next += 1
            self.umc[0] += 1000
        # うんこ
        if result.count("う") >= 1 and result.count("ん") >= 1 and result.count("こ") >= 1:
            ctx.send("UNKO")
            next += 1
            self.umc[0] += 1000
        # おまんこ
        if result.count("お") >= 1 and result.count("ま") >= 1 and result.count("ん") >= 1 and result.count("こ") >= 1:
            ctx.send("OMANKO")
            next += 1
            self.umc[1] += 5000
        # まんこ
        elif result.count("ま") >= 1 and result.count("ん") >= 1 and result.count("こ") >= 1:
            ctx.send("MANKO")
            next += 1
            self.umc[1] += 1000
        # ちんこ
        if result.count("ち") >= 1 and result.count("ん") >= 1 and result.count("こ") >= 1:
            ctx.send("CHINKO")
            next += 1
            self.umc[2] += 1000
        # おちんちん
        if result.count("お") >= 1 and result.count("ち") >= 2 and result.count("ん") >= 2:
            ctx.send("O C H I N C H I N")
            next = 10
            self.umc[2] += 10000
        # ちんちん
        elif result.count("ち") >= 2 and result.count("ん") >= 2:
            ctx.send("CHINCHIN")
            next += 1
            self.umc[2] += 3000
        
        if next > 0:
            self.dice = 5 + next
        else:
            self.dice = 5
        
        if next >= 0:
            self.diceleft += 1
        
        self.nudges += next + 1
            

        # ううう
        count = result.count("う")
        if count >= 3:
            bonus = count - 3
            if bonus > 4: bonus = 4
            self.umc[0] *= (2 + bonus)
            ctx.send("".join(["う" for _ in range(count)]))
        
        # ままま
        count = result.count("ま")
        if count >= 3:
            bonus = count - 3
            if bonus > 4: bonus = 4
            self.umc[1] *= (2 + bonus)
            ctx.send("".join(["ま" for _ in range(count)]))

        # ちちち
        count = result.count("ち")
        if count >= 3:
            bonus = count - 3
            if bonus > 4: bonus = 4
            self.umc[2] *= (2 + bonus)
            ctx.send("".join(["ち" for _ in range(count)]))
        
        # んんん
        count = result.count("ん")
        if count >= 3:
            bonus = count - 3
            if bonus > 4: bonus = 4
            self.umc = list(map(lambda n: n * -(3 + bonus), self.umc))
            ctx.send("".join(["ん" for _ in range(count)]))
        
        # こここ
        count = result.count("こ")
        if count >= 3:
            bonus = count - 3
            if bonus > 4: bonus = 4
            self.umc = list(map(lambda n: n * (1.5 + bonus), self.umc))
            ctx.send("".join(["こ" for _ in range(count)]))

        # おおお
        count = result.count("お")
        if count >= 3:
            bonus = count - 3
            if bonus > 4: bonus = 4
            self.umc = list(map(lambda n: n * (1.5 + bonus), self.umc))
            self.umc = list(map(lambda n: abs(n), self.umc))
            ctx.send("".join(["お" for _ in range(count)]))
        
        self.umc = list(map(int, self.umc))

UMC = Nko()

@bot.command()
async def dice(ctx):
    if UMC.diceleft > 0:
        await ctx.send(f"ROUND:{UMC.round} DICE:{UMC.dice} LEFT DICE:{UMC.diceleft}")
        time.sleep(1)
        nk = UMC.roll()
        await ctx.send("：".join(nk))
        time.sleep(1)
        UMC.check(nk, ctx)
        time.sleep(2)
        await ctx.send(f"U:{UMC.umc[0]} M:{UMC.umc[1]} C:{UMC.umc[2]}\nSCORE: {UMC.umc[0] + UMC.umc[1] + UMC.umc[2]}")
    if UMC.diseleft = 0:
        time.sleep(1)
        if (UMC.umc[0] + UMC.umc[1] + UMC.umc[2]) > UMC.hiscore:
            UMC.hiscore = UMC.umc[0] + UMC.umc[1] + UMC.umc[2]
        ctx.send(f"GAME OVER\nU:{UMC.umc[0]} M:{UMC.umc[1]} C:{UMC.umc[2]}\nSCORE: {UMC.umc[0] + UMC.umc[1] + UMC.umc[2]} HI SCORE: {UMC.hiscore}")
        UMC.reset()

@bot.command()
async def ping(ctx):
    await ctx.send('pong')


        
client.run(os.environ['DISCORD_BOT_TOKEN'])
