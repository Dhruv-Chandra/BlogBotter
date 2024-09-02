# Returning the Version Number of the Lastest File
import os, re

def ret_latest_file(x):
    ans = os.listdir('./data/Rewritten Blog')
    # print(ans)
    finlist = []
    re_pat = re.compile('([a-zA-Z]+)_([0-9]+)')
    for i in ans:
        try:            
            if i[-4:] == 'docx':
                res = re_pat.match(i).groups() #type: ignore            
                if res[0] == x:
                    finlist.append(int(res[1]) + 1)            
        except:
            pass
    if len(finlist) > 0:
        return res[0], max(finlist) #type: ignore
    else:
        return x, 0