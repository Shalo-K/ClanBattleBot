/**
 * @property {number} id ボスの番号
 * @property {string} name ボスの名前
 * @property {number} maxHp ボスの最大HP
 * @property {number} curHp ボスの現在HP
 * @property {array} manageId ボスの管理用メッセージID
 * @property {string} voteId 参加者投票用ID
 * @property {array} scheduleB 物理アンケ
 * @property {array} scheduleM 魔法アンケ
 * @property {array} attendB 物理参加者
 * @property {array} attendM 魔法参加者
 * @property {Map} attackB 物理ダメージ
 * @property {Map} attackM 魔法ダメージ
 * @property {Map} sampleB 物理予定ダメージ
 * @property {Map} sampleM 魔法予定ダメージ
 */
class BossData {
    /**
     * @constructor
     * @param {number} id ボスの番号
     * @param {string} name ボスの名前
     * @param {number} hp ボスの最大HP
     * @param {string} voteId 参加者投票用ID
     */
    constructor(id, name, hp, manageId, scheduleId, voteId){
        this.id = id;
        this.name = name;
        this.maxHp = hp;
        this.curHp = hp;
        this.manageId = [manageId, scheduleId];
        this.voteId = voteId;
        this.scheduleB = [];
        this.scheduleM = [];
        this.attendB = [];
        this.attendM = [];
        this.attackB = new Map();
        this.attackM = new Map();
        this.sampleB = new Map();
        this.sampleM = new Map();
    }

    /**
     * ボスの名前を変更する
     * @param {string} name name
     */
    setName(name){
        this.name = name;
    }

    /**
     * ボスの最大HPを変更する
     * @param {number} maxHp maxHP
     */
     setMaxHp(maxHp){
        this.maxHp = maxHp;
    }

    /**
     * ボスの現在HPを変更する
     * @param {number} curHp curHP
     */
     setCurHp(curHp){
        this.curHp = curHp;
    }

    /**
     * ボスの管理メッセージIDを変更する
     * @param {string} manageId manageID
     */
     setManageId(manageId){
        this.manageId.length = 0;
        this.manageId.push(manageId);
    }

    /**
     * ボスの投票用IDを変更する
     * @param {string} voteId voteID
     */
    setVoteId(voteId){
        this.voteId = voteId;
    }

    /**
     * ボス情報のテキストを編集する
     * @param {Map} memberNameMap ユーザ情報 
     * @returns {string} メッセージテキスト
     */
    createInfoText(memberNameMap) {
        let user;
        let text = '```' + this.name + '\n\n現在の参加者\n';

        // 物理
        for (user in this.attendB){
            text = text + memberNameMap.get(this.attendB[user]) + '(物理) ' + '\n';
        }
        
        // 魔法
        for (user in this.attendM){
            text = text + memberNameMap.get(this.attendM[user]) + '(魔法) ' + '\n';
        }

        text = text + '```'
        return text;
    }

    /**
     * ボスごとの参加ユーザを追加/削除する
     * @param {string} controllType 操作の種類 (追加/削除)
     * @param {string} userId ユーザID
     * @param {string} reactionType リアクションの種類 (物理/魔法)
     */
    controllAttendUser(controllType, userId, reactionType) {
        switch(reactionType){
            // 物理
            case 'b':
                switch(controllType){
                    // 追加
                    case 'add':
                        if (!this.attendB.includes(userId)){
                            this.attendB.push(userId);
                            this.attackB.set(userId, '0');
                            this.sampleB.set(userId, '0');
                        }
                        break;
                    
                    // 削除
                    case 'del':
                        if (this.attendB.includes(userId)){
                            this.attendB = this.attendB.filter(item => item.match(userId) == null);
                            this.attackB.delete(userId);
                            this.sampleB.delete(userId);
                        }
                        break;
                }
                break;
            
            // 魔法
            case 'm':
                switch(controllType){
                    // 追加
                    case 'add':
                        if (!this.attendM.includes(userId)){
                            this.attendM.push(userId);
                            this.attackM.set(userId, '0');
                            this.sampleM.set(userId, '0');
                        }
                        break;
                    
                    // 削除
                    case 'del':
                        if (this.attendM.includes(userId)){
                            this.attendM = this.attendM.filter(item => item.match(userId) == null);
                            this.attackM.delete(userId);
                            this.sampleM.delete(userId);
                        }
                        break;
                }
                break;
        }
    }

    /**
     * ボス情報のアンケテキストを編集する
     * @param {Map} memberNameMap ユーザ情報 
     * @returns {string} メッセージテキスト
     */
    createScheduleText(memberNameMap) {
        let user;
        let text = '```' + this.name + ' 凸希望者\n';

        // 物理
        for (user in this.scheduleB){
            text = text + memberNameMap.get(this.scheduleB[user]) + '(物理) ' + '\n';
        }
        
        // 魔法
        for (user in this.scheduleM){
            text = text + memberNameMap.get(this.scheduleM[user]) + '(魔法) ' + '\n';
        }

        text = text + '```'
        return text;
    }

    /**
     * ボスごとのアンケユーザを追加/削除する
     * @param {string} controllType 操作の種類 (追加/削除)
     * @param {string} userId ユーザID
     * @param {string} reactionType リアクションの種類 (物理/魔法)
     */
    controllScheduleUser(controllType, userId, reactionType) {
        switch(reactionType){
            // 物理
            case 'b':
                switch(controllType){
                    // 追加
                    case 'add':
                        if (!this.scheduleB.includes(userId)){
                            this.scheduleB.push(userId);
                        }
                        break;
                    
                    // 削除
                    case 'del':
                        if (this.scheduleB.includes(userId)){
                            this.scheduleB = this.scheduleB.filter(item => item.match(userId) == null);
                        }
                        break;
                }
                break;
            
            // 魔法
            case 'm':
                switch(controllType){
                    // 追加
                    case 'add':
                        if (!this.scheduleM.includes(userId)){
                            this.scheduleM.push(userId);
                        }
                        break;
                    
                    // 削除
                    case 'del':
                        if (this.scheduleM.includes(userId)){
                            this.scheduleM = this.scheduleM.filter(item => item.match(userId) == null);
                        }
                        break;
                }
                break;
        }
    }

    /**
     * 参戦者の情報をリセットする
     */
    clearAttendList(){
        this.attendB.length = 0;
        this.attendM.length = 0;
        this.attackB.clear;
        this.attackM.clear;
        this.sampleB.clear;
        this.sampleM.clear;
    }
}

module.exports = BossData;