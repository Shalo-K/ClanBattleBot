/* 共通パラメータ定義 */
// 環境変数
require('dotenv').config();

// 共通定数
const aplConst = require('./conf/aplConstants.js');

// ログ関連
const LogUtil = require('./util/logUtil.js');
const logUtil = new LogUtil();


// DiscordAPI
const {Client, GatewayIntentBits, MessageReaction} = require('discord.js');    // DiscordAPIのオブジェクト
const client = new Client({                                   // Discordクライアントのオブジェクト
    intents:[
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMembers,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.GuildMessageReactions,
        GatewayIntentBits.MessageContent
    ]
});

// 内部処理変数
let boolRunningFlag = false;                    // サーバ起動フラグ
let intReturnCode = 0;                          // 結果コード

/* ボスデータ定義　　*/
const BossData = require('./BossManager.js');
let bossdata = [];
bossdata.push(new BossData(1, 'ワイバーン', 14500, aplConst.discord_server.message.vote1)); 
bossdata.push(new BossData(2, 'ライライ', 15000, aplConst.discord_server.message.vote2)); 
bossdata.push(new BossData(3, 'オークチーフ', 17500, aplConst.discord_server.message.vote3)); 
bossdata.push(new BossData(4, 'トライロッカー', 19500, aplConst.discord_server.message.vote4)); 
bossdata.push(new BossData(5, 'レサトパルト', 21000, aplConst.discord_server.message.vote5)); 

/* ユーザIDとサーバ表示名のマッピング */
let memberNameMap = new Map();


/* 処理ロジック */
// ロガー起動の確認
if(logUtil === undefined){
    console.log('ログオブジェクトがありません。処理を終了します。');
    process.exit();
}

try{
    processController();

}catch(e){
    // エラー処理
    console.log('システムエラーが発生しました。');
    console.log(e.toString());
    console.log(e.stack);
    
}finally{
    // プロセス終了
    // process.exit();

}

/* コントロールルーチン */
function processController(){
    try{
        logUtil.writeLog(aplConst.logSys, 'info', 'プロセスを開始します。');

        // 初期処理
        intReturnCode = init();

        // メイン処理
        if(intReturnCode == 0){
            main();
        }
        
    }catch(e){
        // エラー処理
        logUtil.writeLog(aplConst.log.sys, 'error', 'システムエラーが発生しました。');
        logUtil.writeLog(aplConst.log.sys, 'error', e.toString());
        logUtil.writeLog(aplConst.log.sys, 'error', e.stack);
        
    }finally{
        // サーバ停止
        logUtil.writeLog(aplConst.log.all, 'debug', 'finally logic start');
        if(!boolRunningFlag){
            logUtil.writeLog(aplConst.log.sys, 'info', 'サーバを停止します。');
            // process.exit();

        }
        logUtil.writeLog(aplConst.log.all, 'debug', 'finally logic end');
        logUtil.writeLog(aplConst.log.sys, 'info', '全てのプロセスが完了しました。')

    }
}

/*
 *discription
 *  初期処理
 *  サーバを起動する。
 *name
 *  init
 *args
 *  なし
 *return
 *  0:正常終了
 *  1:異常終了
 */
