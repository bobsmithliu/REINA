import asyncio

import discord
from discord.ext import commands
import datetime
import pytz
import time
import bs4
import aiohttp
import random
from textblob import TextBlob

import TOKEN

bot_description = '''
R.E.I.N.A. 1.20

Roles and Entertainment Information and Notification Agent

Open source at: https://github.com/Skk-nsmt/REINA
Licensed under WTFPL
'''
bot = commands.Bot(command_prefix='>', description=bot_description, case_insensitive=True)

# -----------------------------------
# |                                 |
# |       Below are constants       |
# |                                 |
# -----------------------------------

jptz = pytz.timezone('Asia/Tokyo')
universaltz = pytz.timezone('UTC')
pacifictz = pytz.timezone('America/Los_Angeles')
centraltz = pytz.timezone('America/Chicago')
easterntz = pytz.timezone('America/New_York')

sub_roles_id = {
    'Tamago': 497370840824807424,
    'Tsubomi': 497369993428729856,
    'Ainacchi': 466163376779689985,
    'Yuki': 497369955181002765,
    'Rettan': 466163341031637002,
    'Mikami': 497369641241411584,
    'Moe': 466163363756638209,
    'Ayaka': 466163285318828032,
    'Reinyan': 466163253232402432,
    'Reika': 466163208315731968,
    'Chiharun': 466163143983366145,
    'Nicole': 466163118695776266,
    'Meimei': 466163049217261570,
    'Miu': 466162997971255296,
    'Nagomin': 466162947807248386,
    'Akane': 466162927758737409,
    'Kanaeru': 466162902349643786,
    'Miyako': 466162830371192832,
    'Mizzy': 466162802692980737,
    'Jun': 466162727598161931,
    'Ruri': 466162700880183307,
    'Sakura': 466162595817193482,
    'Sally': 466162519447437312,
    'Uta': 659171909723750405,
    'Gouda': 689628756968472576,
    'Kaoruko': 691153598884741131,
    'Nana': 691153793626144779,
    'Miko': 691154105208537168
}
main_roles_id = {
    'Tamago': 497370864254320670,
    'Tsubomi': 497370023397163008,
    'Ainacchi': 466160683185340426,
    'Yuki': 497369857042677768,
    'Rettan': 466160640428343298,
    'Mikami': 497369717175222284,
    'Moe': 466160644341628929,
    'Ayaka': 466160548128620554,
    'Reinyan': 466160517044502578,
    'Reika': 466160400405102593,
    'Chiharun': 466160373855420418,
    'Nicole': 466160288564117515,
    'Meimei': 466160266451877892,
    'Miu': 466160184725864448,
    'Nagomin': 466160116534607875,
    'Akane': 466160086583083008,
    'Kanaeru': 466160011996037122,
    'Miyako': 466159974125404171,
    'Mizzy': 466159885629784064,
    'Jun': 466159852532531210,
    'Ruri': 466159773604249611,
    'Sakura': 466159732235829249,
    'Sally': 466159611179958273,
    'Uta': 659171144028520475,
    'Gouda': 689629655548035156,
    'Kaoruko': 691153281820524605,
    'Nana': 691153662415863849,
    'Miko': 691154027534221323
}

acceptable_roles = main_roles_id.keys()

