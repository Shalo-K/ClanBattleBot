/* アプリケーション共通定数定義 */
module.exports ={
    /* ログ定義 */
    'log':{
        'all': 'debug',
        'sys': 'system',
        'command': 'command'
    },

    /* DiscordID */
    'discord_server':{
        'client': '',    // BOT自身のID
        'guild': '',      // 使用するサーバー
        
        // 使用するチャンネル
        'chnanel':{
            'post': '',      // ボス情報を投稿するチャンネル
            'vote': '',      // 参加募集をするチャンネル
            'report': '',    // 凸情報を記録するチャンネル
            'command': ''    // コマンド実行を許容するチャンネル
        },

        // 固定で使用するメッセージのID
        'message':{
            // 各ボスの参加リアクションをもらうメッセージ
            'vote1': '',
            'vote2': '',
            'vote3': '',
            'vote4': '',
            'vote5': ''
        }
    }
}