function init(){
    let intReturnCodeChild = 1;
    const token = process.env.TOKEN;

    logUtil.writeLog(aplConst.log.all, 'debug', 'function "init" start');
    logUtil.writeLog(aplConst.log.sys, 'info', 'サーバを起動します。');

    try{
        // トークン取得チェック
        if(token === undefined || token == ''){
            new Error('トークンの取得に失敗しました。取得値：' + token.toString());
        }
        
        // サーバ起動
        client.login(token);
        logUtil.writeLog(aplConst.log.all, 'debug', 'login OK');
        boolRunningFlag = true;
        intReturnCodeChild = 0;

        // 起動後の初期処理
        client.on('ready', async function(){
            let message;
            let messageReactions;
            let boss;

            // サーバ内のユーザ情報を取得            
            const members = await client.guilds.cache.get(aplConst.discord_server.guild).members.fetch();
            members.forEach(function(member) {
                memberNameMap.set(member.id, member.displayName);
            });
            
            const messages = await client.channels.cache.get(aplConst.discord_server.chnanel.vote).messages.fetch();

            for(boss in bossdata){
                // 管理用メッセージにリアクション追加
                message = await messages.get(bossdata[boss].voteId).react('⚔️');
                message = await messages.get(bossdata[boss].voteId).react('🧙');
                
                // 物理
                messageReactions = await messages.get(bossdata[boss].voteId).reactions.cache.get('⚔️').users.fetch();
                messageReactions.forEach(function(user) {
                    logUtil.writeLog(aplConst.log.all, 'debug', 'userB:' + user);
                    if(!user.bot){
                        bossdata[boss].controllAttendUser('add', user.id, 'b');
                    }
                });
                
                // 魔法
                messageReactions = await messages.get(bossdata[boss].voteId).reactions.cache.get('🧙').users.fetch();
                messageReactions.forEach(function(user) {
                    logUtil.writeLog(aplConst.log.all, 'debug', 'userM:' + user);
                    if(!user.bot){
                        bossdata[boss].controllAttendUser('add', user.id, 'm');
                    }
                });
            
        }
        logUtil.writeLog(aplConst.log.sys, 'info', 'リアクション対象のfetch完了');
        });
    
    }catch(e){
        // エラー処理
        logUtil.writeLog(aplConst.log.sys, 'error', 'サーバの起動に失敗しました。');
        logUtil.writeLog(aplConst.log.sys, 'error', e.toString());
        logUtil.writeLog(aplConst.log.sys, 'error', e.stack);

    }finally{
        logUtil.writeLog(aplConst.logAll, 'debug', 'function "init" end');
        return intReturnCodeChild;
        
    }
}

