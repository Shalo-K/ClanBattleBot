##### import #####
import discord

def getChannelByName(guild, channelName):
    '''
    チャンネル名からチャンネルのオブジェクトを取得する。
    取得できない場合はNoneを返却する。

    Parameters
    ----------
    guild       : guild  チャンネルを検索する対象のサーバー
    channelName : string 取得するチャンネルの名前

    Returns
    -------
    channel : channel 検索から取得したチャンネルオブジェクト
    '''
    channels = guild.text_channels
    for channel in channels:
        if (channel.name == channelName):
            # チャンネルが存在した場合、そのチャンネルのオブジェクトを返却
            return guild.get_channel(channel.id)
    
    # 見つからない場合、Noneを返却
    return None

async def getMessageContentFromPayload(client, payload):
    '''
    メッセージのPayloadからメッセージの本文を取得する。

    Parameters
    ----------
    client  : Client  取得を実行するclientのオブジェクト
    payload : Payload 取得する対象のPayloadオブジェクト

    Returns
    -------
    content : String 取得したメッセージの本文
    '''
    messageObject = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    content = messageObject.content
    return content

async def getMessageAuthorIdFromPayload(client, payload):
    '''
    メッセージのPayloadからメッセージ作成者のIDを取得する。

    Parameters
    ----------
    client  : Client  取得を実行するclientのオブジェクト
    payload : Payload 取得する対象のPayloadオブジェクト

    Returns
    -------
    id : int 取得したID
    '''
    messageObject = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    id = messageObject.author.id
    return id

def replaceAllForEmbedText(embed, index, content, beforeString, afterString):
    '''
    embed、インデックス、要素名を指定して、含まれるテキスト内容を全て置換したembedを返却する。
    実際のメッセージ更新は実行しない。
    
    Parameters
    ----------
    embed        : Embed  置換対象のembedオブジェクト
    index        : int    操作対象のインデックス
    content      : string 操作対象の要素名
    beforeString : string 変更前の文字列
    afterString  : string 変更後の文字列

    Returns
    -------
    Embed : 置換後のembedオブジェクト
    '''
    tempDict = embed.to_dict()

    # メッセージ内の対象単語を全て置換
    tempDict["fields"][index][content] = tempDict["fields"][index][content].replace(beforeString, afterString)
    
    # 置換後のembedオブジェクトを返却
    return discord.Embed.from_dict(tempDict)