from time import time

TIMESTAMP = 0 # date du dernier appui
INTERVAL = 500 # temps minimum entre 2 appuis en ms

def route(type, channel, number, value, send, get):
    """
        type: 'note', 'program' ou 'control'
        channel: 1 à 15
        data: [x, y] où x est le numéro du contrôle et y la valeur

        send: voir scenes.py
        get: voir scenes.py
    """

    #### Anti double appui
    global TIMESTAMP
    now = time() * 1000
    delta = now - TIMESTAMP
    if delta < INTERVAL:
        print('MIDI: double appui ignoré' % )
        return
    TIMESTAMP = now
    ####

    print('MIDI: %s, %s, %s, %s' % (type, channel, control, value))

    if type == 'program':
        # number -> numéro du program change -> numéro de la scène
        send('server', '/scene', number + 1)
        send('server', '/subscene', 'INIT')
        pass

    # exemple de stop + reset
    # send('server', '/stop')
    # send('server', '/subscene', 'INIT')

    if type == 'control':
        """
        Exemple pour un controle fixe qui ne passe par les scènes

            if control == 8:
                send('/sl/-1/hit', 'mute_on')
            else:
                receive('/subscene', control)

        """
        send('server', '/subscene', number)
        pass