stream_links = {
    'Chiharu': ['Hokaze Chiharu', 'https://www.showroom-live.com/digital_idol_2', discord.Color.red()],
    'Ruri': ['Umino Ruri', 'https://www.showroom-live.com/digital_idol_4', discord.Color.green()],
    'Mei': ['Hanakawa Mei', 'https://www.showroom-live.com/digital_idol_7', discord.Color.blue()],
    'Uta': ['Kawase Uta', 'https://www.showroom-live.com/kawaseuta', discord.Color.blue()],
    'Reina': ['Miyase Reina', 'https://www.showroom-live.com/digital_idol_9', discord.Color.dark_magenta()],
    'Sally': ['Amaki Sally', 'https://www.showroom-live.com/digital_idol_11', discord.Color.gold()],
    'Aina': ['Takeda Aina', 'https://www.showroom-live.com/digital_idol_15', discord.Color.teal()],
    'Kanae': ['Shirosawa Kanae', 'https://www.showroom-live.com/digital_idol_18', discord.Color.purple()],
    'Urara': ['Takatsuji Urara', 'https://www.showroom-live.com/digital_idol_19',
              discord.Color.from_rgb(230, 136, 242)],
    'Moe': ['Suzuhana Moe', 'https://www.showroom-live.com/digital_idol_20', discord.Color.magenta()],
    'Mizuha': ['Kuraoka Mizuha', 'https://www.showroom-live.com/digital_idol_21', discord.Color.orange()],
    'Nagomi': ['Saijo Nagomi', 'https://www.showroom-live.com/digital_idol_22', discord.Color.from_rgb(220, 248, 250)],
    'Nananiji': ['Group Stream', 'https://www.showroom-live.com/nanabunno', discord.Color.blue()]
}

