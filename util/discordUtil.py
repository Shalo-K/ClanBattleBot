# import discord

# class discordClient:
#     '''
#     Discordに接続するClientオブジェクトを管理するクラス

#     Attributes
#     ----------
#     intent : Intent Client作成時のintent
#     client : Client Clientオブジェクト
#     '''
#     def __init__(self):
#         self.intent = discord.Intents(
#             guilds = True,
#             members = True,
#             messages = True,
#             reactions = True,
#             message_content = True
#         )
#         self.client = discord.Client(intents=self.intent)

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
