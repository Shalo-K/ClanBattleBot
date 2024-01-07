###### import #####
import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from util.fileController import AplConst

##### configの読み込み #####
aplPath = os.getcwd()
aplConst = AplConst(aplPath)

##### Cog一覧取得　 #####
cogs = aplConst.get("cogs")

##### Discordに接続 #####
load_dotenv()
token = os.getenv("TOKEN")

##### BotClientオブジェクト作成 #####
class ClanBattleBot(commands.Bot):
    def __init__(self, command_prefix, intents, application_id):
        # スーパークラスのコンストラクタに値を渡して実行。
        super().__init__(
            command_prefix
            ,case_insensitive = True
            ,help_command=None
            ,intents=intents
            ,application_id=application_id
        )
    
    async def setup_hook(self):
        # Cog情報を読み込み。
        for cog in cogs:
            await self.load_extension("cogs." + cog)
        # グローバルコマンドとして発行(使用できるまで、最大1時間程度かかる)
        await self.tree.sync()

# Botのインスタンス化および起動処理。
async def main():
    # Botの起動
    async with bot:
        await bot.start(token)

if __name__ == '__main__':
    intents = discord.Intents(
        guilds = True,
        members = True,
        messages = True,
        reactions = True,
        message_content = True
    )

    bot = ClanBattleBot(
            command_prefix = '/'
            ,intents=intents
            ,application_id=aplConst.get("id.client")
        )
    
    ##### イベント処理 #####
    @bot.event
    async def on_ready():
        # 起動時に動作する処理
        print("ログインしました")

    @bot.event
    async def on_raw_reaction_add(message):
        # リアクションが追加された時の処理
        endFlag = False

        # クランバトル用機能の呼出
        readCog = bot.get_cog("ClanBattleReactionManager")
        if readCog is not None:
            endFlag = await readCog.reactionAdd(message)

    @bot.event
    async def on_member_update(before, after):
        # リアクションが追加された時の処理
        endFlag = False

        # クランバトル用機能の呼出
        readCog = bot.get_cog("ClanBattleNameManager")
        if readCog is not None:
            endFlag = await readCog.changeNickInEmbeds(before, after)


    # 起動
    asyncio.run(main())