lyrics = {
    "僕は存在していなかった":
        ["僕は自分を信じていない \n自分の存在　知られたくなかった",
         "風が吹く日は　その風が止むまで \n部屋から出るなんて考えたこともない",
         "心の窓にはカーテンを引いて \n世界の隅でそっと息をしてた",
         "夢見るってことは　何かを期待すること \n傷つくくらいなら　夢なんか見たくない",
         "僕は色を持たない花 \n君とまたすれ違っても \nきっと僕を思い出せないだろう \n好きと言ってはダメなんだ",
         "青い空よりどこまでも澄んだ \n自由の意味を知るやさしい眼差しで",
         "孤独な窓を何度も叩いて \n世界の広さ君は教えてくれた",
         "必要とされるのは生きてる意味を感じる \n雨風に打たれても生まれ変われる",
         "僕も色を持ってた花 \nやっと今さら気づいたよ \n君が僕に光をくれたんだ \n好きと言ってもいいのかな",
         "すべては他人事 (ひとごと) のようでも \n君だけは愛を見捨てずに \nどこからか　僕を呼ぶ声が聴こえる",
         "他の花と比べていた \nずっと一人絶望して \nどんな花も色があるように \n僕には僕の色がある",
         "僕は自分を信じ始めた \n今なら好きだと言えるかもしれない"],
    "やさしい記憶":
        ["狭い校庭のフェンスの脇 \n咲いてた花の名前 なんて言ったっけ？ \nみんな知らなくて調べたんだ \n僕の植物図鑑 片隅に載ってた",
         "忘れることって便利だと思う \nクラスメイトの誰かまで \nどこかに消えてしまったよ",
         "やさしい記憶なんて あやふやで \nこれ以上 僕のこと傷つけはしない \n悲しいことは きっと勘違い \n人に聞いたのを信じ込んだだけ \n終わったことなんか終わったままでいいよ",
         "夏の教室の日差しの中 \n窓際の君のこと いつも盗み見た \n何も言い出せず 秋になって \nやがて心の花も枯れてしまったよ",
         "覚えてないのは悲しいからだろう \n過ぎた月日の思いやり \nあの日の自分は嫌いだ",
         "ホントの記憶 どこかぼんやりと \n切ないベールで守ってくれてる \n真実なんてどうだっていいことなのか？ \n人はそう過去を美化してしまうよ \n未来はいつだって上書きのためにある",
         "やさしい記憶なんて あやふやで \nこれ以上 僕のこと傷つけはしない \n大事なことは ある日 振り向けば \nほんの一瞬だけ 思い出すものさ \nどうでもいいことなんかどこにもないと知った"],
    "未来があるから":
        ["誰かに手首をぎゅっと掴まれて \n行くなと言われて引き留められる \nそういう経験したことあるかい？ \nもちろん愛だとわかってはいても…",
         "抵抗したのはなぜだったのか？ \n腕を振り切ったのは　プライドに似た変な意地だ",
         "君が思ってるより　僕はいい人じゃない \n嘘はついていないけど正直でもない \n君が知ってる僕は　本当の僕じゃない \n自分でも呆れるほど自分が好きになれない",
         "未来があるからいいじゃない？ \n振り向きざま \n僕に言うつもりか",
         "事実がどうでも関係ないなんて \n勝手な理屈と思ってしまう \n何より大事な基準はいつでも \n白とか黒とか二つに一つだ",
         "逃走したのはどうしてなのか？ \n裏切られたとしても　そう簡単に傷つくものか？",
         "君が信じてくれても　僕は悪い人間だ \n愛が真実かなんてどうでもいいこと \n君の知らない僕が　この世界にいたんだ \nさあ今なら間に合うよ　すべてを忘れて欲しい",
         "未来というのはでまかせだ \n目を見ながら \nちゃんと言えるのかなあ"],
    "何もしてあげられない":
        ["一枚の枝の葉が吹き抜ける風に揺れ\nひらひらと宙を舞い　舗道へと落ちて行く",
         "そう僕は偶然にその場所に居合わせて\n知らぬ間に罪もない他人 (ひと) のこと踏んでいる",
         "誰かの嘆きや痛みに\n耳を傾けることなく\n傲慢に生きて来て\nごめんなさい",
         "何もしてあげられなくて　遠巻きに見るしかなくて\n涙どれだけ流しても他人事だろう",
         "僕が生きてるその意味を　ずっと考えてみたけど\nただ一つ願ってた君のことさえ守れなかった",
         "人混みを避けながら　今までは歩いてた\nぶつかってしまったら悪いって思ってた\nでもそれは　本当のやさしさと違うんだ\n気づかずに傷つけることだってあったはず",
         "意識してるかしてないか\n人間 (ひと) は迷惑かけるもの\n友達は欲しくない\nいけませんか？",
         "何も望んでなどいない　愛なんて面倒だった\nだってきっと愛されたら愛すべきだろう",
         "僕が拒否してた世界　ドアを頑なに閉めてた\nそう助け求めてた君を孤独に突き放したまま",
         "残酷なアスファルトに消えた君のその叫び\nどこかから聴こえるよ\n踏んでしまった運命よ",
         "何もしてあげられなくて　遠巻きに見るしかなくて\n涙どれだけ流しても他人事だろう",
         "僕が生きてるその意味を　ずっと考えてみたけど\nただ一つ願ってた君のことさえ守れなかった"],
    "ムズイ":
        ["「大人たちは簡単に言うけど… \n私にとっての希望って　どこにあるの？」",
         "途切れることのない車の往来に \n国道　渡れなかった \n誰かの言葉とか　冷たい眼差しに \n心が萎縮するように…",
         "夢なんかを見ていたって \n傷つくだけだと身にしみた",
         "「自分がどこにいるのかわからない　何も見えない世界で途方に暮れている \nどっちに向かって進めばいいの？もうどこへも歩きたくない」",
         "ねえどうして　(人は)　生きていかなきゃいけないの？　(教えて) \n命って　(命って)　何のためにあるの？",
         "自信がない　(私)　これからどう生きればいい？　(孤独よ) \nだって人生が長すぎる \n「ムズイよ」",
         "教室のカーテン　漏らしたため息に \n何度も膨らみ萎 (しぼ) む \nつまらない授業もただのクラスメイトも \n何にも興味が持てない",
         "日常から逃げ出すには \n一つしか方法がなかった",
         "「優しい言葉なんか掛けないで　叶わない夢ばかり見てしまうから \nはっきり言って欲しい　すべては幻想なんだと」",
         "ねえどうして (人は)　死にたくなっちゃいけないの？　(教えて) \n誰だって　(誰だって)　考えるでしょう？",
         "私なんて　(きっと)　このままいなくなればいい　(さよなら) \n何を信じて生きるのだろう",
         "なりたかった自分も　なれなかった自分も \n窓ガラスに映った泣いている自分も　全部自分だ",
         "人は誰でも変われるって \n夢なんか見せないでよ"]

}


