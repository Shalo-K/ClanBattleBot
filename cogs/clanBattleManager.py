###### import #####
import enum
import os
import discord
from discord import app_commands
from discord.ext import commands

##### util #####
from util import discordUtil
from util import formatUtil
from util.fileController import AplConst

##### configの読み込み #####
aplPath = os.getcwd()
aplConst = AplConst(aplPath)


##### コマンドパラメータ用のEnum #####
class ChannelListEnum(enum.Enum):
    vote = aplConst.get("channelName.vote")
    list = aplConst.get("channelName.list")

##### cogのクラス定義 #####
class ClanBattleCommandManager(commands.Cog):
    '''
    クランバトル用コマンド定義クラス

    Attributes
    ----------
    bot : Bot bot自身のオブジェクト
    '''
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name = "messageset", description = "操作用メッセージ作成")
    async def messageset(self, interaction: discord.Interaction, channel: ChannelListEnum):
        '''
        クランバトル操作用のメッセージを作成する。
        '''
        completeFlag = False
        await interaction.response.defer(ephemeral=True)
        # チャンネル取得
        channelObject = discordUtil.getChannelByName(interaction.guild, channel.value)
        if channelObject is None:
            await interaction.followup.send("指定されたチャンネル(" + channel.value + ")が存在しません。", ephemeral=True)
        else:
            if (channel.value == aplConst.get("channelName.vote")):
                for i in range(1,6):
                    # embed作成
                    embed = discord.Embed(title= str(i) + aplConst.get("embed.vote"))
                    embed.add_field(name= aplConst.get("embed.physic"), value= "", inline= False)
                    embed.add_field(name= aplConst.get("embed.magic"), value= "", inline= False)
                    embed.add_field(name= aplConst.get("embed.re"), value= "", inline= False)

                    # 凸先アンケートにリアクション付きでメッセージを作成
                    sent = await channelObject.send(embed=embed)
                    await sent.add_reaction(aplConst.get("reaction.crossed_swords"))
                    await sent.add_reaction(aplConst.get("reaction.mage"))
                    await sent.add_reaction(aplConst.get("reaction.coffee"))
                    await sent.add_reaction(aplConst.get("reaction.star"))
                    await sent.add_reaction(aplConst.get("reaction.ballot_box_with_check"))
                    await sent.add_reaction(aplConst.get("reaction.wrench"))
                completeFlag = True

            elif (channel.value == aplConst.get("channelName.list")):
                for i in range(1,6):
                    # embed作成
                    embed = discord.Embed(title= str(i) + aplConst.get("embed.list"))
                    embed.add_field(name= aplConst.get("embed.physic"), value= "", inline= False)
                    embed.add_field(name= aplConst.get("embed.magic"), value= "", inline= False)
                    embed.add_field(name= aplConst.get("embed.re"), value= "", inline= False)

                    # 凸参加一覧にリアクション付きでメッセージを作成
                    sent = await channelObject.send(embed=embed)
                    await sent.add_reaction(aplConst.get("reaction.crossed_swords"))
                    await sent.add_reaction(aplConst.get("reaction.mage"))
                    await sent.add_reaction(aplConst.get("reaction.coffee"))
                    await sent.add_reaction(aplConst.get("reaction.star"))
                    await sent.add_reaction(aplConst.get("reaction.ballot_box_with_check"))
                    await sent.add_reaction(aplConst.get("reaction.wrench"))
                completeFlag = True
            
            if (completeFlag):
                await interaction.followup.send("メッセージを作成しました。(" + channel.value + ")", ephemeral=True)
            else:
                await interaction.followup.send("メッセージの作成に失敗しました。(" + channel.value + ")", ephemeral=True)