async function main(){

    logUtil.writeLog(aplConst.log.all, 'debug', 'function "main" start');
    
    // メッセージ入力時の反応
    client.on('messageCreate', message =>{
        let param = message.content.split(' ');
        // logUtil.writeLog(aplConst.log.all, 'debug', message.content.toString());
        if(message.channelId == aplConst.discord_server.chnanel.vote){
            if(message.content.includes('bot1')){
                message.channelId = aplConst.discord_server.channel.post;
                message.channel.send('test ' + message.author.username);
            }
            else if(message.content.includes('bot2')){
                message.channelId = aplConst.discord_server.channel.post;
                let user = message.author.toString();
                message.channel.send('test ' + user);
            }
        }

        // コマンド専用チャンネルからの入力
        if(message.channelId == aplConst.discord_server.chnanel.command){
            /** ボス情報メッセージ作成
             * !create
             */
            if(message.content.includes('!create')){
                let boss;
                for(boss in bossdata){
                    createBossMessage(bossdata[boss]).then(message =>{
                        message.react('⚔️');
                        message.react('🧙');
                    });
                }
            }
            
            /** 現在HP修正
             * !hpedit ボス番号 現在HP
             */
            if(message.content.includes('!hpedit')){
                if(!isNaN(param[1])){
                    let boss = parseInt(param[1]) - 1;
                    let hp = Number(param[2]);
                    if(boss > -1 && boss < 5 && !isNaN(hp)){
                        bossdata[boss].setCurHp(hp);
                        bossdata[boss].createInfoText(memberNameMap);
                        editBossText(boss);
                    }
                }
            }

            /** ボス情報修正
             * !edit ボス番号 ボス名称 MaxHP
             */
            if(message.content.includes('!edit')){
                if(!isNaN(param[1])){
                    let boss = parseInt(param[1]) - 1;
                    let hp = Number(param[3]);
                    if(boss > -1 && boss < 5 && !isNaN(hp)){
                        bossdata[boss].setName(param[2]);
                        bossdata[boss].setMaxHp(hp);
                        bossdata[boss].setCurHp(hp);
                        bossdata[boss].createInfoText(memberNameMap);
                        editBossText(boss);
                    }
                }
            }

            /** ボス管理メッセージID修正
             * !manage ボス番号 メッセージID
             */
            if(message.content.includes('!manage')){
                if(!isNaN(param[1])){
                    let boss = parseInt(param[1]) - 1;
                    if(boss > -1 && boss < 5){
                        bossdata[boss].setManageId(param[2]);
                    }
                }
            }

            /** ボス参加メッセージID修正
             * !vote ボス番号 メッセージID
             */
            if(message.content.includes('!vote')){
                if(!isNaN(param[1])){
                    let boss = parseInt(param[1]) - 1;
                    if(boss > -1 && boss < 5){
                        bossdata[boss].setVoteId(param[2]);
                        bossdata[boss].clearAttendList();

                        // リアクションの再取得
                        client.channels.cache.get(aplConst.discord_server.chnanel.vote).messages.fetch().then(messages =>{
                            // 物理
                            messages.get(bossdata[boss].voteId).reactions.cache.get('⚔️').users.fetch().then(messageReactions =>{
                                messageReactions.forEach(function(user) {
                                    if(!user.bot){
                                        bossdata[boss].controllAttendUser('add', user.id, 'b');
                                    }
                                });
                            });

                            // 魔法
                            messages.get(bossdata[boss].voteId).reactions.cache.get('🧙').users.fetch().then(messageReactions =>{
                                messageReactions.forEach(function(user) {
                                    logUtil.writeLog(aplConst.log.all, 'debug', 'userM:' + user);
                                    if(!user.bot){
                                        bossdata[boss].controllAttendUser('add', user.id, 'm');
                                    }
                                });
                            });
                        });
                    }
                }
            }
            
            // サーバ停止
            if(message.content.includes('!shutdown')){
                console.log('サーバ停止コマンドが実行されました');
                process.exit();
            }
        }
    });

    // リアクション時の反応
    client.on('messageReactionAdd', function(reaction, user){
        let reactionName;
        // リアクション内容の判定
        switch(reaction.emoji.name){
            case '⚔️':
                reactionName = 'b';
                break;
            case '🧙':
                reactionName = 'm';
                break;
            case '❌':
                if(reaction.message.author.id == aplConst.discord_server.client && !user.bot){
                    reaction.message.delete();
                }
                break;
        }
        if(!user.bot){
            switch (reaction.message.id){
                // ボス参加者追加
                case bossdata[0].voteId:
                    addBossUser(0, user.id, reactionName);
                    break;
                case bossdata[1].voteId:
                    addBossUser(1, user.id, reactionName);
                    break;
                case bossdata[2].voteId:
                    addBossUser(2, user.id, reactionName);
                    break;
                case bossdata[3].voteId:
                    addBossUser(3, user.id, reactionName);
                    break;
                case bossdata[4].voteId:
                    addBossUser(4, user.id, reactionName);
                    break;
                
                // 凸宣言
                case bossdata[0].manageId[0]:
                    reportAttack(0, user.id, reactionName);
                    break;
                case bossdata[1].manageId[0]:
                    reportAttack(1, user.id, reactionName);
                    break;
                case bossdata[2].manageId[0]:
                    reportAttack(2, user.id, reactionName);
                    break;
                case bossdata[3].manageId[0]:
                    reportAttack(3, user.id, reactionName);
                    break;
                case bossdata[4].manageId[0]:
                    reportAttack(4, user.id, reactionName);
                    break;
            }
        }
    });

    client.on('messageReactionRemove', function(reaction, user){
        let reactionName;
        // リアクション内容の判定
        switch(reaction.emoji.name){
            case '⚔️':
                reactionName = 'b';
                break;
            case '🧙':
                reactionName = 'm';
                break;
        }
        if(!user.bot){
            switch (reaction.message.id){
                // ボス参加者削除
                case bossdata[0].voteId:
                    deleteBossUser(0, user.id, reactionName);
                    break;
                case bossdata[1].voteId:
                        deleteBossUser(1, user.id, reactionName);
                    break;
                case bossdata[2].voteId:
                        deleteBossUser(2, user.id, reactionName);
                    break;
                case bossdata[3].voteId:
                        deleteBossUser(3, user.id, reactionName);
                    break;
                case bossdata[4].voteId:
                        deleteBossUser(4, user.id, reactionName);
                    break;
            }
        }
    });
    logUtil.writeLog(aplConst.log.all, 'debug', 'function "main" end');
}

