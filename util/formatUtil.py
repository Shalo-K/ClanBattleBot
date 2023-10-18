import datetime

def datetimeFormat(target, format):
    '''
    日時情報をフォーマットする。
    
    Parameters
    ----------
    target : string 変換する日時情報(yyyymmddhhmiss)
    format : string 変換のフォーマット(datetime.strftime)

    Returns
    -------
    result : string 変換後の日時情報

    '''
    result = None
    if (target == "now"):
        dt = datetime.datetime.now()
    else:
        param = target.split()
        # パラメータチェック
        if (len(param) != 2):
            return result
        if (len(param[0]) != 8 or len(param[1]) != 6):
            return result

        # パラメータからdatetime型に変換
        dt = datetime.datetime(
            year = param[0][0:4],
            month = param[0][4:6],
            day = param[0][6:8],
            hour = param[1][0:2],
            minute = param[1][2:4],
            second = param[1][4:6],
            microsecond = 0
        )
    
    result = dt.strftime(format)
    return result