# Constants ends here

# Checking functions


def check_if_bot_spam():
    async def predicate(ctx):
        bot_channel = ctx.guild.get_channel(336287198510841856)
        return ctx.channel == bot_channel

    return commands.check(predicate)


def check_if_role_or_bot_spam():
    async def predicate(ctx):
        bot_channel = ctx.guild.get_channel(336287198510841856)
        role_channel = discord.utils.get(ctx.guild.channels, name='roles')
        return ctx.channel == bot_channel or ctx.channel == role_channel

    return commands.check(predicate)


@bot.listen()
async def on_ready():
    print('Ready!')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(">help"))


@bot.listen()
async def on_message(message):
    # don't respond to ourselves
    if message.author == bot.user:
        return
    if "reina" in message.content.lower():
        text = TextBlob(message.content.lower())
        if text.polarity >= 0.2:
            await message.add_reaction('♥️')
        if text.polarity <= -0.2:
            await message.add_reaction('💔')


class Default(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @check_if_bot_spam()
    async def hi(self, ctx):
        """
        Let R.E.I.N.A. greet you!
        """
        await ctx.send("Hi! {}".format(ctx.author.display_name))

    @commands.command()
    @check_if_bot_spam()
    async def rand_lyrics(self, ctx):
        """
        Print out random lyrics from 22/7 songs.
        """
        random_song = random.choice(list(lyrics.keys()))
        random_lyrics = "\n> ".join(("> " + random.choice(lyrics[random_song])).split("\n"))

        await ctx.send("*{}* \nーー *「{}」*".format(random_lyrics, random_song))

    @hi.error
    async def command_error(self, ctx, error):
        bot_channel = ctx.guild.get_channel(336287198510841856)
        if isinstance(error, commands.CheckFailure):
            message = await ctx.send('Please proceed your action at {} (deletion in 5s)'.format(bot_channel.mention))
            await asyncio.sleep(1)
            for i in range(4, 0, -1):
                await message.edit(
                    content="Please proceed your action at {} (deletion in {}s)".format(bot_channel.mention, i))
                await asyncio.sleep(1)
            await message.delete()
            await ctx.message.delete()


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @check_if_role_or_bot_spam()
    async def role(self, ctx, role_type, role_name):
        """
        Add a role.

        role_type: Use 'main' or 'sub' to indicate which type of role you want. Your main role will control your nametag colour.
        role_name: The name of your role. (Case-insensitive)

        E.g.: ">role main Sally" will add Sally as your main role and make your nametag yellow.
        E.g.: ">role sub Mizzy" will add Mizzy as a sub role without affecting your nametag colour.

        Only the following roles may be added:
        Sally, Sakura, Ruri, Jun, Mizzy, Miyako, Kanaeru, Akane, Nagomin, Miu, Meimei, Uta, Nicole, Chiharun, Reika, Reinyan, Ayaka, Moe, Mikami, Rettan, Yuki, Ainacchi, Tsubomi, Tamago, Gouda, Kaoruko, Nana, Miko
        """
        role_name = role_name.capitalize()

        if role_name in acceptable_roles:
            if role_type == 'main':
                role_ids = [role.id for role in ctx.author.roles]
                main_roles = list(set(role_ids) & set(main_roles_id.values()))

                role = ctx.guild.get_role(main_roles_id[role_name])

                if role in ctx.author.roles:
                    await ctx.send("You already have that role!")
                elif main_roles:
                    await ctx.send("You can't have more than one main role!")
                else:
                    await ctx.author.add_roles(role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(
                        datetime.datetime.utcnow()))
                    await ctx.send("Role added.")
            elif role_type == 'sub':
                role = ctx.guild.get_role(sub_roles_id[role_name])

                if role in ctx.author.roles:
                    await ctx.send("You already have that role!")
                else:
                    await ctx.author.add_roles(role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(
                        datetime.datetime.utcnow()))
                    await ctx.send("Role added.")
            else:
                await ctx.send("Illegal operation.")
        else:
            await ctx.send("Illegal role name. Type `>help role` for a list of acceptable role names. ")

    @commands.command()
    @check_if_role_or_bot_spam()
    async def unrole(self, ctx, role_type, role_name):
        """
        Delete a role.

        role_type: Use 'main' or 'sub' to indicate which type of role you wish to delete. If you delete your main role, your nametag colour will change to that of your highest sub role until you add a new main role.
        role_name: The name of your role. (Case-insensitive)

        E.g.: ">unrole main Sally" will remove Sally as your main role. If, say, you have Meimei as a sub role, your nametag colour will then be light blue until you add a new main role.

        Only the following roles may be deleted:
        Sally, Sakura, Ruri, Jun, Mizzy, Miyako, Kanaeru, Akane, Nagomin, Miu, Meimei, Uta, Nicole, Chiharun, Reika, Reinyan, Ayaka, Moe, Mikami, Rettan, Yuki, Ainacchi, Tsubomi, Tamago, Gouda, Kaoruko, Nana, Miko
        """
        role_name = role_name.capitalize()

        if role_name in acceptable_roles:
            if role_type == 'main':
                role = ctx.guild.get_role(main_roles_id[role_name])
            elif role_type == 'sub':
                role = ctx.guild.get_role(sub_roles_id[role_name])
            else:
                await ctx.send("Illegal operation.")
                return

            if role not in ctx.author.roles:
                await ctx.send("You don't have that role!")
            else:
                await ctx.author.remove_roles(role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(
                    datetime.datetime.utcnow()))
                await ctx.send("Role removed.")

        else:
            await ctx.send("Illegal role name.")

    @role.error
    @unrole.error
    async def command_error(self, ctx, error):
        bot_channel = ctx.guild.get_channel(336287198510841856)
        if isinstance(error, commands.CheckFailure):
            message = await ctx.send('Please proceed your action at {} (deletion in 5s)'.format(bot_channel.mention))
            await asyncio.sleep(1)
            for i in range(4, 0, -1):
                await message.edit(
                    content="Please proceed your action at {} (deletion in {}s)".format(bot_channel.mention, i))
                await asyncio.sleep(1)
            await message.delete()
            await ctx.message.delete()


class Wariraji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @check_if_bot_spam()
    async def sub_wariraji(self, ctx):
        """
        Subscribe to Warikirenai Radio Plus notifications.
        """
        radio_role = ctx.guild.get_role(694627966495490078)
        if radio_role in ctx.author.roles:
            await ctx.send("You already have that role!")
        else:
            await ctx.author.add_roles(radio_role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(
                datetime.datetime.utcnow()))
            await ctx.send("You have subscribed to Warikirenai Radio Plus notifications.")

    @commands.command()
    @check_if_bot_spam()
    async def unsub_wariraji(self, ctx):
        """
        Unsubscribe to Warikirenai Radio Plus notifications.
        """
        radio_role = ctx.guild.get_role(694627966495490078)
        if radio_role not in ctx.author.roles:
            await ctx.send("You don't have that role!")
        else:
            await ctx.author.remove_roles(radio_role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(
                datetime.datetime.utcnow()))
            await ctx.send("You have unsubscribed to Warikirenai Radio Plus notifications.")

    @sub_wariraji.error
    @unsub_wariraji.error
    async def command_error(self, ctx, error):
        bot_channel = ctx.guild.get_channel(336287198510841856)
        if isinstance(error, commands.CheckFailure):
            message = await ctx.send('Please proceed your action at {} (deletion in 5s)'.format(bot_channel.mention))
            await asyncio.sleep(1)
            for i in range(4, 0, -1):
                await message.edit(
                    content="Please proceed your action at {} (deletion in {}s)".format(bot_channel.mention, i))
                await asyncio.sleep(1)
            await message.delete()
            await ctx.message.delete()


class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @check_if_bot_spam()
    async def sub_anime(self, ctx):
        """
        Subscribe to anime notifications.
        """
        anime_role = ctx.guild.get_role(668634086172131378)
        if anime_role in ctx.author.roles:
            await ctx.send("You already have that role!")
        else:
            await ctx.author.add_roles(anime_role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(
                datetime.datetime.utcnow()))
            await ctx.send("You have subscribed to anime notifications.")

    @commands.command()
    @check_if_bot_spam()
    async def unsub_anime(self, ctx):
        """
        Unsubscribe to anime notifications.
        """
        anime_role = ctx.guild.get_role(668634086172131378)
        if anime_role not in ctx.author.roles:
            await ctx.send("You don't have that role!")
        else:
            await ctx.author.remove_roles(anime_role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(
                datetime.datetime.utcnow()))
            await ctx.send("You have unsubscribed to anime notifications.")

    @sub_anime.error
    @unsub_anime.error
    async def command_error(self, ctx, error):
        bot_channel = ctx.guild.get_channel(336287198510841856)
        if isinstance(error, commands.CheckFailure):
            message = await ctx.send('Please proceed your action at {} (deletion in 5s)'.format(bot_channel.mention))
            await asyncio.sleep(1)
            for i in range(4, 0, -1):
                await message.edit(
                    content="Please proceed your action at {} (deletion in {}s)".format(bot_channel.mention, i))
                await asyncio.sleep(1)
            await message.delete()
            await ctx.message.delete()


class Keisanchuu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @check_if_bot_spam()
    async def sub_keisanchuu(self, ctx):
        """
        Subscribe to 22/7 Keisanchuu notifications.
        """
        keisanchuu_role = ctx.guild.get_role(641112458291052584)
        if keisanchuu_role in ctx.author.roles:
            await ctx.send("You already have that role!")
        else:
            await ctx.author.add_roles(keisanchuu_role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(
                datetime.datetime.utcnow()))
            await ctx.send("You have subscribed to 22/7 Keisanchuu notifications.")

    @commands.command()
    @check_if_bot_spam()
    async def unsub_keisanchuu(self, ctx):
        """
        Unsubscribe to 22/7 Keisanchuu notifications.
        """
        keisanchuu_role = ctx.guild.get_role(641112458291052584)
        if keisanchuu_role not in ctx.author.roles:
            await ctx.send("You don't have that role!")
        else:
            await ctx.author.remove_roles(keisanchuu_role, reason="R.E.I.N.A. bot action. Executed at {} UTC".format(
                datetime.datetime.utcnow()))
            await ctx.send("You have unsubscribed to 22/7 Keisanchuu notifications.")

    @sub_keisanchuu.error
    @unsub_keisanchuu.error
    async def command_error(self, ctx, error):
        bot_channel = ctx.guild.get_channel(336287198510841856)
        if isinstance(error, commands.CheckFailure):
            message = await ctx.send('Please proceed your action at {} (deletion in 5s)'.format(bot_channel.mention))
            await asyncio.sleep(1)
            for i in range(4, 0, -1):
                await message.edit(
                    content="Please proceed your action at {} (deletion in {}s)".format(bot_channel.mention, i))
                await asyncio.sleep(1)
            await message.delete()
            await ctx.message.delete()


class Mods(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @commands.has_any_role('Moderators', 'Disciplinary Committee')
    async def protect(self, ctx):
        """
        (Mod-only command) Do mystery things.
        Note: this is an on-off switch command.
        """
        global new_member_loaded

        if new_member_loaded:
            bot.unload_extension("authentication")
            new_member_loaded = False
            await ctx.send("Unloaded. ")
        else:
            bot.load_extension("authentication")
            new_member_loaded = True
            await ctx.send("Loaded. ")

    @commands.command()
    @commands.has_any_role('Moderators', 'Disciplinary Committee')
    @check_if_bot_spam()
    async def announce(self, ctx, person, date, planned_time):
        """
        (Mod-only command) Make stream announcements.

        Make stream announcements at #227 streams.

        person: use members' first name, or use "Nananiji" for Nananiji Room stream.
        date: use either "today" or "tomorrow" to indicate whether the stream is happening today or tomorrow.
        planned_time: "<two_digit_hour>:<two_digit_minute>" format in 24Hr standard.

        Please note that when executing the command, the stream will need to be happening TODAY in Japan.
        """
        stream_channel = discord.utils.get(ctx.guild.channels, name='227-streams')
        await stream_channel.trigger_typing()

        headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.62 Safari/537.36",
            'Referer': "https://www.showroom-live.com"
        }

        if person in stream_links:
            now = datetime.datetime.now(jptz)

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(stream_links[person][1], headers=headers) as r:
                        if r.status == 200:
                            page = bs4.BeautifulSoup(await r.text(), "html.parser")

                parsed_time = time.strptime(planned_time, "%H:%M")

                stream_time = jptz.localize(datetime.datetime(year=now.year,
                                                              month=now.month,
                                                              day=now.day,
                                                              hour=parsed_time.tm_hour,
                                                              minute=parsed_time.tm_min))

                if date == "tomorrow":
                    stream_time = stream_time + datetime.timedelta(days=1)
                else:
                    pass

                announcement_embed = discord.Embed(title="**{}**".format(stream_links[person][0]),
                                                   type='rich',
                                                   description='{}'.format(stream_links[person][1]),
                                                   color=stream_links[person][2])

                announcement_embed.add_field(name='Japan Time',
                                             value='{}'.format(stream_time.strftime("%Y-%m-%d %I:%M%p")))
                announcement_embed.add_field(name='Universal Time',
                                             value='{}'.format(
                                                 stream_time.astimezone(universaltz).strftime("%Y-%m-%d %I:%M%p")))
                announcement_embed.add_field(name='Eastern Time',
                                             value='{}'.format(
                                                 stream_time.astimezone(easterntz).strftime("%Y-%m-%d %I:%M%p")))
                announcement_embed.add_field(name='Central Time',
                                             value='{}'.format(
                                                 stream_time.astimezone(centraltz).strftime("%Y-%m-%d %I:%M%p")))
                announcement_embed.add_field(name='Pacific Time',
                                             value='{}'.format(
                                                 stream_time.astimezone(pacifictz).strftime("%Y-%m-%d %I:%M%p")))

                announcement_embed.set_author(name='Upcoming Stream',
                                              icon_url="https://www.showroom-live.com/assets/img/v3/apple-touch-icon.png")
                announcement_embed.set_image(url=page.find("meta", attrs={"property": "og:image"})['content'])

                announcement_embed.set_footer(text='Sent by {}'.format(ctx.author.display_name),
                                              icon_url=ctx.author.avatar_url)

                stream_msg = await stream_channel.send(embed=announcement_embed)

                await stream_msg.pin()
            except ValueError:
                await ctx.send("Something happened, please report it to the developer. ")

        else:
            await ctx.send("Illegal name.")

    @announce.error
    @protect.error
    async def command_error(self, ctx, error):
        bot_channel = ctx.guild.get_channel(336287198510841856)
        if isinstance(error, commands.CheckFailure):
            message = await ctx.send('Please proceed your action at {} (deletion in 5s)'.format(bot_channel.mention))
            await asyncio.sleep(1)
            for i in range(4, 0, -1):
                await message.edit(
                    content="Please proceed your action at {} (deletion in {}s)".format(bot_channel.mention, i))
                await asyncio.sleep(1)
            await message.delete()
            await ctx.message.delete()


bot.load_extension("authentication")
new_member_loaded = True

bot.add_cog(Default(bot))
bot.add_cog(Roles(bot))
bot.add_cog(Wariraji(bot))
bot.add_cog(Keisanchuu(bot))
# bot.add_cog(Anime(bot))
bot.add_cog(Mods(bot))
bot.run(TOKEN.TOKEN)