##### リアクション操作 #####
class ClanBattleReactionManager(commands.Cog):
    '''
    クランバトル用リアクション操作定義クラス

    Attributes
    ----------
    bot : Bot bot自身のオブジェクト
    '''
    def __init__(self, bot):
        self.bot = bot
    
    async def reactionAdd(self, message: discord.RawReactionActionEvent):
        '''
        追加されたリアクションに応じた操作を実行

        Parameters
        ----------
        message : RawReactionActionEvent 追加されたリアクションの情報

        Returns
        -------
        endFlag : 処理終了フラグ
        '''
        endFlag = False
        if (message.user_id != int(aplConst.get("id.client"))):
            # リアクションを実行したユーザがbot自身でない場合のアクション
            # メッセージの内容を取得
            messageObject = await self.bot.get_channel(message.channel_id).fetch_message(message.message_id)
            messageText = messageObject.content.replace("`", "")
            embeds = messageObject.embeds
            guildObject = self.bot.get_guild(message.guild_id)
            userObject = guildObject.get_member(message.user_id)
            userName = userObject.display_name

            if (messageObject.author.id == int(aplConst.get("id.client"))):
                # bot自身が作成したメッセージに対するリアクションの場合のアクション
                if (bool(embeds)):
                    fieldIndex = None
                    ##### 凸先アンケート #####
                    if (messageObject.channel.name == aplConst.get("channelName.vote")):
                        if (message.emoji.name == aplConst.get("reaction.crossed_swords")
                            or message.emoji.name == aplConst.get("reaction.mage")
                            or message.emoji.name == aplConst.get("reaction.coffee")):
                            # 物理/魔法/持越のリアクションが押された場合、ユーザーを追加/削除する
                            if (message.emoji.name == aplConst.get("reaction.crossed_swords")):
                                # 物理
                                fieldIndex = 0
                            elif (message.emoji.name == aplConst.get("reaction.mage")):
                                # 魔法
                                fieldIndex = 1
                            elif (message.emoji.name == aplConst.get("reaction.coffee")):
                                # 持越
                                fieldIndex = 2

                            # メッセージを編集してリアクションを解除
                            await self.editEmbedForEntry(messageObject, fieldIndex, userName)
                            await messageObject.remove_reaction(message.emoji, message.member)

                            # botリアクションがない場合は追加する
                            await messageObject.add_reaction(message.emoji)

                        elif (message.emoji.name == aplConst.get("reaction.ballot_box_with_check")):
                            # 確定状態の変更
                            fieldIndex = []
                            for i in range(0, len(embeds[0].fields)):
                                if (userName in embeds[0].fields[i].value):
                                    fieldIndex.append(i)

                            if (len(fieldIndex) == 1):
                                # 編集対象が1つの場合、対象を直接指定して編集
                                await self.editEmbedForCheck(messageObject, fieldIndex[0], userName)
                            elif (len(fieldIndex) > 1):
                                # 編集対象が複数ある場合、対象を確認するメッセージを送信
                                sent = await messageObject.reply(content=userObject.mention + aplConst.get("message.selectCheck") + "\n||" + aplConst.get("message.channelId") + str(message.channel_id) + "\n" + aplConst.get("message.messageId") + str(message.message_id) + "||")
                                for i in fieldIndex:
                                    # インデックスに応じたリアクションを追加
                                    if (i == 0):
                                        await sent.add_reaction(aplConst.get("reaction.crossed_swords"))
                                    elif (i == 1):
                                        await sent.add_reaction(aplConst.get("reaction.mage"))
                                    elif (i == 2):
                                        await sent.add_reaction(aplConst.get("reaction.coffee"))
                                    elif (i == 3):
                                        await sent.add_reaction(aplConst.get("reaction.star"))
                                await sent.add_reaction(aplConst.get("reaction.x"))

                            # リアクションを解除
                            await messageObject.remove_reaction(message.emoji, message.member)

                            # botリアクションがない場合は追加する
                            await messageObject.add_reaction(message.emoji)

                        elif (message.emoji.name == aplConst.get("reaction.wrench")):
                            # 参加者を全員リセット
                            content = embeds[0].to_dict()
                            for i in range(0, len(embeds[0].fields)):
                                content["fields"][i]["value"] = ""
                                if (content["fields"][i]["name"] == aplConst.get("embed.spare")):
                                    # 予備枠の削除
                                    del content["fields"][i]

                            # メッセージを編集
                            embed = discord.Embed.from_dict(content)
                            await messageObject.edit(embed=embed)
                        
                            # リアクションを解除
                            await messageObject.remove_reaction(message.emoji, message.member)

                            # botリアクションがない場合は追加する
                            await messageObject.add_reaction(message.emoji)

                        elif (message.emoji.name == aplConst.get("reaction.star")):
                            # 予備用枠の追加と削除
                            for i in range(0, len(embeds[0].fields)):
                                if (embeds[0].fields[i].name == aplConst.get("embed.spare")):
                                    fieldIndex = i
                                    break

                            if (fieldIndex is not None):
                                # 予備用枠が既にある場合、編集
                                await self.editEmbedForEntry(messageObject, fieldIndex, userName)
                            else:
                                # 予備用枠がない場合、作成してユーザーを追加
                                embeds[0].add_field(name= aplConst.get("embed.spare"), value= userName, inline= False)
                                content = embeds[0].to_dict()
                                embed = discord.Embed.from_dict(content)
                                await messageObject.edit(embed=embed)

                            # リアクションを解除
                            await messageObject.remove_reaction(message.emoji, message.member)

                            # botリアクションがない場合は追加する
                            await messageObject.add_reaction(message.emoji)

                        # 後続のリアクション判定を実施しない
                        endFlag = True

                    ##### 凸参加一覧 #####
                    elif (messageObject.channel.name == aplConst.get("channelName.list")):
                        if (message.emoji.name == aplConst.get("reaction.crossed_swords")
                            or message.emoji.name == aplConst.get("reaction.mage")
                            or message.emoji.name == aplConst.get("reaction.coffee")):
                            # 物理/魔法/持越のリアクションが押された場合、ユーザーを追加/削除する
                            if (message.emoji.name == aplConst.get("reaction.crossed_swords")):
                                # 物理
                                fieldIndex = 0
                            elif (message.emoji.name == aplConst.get("reaction.mage")):
                                # 魔法
                                fieldIndex = 1
                            elif (message.emoji.name == aplConst.get("reaction.coffee")):
                                # 持越
                                fieldIndex = 2

                            # メッセージを編集してリアクションを解除
                            await self.editEmbedForEntry(messageObject, fieldIndex, userName)
                            await messageObject.remove_reaction(message.emoji, message.member)

                            # botリアクションがない場合は追加する
                            await messageObject.add_reaction(message.emoji)

                        elif (message.emoji.name == aplConst.get("reaction.ballot_box_with_check")):
                            # 確定状態の変更
                            fieldIndex = []
                            for i in range(0, len(embeds[0].fields)):
                                if (userName in embeds[0].fields[i].value):
                                    fieldIndex.append(i)

                            if (len(fieldIndex) == 1):
                                # 編集対象が1つの場合、対象を直接指定して編集
                                await self.editEmbedForCheck(messageObject, fieldIndex[0], userName)
                            else:
                                # 編集対象が複数ある場合、対象を確認するメッセージを送信
                                sent = await messageObject.reply(content=userObject.mention + aplConst.get("message.selectCheck") + "\n||" + aplConst.get("message.channelId") + str(message.channel_id) + "\n" + aplConst.get("message.messageId") + str(message.message_id) + "||")
                                for i in fieldIndex:
                                    # インデックスに応じたリアクションを追加
                                    if (i == 0):
                                        await sent.add_reaction(aplConst.get("reaction.crossed_swords"))
                                    elif (i == 1):
                                        await sent.add_reaction(aplConst.get("reaction.mage"))
                                    elif (i == 2):
                                        await sent.add_reaction(aplConst.get("reaction.coffee"))
                                    elif (i == 3):
                                        await sent.add_reaction(aplConst.get("reaction.star"))
                                await sent.add_reaction(aplConst.get("reaction.x"))

                            # リアクションを解除
                            await messageObject.remove_reaction(message.emoji, message.member)

                            # botリアクションがない場合は追加する
                            await messageObject.add_reaction(message.emoji)

                        elif (message.emoji.name == aplConst.get("reaction.wrench")):
                            # 参加者を全員リセット
                            content = embeds[0].to_dict()
                            for i in range(0, len(embeds[0].fields)):
                                content["fields"][i]["value"] = ""
                                if (content["fields"][i]["name"] == aplConst.get("embed.spare")):
                                    # 予備枠の削除
                                    del content["fields"][i]

                            # メッセージを編集
                            embed = discord.Embed.from_dict(content)
                            await messageObject.edit(embed=embed)
                        
                            # リアクションを解除
                            await messageObject.remove_reaction(message.emoji, message.member)

                            # botリアクションがない場合は追加する
                            await messageObject.add_reaction(message.emoji)

                        elif (message.emoji.name == aplConst.get("reaction.star")):
                            # 予備用枠の追加と削除
                            for i in range(0, len(embeds[0].fields)):
                                if (embeds[0].fields[i].name == aplConst.get("embed.spare")):
                                    fieldIndex = i
                                    break

                            if (fieldIndex is not None):
                                # 予備用枠が既にある場合、編集
                                await self.editEmbedForEntry(messageObject, fieldIndex, userName)
                            else:
                                # 予備用枠がない場合、作成してユーザーを追加
                                embeds[0].add_field(name= aplConst.get("embed.spare"), value= userName, inline= False)
                                content = embeds[0].to_dict()
                                embed = discord.Embed.from_dict(content)
                                await messageObject.edit(embed=embed)

                            # リアクションを解除
                            await messageObject.remove_reaction(message.emoji, message.member)

                            # botリアクションがない場合は追加する
                            await messageObject.add_reaction(message.emoji)

                        # 後続のリアクション判定を実施しない
                        endFlag = True

                ##### embedなしのメッセージ #####
                else:
                    if ((messageObject.channel.name == aplConst.get("channelName.vote"))
                        or (messageObject.channel.name == aplConst.get("channelName.list"))):
                        deleteFlg = False
                        messageText = messageObject.content.replace("||", "").split("\n")

                        if (message.emoji.name == aplConst.get("reaction.x")):
                            # 削除リアクション
                            deleteFlg = True

                        elif (aplConst.get("message.selectCheck") in messageText[0]):
                            # 複数の参加がある場合の再リアクション判定
                            if (("~~" in userName) or ("||" in userName)):
                                # 動作上使用できない絵文字が名前に含まれている場合、警告メッセージを送信
                                sent = await messageObject.reply(content=userObject.mention + aplConst.get("message.alertName"))
                                await sent.add_reaction(aplConst.get("reaction.x"))

                            else:
                                channelId = messageText[1].replace(aplConst.get("message.channelId"), "")
                                messageId = messageText[2].replace(aplConst.get("message.messageId"), "")
                                editMessage = await self.bot.get_channel(int(channelId)).fetch_message(int(messageId))
                                if (message.emoji.name == aplConst.get("reaction.crossed_swords")):
                                    await self.editEmbedForCheck(editMessage, 0, userName)
                                    deleteFlg = True
                                elif (message.emoji.name == aplConst.get("reaction.mage")):
                                    await self.editEmbedForCheck(editMessage, 1, userName)
                                    deleteFlg = True
                                elif (message.emoji.name == aplConst.get("reaction.coffee")):
                                    await self.editEmbedForCheck(editMessage, 2, userName)
                                    deleteFlg = True
                                elif (message.emoji.name == aplConst.get("reaction.star")):
                                    await self.editEmbedForCheck(editMessage, 3, userName)
                                    deleteFlg = True
                        
                        # 削除フラグが立っている場合、確認メッセージを削除
                        if (deleteFlg):
                            await messageObject.delete()

                        # 後続のリアクション判定を実施しない
                        endFlag = True

                    elif (messageObject.channel.name == aplConst.get("channelName.memory")):
                        # 凸宣言記録
                        if (message.emoji.name == aplConst.get("reaction.x")):
                            # 凸宣言のキャンセル
                            await messageObject.reply(content="キャンセルされました")
                            await messageObject.edit(content="~~"+messageText+"~~")
                            await messageObject.remove_reaction(message.emoji, message.member)

                        # 後続のリアクション判定を実施しない
                        endFlag = True
                    
                    elif (messageObject.channel.name == aplConst.get("channelName.action")):
                        # botメッセージチャンネル
                        if (message.emoji.name == aplConst.get("reaction.thumbsup")):
                            messageText = messageObject.content.split("\n")
                            if (aplConst.get("message.changeName") in messageText[0]):
                                # 名前変更操作
                                deleteFlg = False

                                # 前回の失敗リアクションがある場合、解除する
                                for react in messageObject.reactions:
                                    if ((react.emoji == aplConst.get("reaction.thinking"))
                                        and (react.me)):
                                        await react.remove(messageObject.author)

                                beforeName = messageText[1].replace(aplConst.get("message.changeBefore"), "")
                                afterName = messageText[2].replace(aplConst.get("message.changeAfter"), "")

                                # 検索対象のチャンネル
                                channelVote = discordUtil.getChannelByName(guildObject, aplConst.get("channelName.vote"))
                                channelList = discordUtil.getChannelByName(guildObject, aplConst.get("channelName.list"))
                                
                                # 置換実行
                                try:
                                    await self.editEmbedForRename(channelVote, beforeName, afterName)
                                    await self.editEmbedForRename(channelList, beforeName, afterName)
                                    deleteFlg = True
                                except Exception as e:
                                    # 置換に失敗した場合、リアクションを追加
                                    await messageObject.add_reaction(aplConst.get("reaction.thinking"))
                                    await messageObject.remove_reaction(message.emoji, message.member)

                                # 処理終了後にメッセージを削除する
                                if (deleteFlg):
                                    await messageObject.delete()

                            # 後続のリアクション判定を実施しない
                            endFlag = True
        
        # 判定終了
        return endFlag


    async def editEmbedForEntry(self, message, fieldIndex, userName):
        '''
        メッセージのembedを編集し、凸参加情報を変更する。
        凸参加一覧のメッセージでユーザーを追加した場合は凸宣言も送信する。

        Parameters
        ----------
        message    : Message 編集するメッセージの情報
        fieldIndex : int     編集するembedのインデックス
        userName   : string  参加情報を変更するユーザー
        '''
        embeds = message.embeds
        titleArray = embeds[0].title.split(" ")
        content = embeds[0].to_dict()
        fieldValue = embeds[0].fields[fieldIndex].value
        if (userName not in fieldValue):
            # ユーザー追加
            content["fields"][fieldIndex]["value"] = fieldValue + "\n" + userName
            if (aplConst.get("embed.list") in embeds[0].title):
                # 凸参加一覧のメッセージである場合、凸宣言を送信
                sendChannel = discordUtil.getChannelByName(message.guild, aplConst.get("channelName.memory"))
                logTime = formatUtil.datetimeFormat("now", "%Y/%m/%d %H:%M:%S")
                nameInfo = userName + "(" + content["fields"][fieldIndex]["name"] + ")"
                sent = await sendChannel.send(content="```" + logTime + " " + nameInfo + " " + titleArray[0] + "```")
                await sent.add_reaction(aplConst.get("reaction.x"))
        else:
            # ユーザー削除
            fieldValue = fieldValue.replace(userName, "")
            fieldValue = fieldValue.replace(("~~~~"), "")
            fieldValue = fieldValue.replace(("\n\n"), "\n")
            if ((content["fields"][fieldIndex]["name"] == aplConst.get("embed.spare")) and (fieldValue == "")):
                # 予備枠が空となる場合、フィールドごと削除する
                del content["fields"][fieldIndex]
            else:
                content["fields"][fieldIndex]["value"] = fieldValue
        
        # メッセージを編集
        embed = discord.Embed.from_dict(content)
        await message.edit(embed=embed)


    async def editEmbedForCheck(self, message, fieldIndex, userName):
        '''
        メッセージのembedを編集し、凸完了情報を変更する。

        Parameters
        ----------
        message    : Message 編集するメッセージの情報
        fieldIndex : int     編集するembedのインデックス
        userName   : string  参加情報を変更するユーザー
        '''
        embeds = message.embeds
        content = embeds[0].to_dict()
        fieldValue = embeds[0].fields[fieldIndex].value
        if (("~~" + userName + "~~") in fieldValue):
            # 確定の解除
            content["fields"][fieldIndex]["value"] = fieldValue.replace(("~~" + userName + "~~"), userName)
        else:
            # 確定
            content["fields"][fieldIndex]["value"] = fieldValue.replace(userName, ("~~" + userName + "~~"))
        
        # メッセージを編集
        embed = discord.Embed.from_dict(content)
        await message.edit(embed=embed)


    async def editEmbedForRename(self, channel, beforeName, afterName):
        '''
        メッセージのembedを編集し、既に登録されている名前を変更する。

        Parameters
        ----------
        channel    : Channel 編集するメッセージを検索するチャンネル
        beforeName : string  編集するembedのインデックス
        afterName  : string  参加情報を変更するユーザー
        '''
        async for message in channel.history(limit = 100):
            if (message.author.id == int(aplConst.get("id.client"))):
                editFlag = False
                embeds = message.embeds
                if (bool(embeds)):
                    # bot自身が生成したメッセージかつembedが使用されている場合、変更操作を実行
                    for i in range(0, len(embeds[0].fields)):
                        # メッセージ内の対象単語を全て置換
                        tempString = embeds[0].fields[i].value
                        embeds[0] = discordUtil.replaceAllForEmbedText(embeds[0], i, "value", beforeName, afterName)
                        
                        if (tempString != embeds[0].fields[i].value):
                            editFlag = True

                    if (editFlag):
                        # 置換の前後を比較し、差分があった場合のみ変更を確定
                        await message.edit(embed=embeds[0])


