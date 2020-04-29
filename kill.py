"""
杀死占用52075端口的进程，让协同始终能使用52075端口
Time: 2020/4/26 9:39
Author: chengyao
Email: chengy_work@163.com
"""
import os

PORT = 52075


def killer():
    PID = None
    PPID = None
    # 根据端口号获取占用该端口号进程pid
    cmd = 'netstat -aon|findstr {}'.format(str(PORT))
    with os.popen(cmd) as r:
        res = r.read().split('\n')
    for line in res:
        temp = [i for i in line.split(' ') if i != '']
        if len(temp) > 4:
            PID = int(temp[4])
    # 根据进程pid查询其父进程ppid
    try:
        cmd = "wmic process where ProcessId={} get ParentProcessId".format(PID)
        with os.popen(cmd) as r:
            res = r.readlines()
        PPID = [line for line in res if line != '\n'][1].split('\n')[0]
    except Exception:
        pass
    # 根据pid和ppid来杀死进程
    try:
        cmd1 = "taskkill /pid {}  -t  -f".format(str(PID))
        cmd2 = "taskkill /pid {}  -t  -f".format(str(PPID))
        os.popen(cmd1)
        os.popen(cmd2)
    except Exception:
        pass


if __name__ == '__main__':
    try:
        killer()
    except Exception:
        pass
