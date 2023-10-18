import json

def input_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def output_json(filename, obj):
    with open(filename, 'w') as f:
        json.dump(obj, f, indent=4, ensure_ascii=False)

class AplConst:
    '''
    アプリケーションで使用する定数を格納するクラス
    定数は"conf/aplConstans.json"から取得する。

    Attributes
    ----------
    aplConst : AttrDict 定数を格納するオブジェクト
    '''
    def __init__(self, aplPath):
        self.aplConst = input_json(aplPath + "/conf/aplConstants.json")
        #self.aplConst = AttrDict(input_json(aplPath + "/conf/aplConstants.json"))
    
    def get(self, key):
        '''
        指定された名前に紐づく定数(String)を返却する。
        見つからない場合はNoneを返却する。

        Parameters
        ----------
        key : String 取得する定数の名称

        Returns
        -------
        value : String 取得した定数の結果
        '''
        value = self.aplConst
        keys = key.split(".")
        for name in keys:
            if (value == None):
                break
            value = value.get(name)
        return value
