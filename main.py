import sys
import core
import re
import cakelib2
import time
import json
import glob
import threading
import imp
import text

'''
This is just the base bot with little or no personality or commands.
It will be up to you guys to come up with silly/funny commands or command ideas, and
give the bot some personality!!! :3. I will be working on a RPG that swill came
up with the ideas for, and if you complete a command or have an idea for one send me it
at myth and I will update the core file with the command. This main file will also be looked over
by someone else. For those of you who have never coded just install python and put all of the files in a
single folder and run the main.py. should log in to the chat on the voxela account, which is a random
account that i made for this. Its password is encrypted but if you know how it is easy to decrypt it. so basically
dont go sharing this around with everyone.
'''

_prefix_ = '*'

class Lemonator(cakelib2.Main):

    def lemonate(self):
        threading.Thread(target=core.gLastmsg, args=(self,), daemon = True).start()

    def e(self, string, user, uid, chat, cake):
        if "password" in string.lower(): return 'fail'
        else:
            try:
                ret = eval(string.decode() if type(string) == bytes else string)
                return str(repr(ret))
            except Exception: return str('%s' % get_error())

    def reindex(self, string, user, uid, chat, othervars):
        try: list(map(lambda x: exec('imp.reload({a})'.format(a=x.replace('.py','') if x.replace('.py','') != 'main' else 'core')), glob.glob('*.py')))
        except Exception: return '%s' % get_error()
        return 'Reloaded Modules.'

    def onPost(self, user, chat, message):
        mods = core._mods
        user.rank = 2 if user.name.lower() in mods else 1
        othervars = [message, self.pm, self, user]
        uid = message.uid
        user = user.name.lower()
        prefix = chat.prefix
        if len(message.content) > 0:
            try:
                if user in core.notify:
                    lmessage = json.loads(core.notify[user])
                    chat.post(lmessage)
                    del core.notify[user]
                    f = open("notify.txt", "w")
                    for i in core.notify:
                        lmessage = json.loads(core.notify[i])
                        f.write(json.dumps([i, lmessage]))
                    f.close()
            except Exception as e: print(e)
            core.lastmsg[user] = [cakelib2.escape(message.content), chat.chatname, time.time()]
            data = message.content.split(" ", 1)
            if len(data) > 1: func, string = data[0], data[1]
            else: func, string = data[0].lower(), ""
            try:
                _prefix = True if func[0] == prefix else False
                func = func[1:] if _prefix == True else func
            except: _prefix = False
            if _prefix:
                if hasattr(self, func):
                    try:
                        if othervars[3].rank < 2:
                            chat.post('You do not have moderator privleges.')
                            return
                        chat.post(getattr(self, func)(string, user, uid, chat, othervars))
                    except Exception: chat.post(get_error())
                elif hasattr(core, func):
                    try:
                        resp = getattr(core, func)(string, user, uid, chat, othervars)
                        if resp == None: resp = 'incorrect command usage'
                        chat.post(resp)
                    except Exception: chat.post(get_error())
            
debug = False
if debug == True: core.room_list = ['timecapsule']            
        
def get_error():
    try: et, ev, tb = sys.exc_info()
    except Exception as e: print(e)
    if not tb: return None
    while tb:
            line = tb.tb_lineno
            file = tb.tb_frame.f_code.co_filename
            tb = tb.tb_next
    try: return "%s: %i: %s[%s]" % (file, line, et.__name__, str(ev))
    except Exception as e: print(e)

def load_utill():
    f = open('utill.txt', 'r')
    data = f.read()
    p = re.compile(r"<p>(.*?)</p>").search(data).group(1)
    k = re.compile(r"<k>(.*?)</k>").search(data).group(1)
    f.close()
    return (p, k)
    
if __name__ == '__main__':
    try:
        p, k = load_utill()
        Lemonator.start('voxela',core.decrypt(k, p), core.room_list, pm=True)
    except:
        'caek' == 'WATER MALONE'
        print(get_error())
