from time import time

TIMESTAMP = 0 # date du dernier appui
INTERVAL = 500 # temps minimum entre 2 appuis en ms

BANK = 0

def route(path, args, send, get):
    """
        path: osc address (string: '/pedalBoard/button')
        args: osc arguments (list)

        send: voir scenes.py
        get: voir scenes.py
    """

    #### Anti double appui
    global TIMESTAMP
    now = time() * 1000
    delta = now - TIMESTAMP
    if delta < INTERVAL:
        print('OSC: double appui ignoré: %s, %s' % (path, args))
        return
    TIMESTAMP = now
    ####

    print('OSC: %s, %s' % (path, args))

    global BANK
    number = args[0]
    if path == '/pedalBoard/button':

        if number >= 1 and number <= 4:

            if BANK == 0:
                send('server', '/scene', number)
            elif BANK == 1:
                send('server', '/scene', number + 4)

            send('server', '/subscene', 'INIT')

        elif number == 5:

            send('server', '/subscene', 1)

        elif number == 6:
            BANK = 0

        elif number == 7:
            BANK = 1

        elif number == 8:
            pass
