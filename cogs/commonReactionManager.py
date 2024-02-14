###### import #####
import os
import discord
from discord.ext import commands

##### util #####
from util import discordUtil
from util.fileController import AplConst

##### configの読み込み #####
aplPath = os.getcwd()
aplConst = AplConst(aplPath)


class CommonReactionManager(commands.Cog):
    '''
    リアクション実行時の操作定義クラス

    Attributes
    ----------
    bot : Bot bot自身のオブジェクト
    '''
    def __init__(self, bot):
        self.bot = bot
    
    ##### リアクション追加のロジック #####
    async def reactionAdd(self, reaction: discord.RawReactionActionEvent):
        '''
        リアクション追加時処理のメインロジック

        Parameters
        ----------
        reaction : RawReactionActionEvent 実行されたリアクションの情報

        Returns
        -------
        endFlag : 処理終了フラグ
        '''
        endFlag = False

        if (reaction.user_id != int(aplConst.get("id.client"))):
            # リアクションを実行したユーザがbot自身でない場合のアクション
            if (await discordUtil.getMessageAuthorIdFromPayload(self.bot, reaction) == int(aplConst.get("id.client"))):
                ##### bot自身が作成したメッセージに対するリアクションの場合のアクション #####
                await self.checkReactionToBot(reaction)
                    
            else:
                ##### このbot以外が作成したメッセージに対するリアクションの場合のアクション #####
                await self.checkReactionElseBot(reaction)

        return endFlag
    

    ##### リアクション削除のロジック #####
    async def reactionRemove(self, reaction: discord.RawReactionActionEvent):
        '''
        リアクション削除時処理のメインロジック

        Parameters
        ----------
        reaction : RawReactionActionEvent 実行されたリアクションの情報

        Returns
        -------
        endFlag : 処理終了フラグ
        '''
        endFlag = False

        if (reaction.user_id != int(aplConst.get("id.client"))):
            # リアクションを実行したユーザがbot自身でない場合のアクション
            if (await discordUtil.getMessageAuthorIdFromPayload(self.bot, reaction) == int(aplConst.get("id.client"))):
                ##### bot自身が作成したメッセージに対するリアクションの場合のアクション #####
                await self.checkReactionToBot(reaction)

        return endFlag

    
    ##### 詳細ロジック #####
    async def checkReactionToBot(self, reaction: discord.RawReactionActionEvent):
        '''
        bot自身が作成したメッセージに対するリアクションの実行ロジック

        Parameters
        ----------
        reaction : RawReactionActionEvent 実行されたリアクションの情報
        '''
        reactionMessage = await self.bot.get_channel(reaction.channel_id).fetch_message(reaction.message_id)

        if (aplConst.get("message.reactionList") in reactionMessage.content):
            # リアクション一覧の集計
            await self.editReactionListMessage(reactionMessage)

    async def checkReactionElseBot(self, reaction: discord.RawReactionActionEvent):
        '''
        bot以外が作成したメッセージに対するリアクションの実行ロジック

        Parameters
        ----------
        reaction : RawReactionActionEvent 実行されたリアクションの情報
        '''
        reactionMessage = await self.bot.get_channel(reaction.channel_id).fetch_message(reaction.message_id)

        if (discordUtil.includeMention(reactionMessage, self.bot.user)):
            # メッセージにbotへのメンションが含まれる場合のアクション
            await self.checkReactionIncludeMentionToBot(reaction, reactionMessage)

    async def checkReactionIncludeMentionToBot(self, reaction: discord.RawReactionActionEvent, message):
        '''
        botへのメンションを含むメッセージに対するリアクションの実行ロジック

        Parameters
        ----------
        reaction : RawReactionActionEvent 実行されたリアクションの情報
        message  : message                リアクションが実行されたメッセージ
        '''
        # 操作対象のbotメッセージを検索
        botMessages = await discordUtil.getMessageFromReply(message= message, author= self.bot.user)

        # 対象のメッセージにbotのリアクションを追加
        for bm in botMessages:
            if not (reaction.emoji.is_custom_emoji()):
                await bm.add_reaction(reaction.emoji)
                await message.remove_reaction(reaction.emoji, reaction.member)
                # 集計のメッセージ内容を更新
                await self.editReactionListMessage(bm)

    async def editReactionListMessage(self, message):
        '''
        リアクションを集計するメッセージを編集する。

        Parameters
        ----------
        message : message リアクションが実行されたメッセージ
        '''
        targetUsers = []
        targetNames = []
        reactionUsers = []

        ##### 集計するユーザーの一覧を取得 #####
        messageReference = message.reference
        if messageReference is not None:
            fetchMessage = await message.channel.fetch_message(messageReference.message_id)

        # 集計対象メンバーに、ロールに含まれるメンバーを追加
        for role in fetchMessage.role_mentions:
            targetUsers.extend(role.members)

        # 集計対象メンバーに、直接メンションしているメンバーを追加
        for member in fetchMessage.mentions:
            targetUsers.append(member)

        # 重複を削除して表示名に置き換え
        targetUsers = list(set(targetUsers))
        targetNames = [user.display_name for user in targetUsers if not (user.bot)]
        
        ##### メッセージ文言の作成 #####
        contentArray = [aplConst.get("message.reactionList")]
        for r in message.reactions:
            # リアクションの一覧を取得
            if not (r.is_custom_emoji()):
                # botが参照可能な絵文字のみ集計対象にする
                reactionUsers = [u.display_name async for u in r.users() if not (u.bot)]

                contentArray.append(str(r.emoji))
                if (len(reactionUsers) > 0):
                    contentArray.append("```" + " ".join(reactionUsers) + "```")
                else:
                    contentArray.append("```該当者なし```")

                # 集計対象メンバーから、リアクションを追加しているユーザーを削除する
                for ru in reactionUsers:
                    for tn in targetNames:
                        if (tn == ru):
                            targetNames.remove(ru)
                            break
        
        # どこにもリアクションしていないユーザー
        contentArray.append(aplConst.get("message.noReaction"))
        if (len(targetNames) > 0):
            contentArray.append("```" + " ".join(targetNames) + "```")
        else:
            contentArray.append("```該当者なし```")

        # メッセージを編集
        await message.edit(content="\n".join(contentArray))


##### Cog読み込み時に実行されるメソッド #####
async def setup(bot):
    # Botを渡してインスタンス化し、Botにコグとして登録する
    await bot.add_cog(CommonReactionManager(bot))
