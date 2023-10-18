import os
from attrdict import AttrDict
from util import fileController

##### configの読み込み #####
aplPath = os.getcwd()
aplConst = AttrDict(fileController.input_json(aplPath + "/conf/aplConstants.json"))

class BossData:
    '''
    ボス情報を定義する。
    
    Attributes
    ----------
    id       : int    ボスの番号
    name     : string ボスの名前
    maxHp    : int    ボスの最大HP
    curHp    : int    ボスの現在HP
    manageId : array  ボスの管理用メッセージID
    attendB  : list   物理参加者
    attendM  : kist   魔法参加者
    attackB  : dict   物理ダメージ
    attackM  : dict   魔法ダメージ
    '''
    def __init__(self, id, name, hp):
        '''
        Parameters
        ----------
        id     : int    ボスの番号
        name   : string ボスの名前
        hp     : int    ボスの最大HP
        '''
        self.id = id
        self.name = name
        self.maxHp = hp
        self.curHp = hp
        self.manageId = []
        self.attendB = []
        self.attendM = []
        self.attackB = dict()
        self.attackM = dict()

    def setName(self, name):
        '''
        ボスの名前を変更する。

        Parameters
        ----------
        name : string name
        '''
        self.name = name
        
    def setMaxHp(self, maxHp):
        '''
        ボスの最大HPを変更する。

        Parameters
        ----------
        maxHp : int maxHP
        '''
        self.maxHp = maxHp
    
    def setCurHp(self, curHp):
        '''
        ボスの現在HPを変更する。
        
        Parameters
        ----------
        curHp : int curHP
        '''
        self.curHp = curHp
    
    def setManageId(self, manageId):
        '''
        ボスの管理メッセージIDを変更する。
        
        manageId : string manageID
        '''
        self.manageId.length = 0
        self.manageId.push(manageId)
        
    def createInfoText(self, memberNameMap):
        '''
        ボス情報のテキストを編集する。
        
        Parameters
        ----------
        memberNameMap : dict ユーザ情報 

        Returns
        -------
        text : string メッセージテキスト
        '''
        text = '```' + self.name + ' : ' + self.curHp + '/' + self.maxHp + '\n\n現在の参加者\n'

        # 物理
        for user in self.attendB:
            text = text + aplConst.reaction.crossed_swords + memberNameMap.get(self.attendB[user]) + '\n'
        
        # 魔法
        for user in self.attendM:
            text = text + aplConst.reaction.mage + memberNameMap.get(self.attendM[user]) + '\n'
        
        text = text + '```'
        return text
    
    def controllAttendUser(self, controllType, userId, reactionType):
        '''
        ボスごとの参加ユーザを追加/削除する。
        controllType : string 操作の種類 (追加/削除)
        userId       : string ユーザID
        reactionType : string リアクションの種類 (物理/魔法)
        '''
        if (reactionType == "b"):
            # 物理
            if (controllType == "add"):
                # 追加
                if (userId not in self.attendB):
                    self.attendB.append(userId)
                    # self.attackB.set(userId, '0')
                
            if (userId == "del"):
                # 削除
                if userId in self.attendB:
                    self.attendB.remove(userId)
                    # self.attackB.delete(userId)
            
        if (reactionType == "m"):
            # 魔法
            if (controllType == "add"):
                # 追加
                if (userId not in self.attendM):
                    self.attendM.append(userId)
                    # self.attackM.set(userId, '0')
                
            if (controllType == "del"):
                # 削除
                if (userId in self.attendM):
                    self.attendM.remove(userId)
                    # self.attackM.delete(userId)

    def clearAttendList(self):
        '''
        参戦者の情報をリセットする。
        '''
        self.attendB.clear
        self.attendM.clear
        # self.attackB.clear
        # self.attackM.clear