##### ユーザ名変更操作 ######
class ClanBattleNameManager(commands.Cog):
    '''
    クランバトル用名前変更定義クラス

    Attributes
    ----------
    bot : Bot bot自身のオブジェクト
    '''
    def __init__(self, bot):
        self.bot = bot

    async def changeNickInEmbeds(self, before: discord.Member, after: discord.Member):
        '''
        embedのリストに登録されているユーザ名を変更する。
        ユーザ名はユーザ情報のオブジェクトから取得する

        Parameters
        ----------
        before : 変更前のユーザ情報
        after  : 変更後のユーザ情報
        '''
        # 変更確認メッセージの送信チャンネル取得
        sendChannel = discordUtil.getChannelByName(before.guild, aplConst.get("channelName.action"))

        # 送信
        sent = await sendChannel.send(content=
                                      before.mention + aplConst.get("message.changeName") + "\n"
                                        + aplConst.get("message.changeBefore") + before.nick + "\n" 
                                        + aplConst.get("message.changeAfter") + after.nick
                                    )
        # 操作用リアクション
        await sent.add_reaction(aplConst.get("reaction.thumbsup"))


##### Cog読み込み時に実行されるメソッド #####
async def setup(bot):
    # Botを渡してインスタンス化し、Botにコグとして登録する
    await bot.add_cog(ClanBattleReactionManager(bot))
    await bot.add_cog(ClanBattleCommandManager(bot))
    await bot.add_cog(ClanBattleNameManager(bot))