/* リアクション取得用にfetch */
async function messageFetch() {
    let channel;
    let message;
    let messageId;
    let target;

    channel = await client.channels.cache.get(aplConst.discord_server.chnanel.vote);
    messageId = aplConst.discord_server.message;

    for(target in messageId){
        message = await channel.messages.fetch(messageId[target]);
        message.reactions.cache.get('⚔️').users;
    }

}

/* ボス管理用メッセージ作成 */
/** 
 * @param {BossData} boss ボス情報オブジェクト
 * @returns {Promise} 送信したメッセージ情報
 */
async function createBossMessage(boss) {
    let text = boss.createInfoText(memberNameMap);
    let message = await client.channels.cache.get(aplConst.discord_server.chnanel.post).send(text);
    boss.manageId.push(message.id);
    return message;
}

/**
 * ボス情報にユーザを追加する
 * @param {number} boss ボス番号
 * @param {string} userId ユーザID
 * @param {string} reactionName リアクションの種類 
 */
function addBossUser(boss, userId, reactionName) {
    // ボスオブジェクトにユーザを追加
    bossdata[boss].controllAttendUser('add', userId, reactionName);
    
    // メッセージ編集
    editBossText(boss);
}

/**
 * ボス情報からユーザを削除する
 * @param {number} boss ボス番号
 * @param {string} userId ユーザID
 * @param {string} reactionName リアクションの種類 
 */
 function deleteBossUser(boss, userId, reactionName) {
    // ボスオブジェクトからユーザを削除
    bossdata[boss].controllAttendUser('del', userId, reactionName);
    
    // メッセージ編集
    editBossText(boss);
}

/**
 * ボス情報のテキストを編集
 * @param {number} boss ボス番号
 */
function editBossText(boss) {
    // 管理IDが未定義の場合、編集を実施しない
    if(bossdata[boss].manageId.length != 0){
        const text = bossdata[boss].createInfoText(memberNameMap);
        client.channels.cache.get(aplConst.discord_server.chnanel.post).messages.fetch(bossdata[boss].manageId[0]).then(message =>{
            message.edit(text);
        });
    }
}

/**
 * 凸情報記録
 * @param {number} boss ボス番号
 * @param {string} user ユーザID
 * @param {string} reactionType リアクションの種類(物理/魔法)
 */
function reportAttack(boss, user, reactionType) {    
    let text;
    let channel;
    let date = new Date();
    let dateFormat = date.getFullYear() + '/' + ('0' + (date.getMonth() + 1)).slice(-2)  + '/' + ('0' + date.getDay()).slice(-2) + ' '
                        + date.getHours() + ':' + ('0' + date.getMinutes()).slice(-2) + ':' + ('0' + date.getSeconds()).slice(-2);
    
    if(reactionType == 'b'){
        // 物理
        if(bossdata[boss].attendB.indexOf(user) !== -1){
            channel = aplConst.discord_server.chnanel.report;
            text = '```' + dateFormat + '  ' + memberNameMap.get(user) + '  ' + bossdata[boss].name + '(物理)' + '```';
        }else{
            // 凸希望に入っていない場合
            channel = aplConst.discord_server.chnanel.post;
            text = '```' + memberNameMap.get(user) +  '\n対象のボスに参加していません ' + bossdata[boss].name + '(物理)```';
        }
    }else if(reactionType == 'm'){
        // 魔法
        if(bossdata[boss].attendM.indexOf(user) !== -1){
            channel = aplConst.discord_server.chnanel.report;
            text = '```' + dateFormat + '  '  + memberNameMap.get(user) + '  ' + bossdata[boss].name + '(魔法)' + '```';
        }else{
            // 凸希望に入っていない場合
            channel = aplConst.discord_server.chnanel.post;
            text = '```' + memberNameMap.get(user) +  '\n対象のボスに参加していません ' + bossdata[boss].name + '(魔法)```';
        }
    }

    // メッセージ送信
    client.channels.cache.get(channel).send(text).then(sent =>{
        sent.react('❌');
    });
}