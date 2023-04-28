
import datetime


def move_now(days=0, fm='%Y-%m-%dT%H:%M:%S'):
    return str((datetime.datetime.now() + datetime.timedelta(days=days)).strftime(fm))

def timestr2datetime(date_time, fm="%a, %d %b %Y %H:%M:%S %z"):
    """
    %a, %d %b %Y %H:%M:%S %z
    """
    try:
        return datetime.datetime.strptime(date_time, fm)
    except Exception as e:
        return datetime.datetime.now()

if __name__ == "__main__":
    print(move_now(fm="%Y-%m-%d"))
    print(timestr2datetime("Thu, 09 Feb 2023 13:07:42 +0000"))