/**
 * @property {number} id ボスの番号
 * @property {string} name ボスの名前
 * @property {number} maxHp ボスの最大HP
 * @property {number} curHp ボスの現在HP
 * @property {array} manageId ボスの管理用メッセージID
 * @property {string} voteId 参加者投票用ID
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
    constructor(id, name, hp, voteId){
        this.id = id;
        this.name = name;
        this.maxHp = hp;
        this.curHp = hp;
        this.manageId = [];
        this.voteId = voteId;
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
     * ボス情報のテキストを編集する
     * @param {Map} memberNameMap ユーザ情報 
     * @returns {string} メッセージテキスト
     */
    createInfoText(memberNameMap) {
        let user;
        let text = '```' + this.name + ' : ' + this.curHp + '/' + this.maxHp + '\n\n現在の参加者\n';

        // 物理
        for (user in this.attendB){
            text = text + memberNameMap.get(this.attendB[user]) + '(物理) ' + this.attackB.get(this.attendB[user]) + ' ' + this.sampleB.get(this.attendB[user]) + '(予定)\n';
        }
        
        // 魔法
        for (user in this.attendM){
            text = text + memberNameMap.get(this.attendM[user]) + '(魔法) ' + this.attackM.get(this.attendM[user]) + ' ' + this.sampleM.get(this.attendM[user]) + '(予定)\n';
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
            case 'b':
                switch(controllType){
                    case 'add':
                        if (!this.attendB.includes(userId)){
                            this.attendB.push(userId);
                            this.attackB.set(userId, '0');
                            this.sampleB.set(userId, '0');
                        }
                        break;
                    case 'del':
                        if (this.attendB.includes(userId)){
                            this.attendB = this.attendB.filter(item => item.match(userId) == null);
                            this.attackB.delete(userId);
                            this.sampleB.delete(userId);
                        }
                        break;
                }
                break;
            case 'm':
                switch(controllType){
                    case 'add':
                        if (!this.attendM.includes(userId)){
                            this.attendM.push(userId);
                            this.attackM.set(userId, '0');
                            this.sampleM.set(userId, '0');
                        }
                        break;
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
}

module.exports = BossData;