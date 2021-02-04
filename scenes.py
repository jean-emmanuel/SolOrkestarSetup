"""

########################

Chaque morceau (ou "scene") est défini comme suit:

def haiduk(subscene, send, get):

    # ici le code du morceau


########################


subscene: valeur transmise en osc à l'adresse /subscene


########################

send(adresse, argument_1, argument_2, etc): fonction d'envoi des commandes à sooperlooper

Exemple :
    send('/sl/0/hit', 'record') # armer la boucle 0
    send('/sl/-1/set', 'mute_on') # muter toutes les pisbouclestes
    send('/sl/[0,1]/set', 'record') # armer les boucles 0 et 1

    send('server', '/stop')
    send('ardour', '/sl/-1/set', 'sync', 1)


Par défaut, send envoie à Sooperlooper, mais on peut préciser en 1er argument une destination différente:
  - 'server' (serveur python)
  - 'ardour' (3819)
  - un port osc arbitraire


Exemple : muter une piste dans ardour

    send('ardour', '/strip/mute', 1, 1) # muter la 1ere piste
    send('ardour', '/strip/mute', 1, 0) # demuter la 1ere piste
    send('ardour', '/master/mute', 1) # muter le master
    send('ardour', '/master/mute', 0) # demuter le master



########################

get(adresse, nom_parametre): fonction de récupération d'une valeur de sooperlooper

Exemple : muter la boucle 0 à la fin de la prochaine iteration

    # on récupère la position actuelle
    position = get('/sl/0/get', 'loop_pos')
    # on la compare à la position actuelle
    while get('/sl/0/get', 'loop_pos') >=  position:
        pass # on recommence tant que la condition n'est pas vraie
    # on mute la boucle une fois la condition vraie
    send('/sl/0/hit', 'mute')

def attendre_debut(get, ):
    position = get('/sl/0/get', 'loop_pos')
    while get('/sl/0/get', 'loop_pos') >=  position:
        pass

########################

Penser à déclarer les variables globales (boucle active, état de la scène, etc)


SCENE_STATE = 0
ACTIVE_LOOP = 0

def haiduk(subscene, send, get):

    global SCENE_STATE, ACTIVE_LOOP

    # etc

########################

"""

SCENE_STATE = 0
ACTIVE_LOOP = 0
def attendre_debut(get, boucle=0):
    print('ATTENTE')
    position = get('/sl/' + str(boucle) + '/get', 'loop_pos')
    next = position
    while next >= position:
        next = get('/sl/' + str(boucle) + '/get', 'loop_pos')
        pass


def reset(subscene, send, get):
    global SCENE_STATE, ACTIVE_LOOP
    SCENE_STATE = 0
    ACTIVE_LOOP = 0
    send('/sl/-1/hit', 'pause')
    send('/sl/-1/hit', 'undo_all')
    send('/sl/-1/hit', 'mute_off')
    send('/set', 'sync_source', 0)
    send('/sl/-1/set', 'sync', 0)
    send('/sl/-1/set', 'quantize', 0)
    send('/sl/-1/set', 'rec_thresh', 0)
    send('ardour', '/strip/mute', 1, 1) # muter la 1ere piste
    send('ardour', '/strip/mute', 2, 1)
    send('ardour', '/strip/mute', 3, 1)
    send('ardour', '/strip/mute', 4, 1)
    send('ardour', '/strip/mute', 5, 1)
    send('ardour', '/strip/mute', 6, 1)
    send('ardour', '/strip/mute', 7, 1)
    send('ardour', '/strip/mute', 8, 1)
    send('ardour', '/strip/mute', 9, 1)
    send('ardour', '/strip/mute', 10, 1)
    send('ardour', '/strip/mute', 11, 1)
    send('ardour', '/strip/mute', 12, 1)
    send('ardour', '/strip/mute', 13, 1)

def boutons_fixes(subscene, send, get):

    global SCENE_STATE, ACTIVE_LOOP

    if subscene == 2:
        pass
    elif subscene == 3:
        pass



def haiduk(subscene, send, get):


    global SCENE_STATE, ACTIVE_LOOP

    if subscene == 'INIT':
        reset(subscene, send, get)
        print('Scene haiduk started')
        return

    elif subscene == 1: # CC1 = NEXT

        SCENE_STATE += 1
        print('Scene haiduk on subscene %s' % SCENE_STATE)

        # CONDUITE LINEAIRE
        if SCENE_STATE == 1:
            send('ardour', '/strip/mute', 1, 0)
            send('ardour', '/strip/mute', 7, 0)
            send('ardour', '/strip/mute', 9, 0)
            send('/sl/0/set', 'rec_thresh', '0.5')
            send('/sl/5/set', 'rec_thresh', '0.5')
            send('/sl/[0,5]/hit', 'record')
            ACTIVE_LOOP = 0

        elif SCENE_STATE == 2:
            send('/sl/[0,5]/hit', 'record')
            send('/set', 'sync_source', 1)
            send('/set', 'overdub_quantized', 1)
            send('/sl/-1/set', 'sync', 1)
            send('/sl/-1/set', 'playback_sync', 1)
            send('/sl/-1/set', 'quantize', 3)
            send('ardour', '/strip/mute', 1, 1)
            send('ardour', '/strip/mute', 7, 1)
            send('ardour', '/strip/mute', 9, 1)
            send('ardour', '/strip/mute', 8, 0)

        elif SCENE_STATE == 3:
            #rec basse A1
            send('/sl/1/hit', 'record')
            send('ardour', '/strip/mute', 2, 0)
            ACTIVE_LOOP = 1

        elif SCENE_STATE == 4:
            #fin rec basse A1, prépa rec basse A2
            send('/sl/1/hit', 'record')
            send('/sl/2/hit', 'record')
            attendre_debut(get, 0)
            send('/sl/1/hit', 'mute_on')
            ACTIVE_LOOP = 2

        elif SCENE_STATE == 5:
            send('/sl/2/hit', 'record')
            attendre_debut(get, 0)
            send('ardour', '/strip/mute', 2, 1)

        elif SCENE_STATE == 6:
            #rec melo A1, mute A2, demute A1
            send('/sl/3/hit', 'record')
            ACTIVE_LOOP = 3
            attendre_debut(get, 0)
            send('/sl/2/hit', 'mute_on')
            send('/sl/1/hit', 'mute_off')
            send('ardour', '/strip/mute', 3, 0)

        elif SCENE_STATE == 7:
            #fin rec melo A1, rec melo A2, mute A1, demute A2
            send('/sl/3/hit', 'record')
            ACTIVE_LOOP = 4
            attendre_debut(get, 0)
            send('/sl/4/hit', 'record')
            send('/sl/1/hit', 'mute_on')
            send('/sl/2/hit', 'mute_off')
            send('/sl/4/hit', 'mute_on')

        elif SCENE_STATE == 8:
            send('/sl/4/hit', 'record')
            send('ardour', '/strip/mute', 3, 1)

        elif SCENE_STATE == 9:
            #play A1, suppr voix
            #position = get('/sl/0/get', 'loop_pos')
            attendre_debut(get, 0)
            send('/sl/1/hit', 'mute_on')
            send('/sl/2/hit', 'mute_off')
            send('/sl/3/hit', 'mute_on')
            send('/sl/4/hit', 'mute_off')
            send('/sl/5/hit', 'undo')

#---------------------------------------

        elif SCENE_STATE == 10:
            #play A2
            position = get('/sl/0/get', 'loop_pos')
            attendre_debut(get, 0)
            send('/sl/1/hit', 'mute_off')
            send('/sl/2/hit', 'mute_on')
            send('/sl/3/hit', 'mute_off')
            send('/sl/4/hit', 'mute_on')

        elif SCENE_STATE == 11:
            #play A1
            position = get('/sl/0/get', 'loop_pos')
            attendre_debut(get, 0)
            send('/sl/1/hit', 'mute_on')
            send('/sl/2/hit', 'mute_off')
            send('/sl/3/hit', 'mute_on')
            send('/sl/4/hit', 'mute_off')

        elif SCENE_STATE == 12:
            #mute A1&A2, rec caval
            position = get('/sl/0/get', 'loop_pos')
            attendre_debut(get, 0)
            send('/sl/2/hit', 'mute_on')
            send('/sl/4/hit', 'mute_on')
            send('/sl/5/hit', 'record')
            ACTIVE_LOOP = 5

        elif SCENE_STATE == 13:
            send('/sl/5/hit', 'record')

        elif SCENE_STATE == 14:
            #rec basse B1
            send('/sl/6/hit', 'record')
            ACTIVE_LOOP = 6

        elif SCENE_STATE == 15:
            send('/sl/6/hit', 'record')

        elif SCENE_STATE == 16:
            #mute caval & B1, rec basse B2
            send('/sl/6/hit', 'record')
            send('/sl/7/hit', 'record')
            ACTIVE_LOOP = 7
            position = get('/sl/0/get', 'loop_pos')
            attendre_debut(get, 0)
            send('/sl/5/hit', 'mute_on')
            send('/sl/6/hit', 'mute_on')

        elif SCENE_STATE == 17:
            send('/sl/7/hit', 'record')

        elif SCENE_STATE == 18:
        #play B1 pendant que je prends le mélo
            position = get('/sl/0/get', 'loop_pos')
            attendre_debut(get, 0)
            send('/sl/5/hit', 'mute_off')
            send('/sl/6/hit', 'mute_off')
            send('/sl/7/hit', 'mute_on')

        elif SCENE_STATE == 19:
        #rec mélo B2
            send('/sl/9/hit', 'record')
            ACTIVE_LOOP = 9
            position = get('/sl/0/get', 'loop_pos')
            attendre_debut(get, 0)
            send('/sl/5/hit', 'mute_on')
            send('/sl/6/hit', 'mute_on')
            send('/sl/7/hit', 'mute_off')

        elif SCENE_STATE == 20:
            send('/sl/9/hit', 'record')

        elif SCENE_STATE == 21:
        #rec violon B1
            send('/sl/8/hit', 'record')
            ACTIVE_LOOP = 8
            position = get('/sl/0/get', 'loop_pos')
            attendre_debut(get, 0)
            send('/sl/5/hit', 'mute_off')
            send('/sl/6/hit', 'mute_off')
            send('/sl/7/hit', 'mute_on')
            send('/sl/9/hit', 'mute_on')

        elif SCENE_STATE == 22:
            send('/sl/8/hit', 'record')

        elif SCENE_STATE == 23:
        #play B2 sur chant
            position = get('/sl/0/get', 'loop_pos')
            attendre_debut(get, 0)
            send('/sl/5/hit', 'mute_on')
            send('/sl/6/hit', 'mute_on')
            send('/sl/7/hit', 'mute_off')
            send('/sl/8/hit', 'mute_on')
            send('/sl/9/hit', 'mute_off')

        elif SCENE_STATE == 24:
        #play B1
            position = get('/sl/0/get', 'loop_pos')
            attendre_debut(get, 0)
            send('/sl/5/hit', 'mute_off')
            send('/sl/6/hit', 'mute_off')
            send('/sl/7/hit', 'mute_on')
            send('/sl/8/hit', 'mute_off')
            send('/sl/9/hit', 'mute_on')

        elif SCENE_STATE == 25:
        #play B2 sur chant
            position = get('/sl/0/get', 'loop_pos')
            attendre_debut(get, 0)
            send('/sl/5/hit', 'mute_on')
            send('/sl/6/hit', 'mute_on')
            send('/sl/7/hit', 'mute_off')
            send('/sl/8/hit', 'mute_on')
            send('/sl/9/hit', 'mute_off')

        elif SCENE_STATE == 26:
        #play B1
            position = get('/sl/0/get', 'loop_pos')
            attendre_debut(get, 0)
            send('/sl/5/hit', 'mute_off')
            send('/sl/6/hit', 'mute_off')
            send('/sl/7/hit', 'mute_on')
            send('/sl/8/hit', 'mute_off')
            send('/sl/9/hit', 'mute_on')

        elif SCENE_STATE == 27:
        #mute all B, play A1 sans la basse sur un tour
            position = get('/sl/0/get', 'loop_pos')
            attendre_debut(get, 0)
            send('/sl/[5,6,7,8,9]/hit', 'mute_on')
            send('/sl/3/hit', 'mute_off')
            position = get('/sl/0/get', 'loop_pos')
            attendre_debut(get, 0)
            send('/sl/1/hit', 'mute_off')

        elif SCENE_STATE == 28:
        #mute A1, play A2
            position = get('/sl/0/get', 'loop_pos')
            attendre_debut(get, 0)
            send('/sl/1/hit', 'mute_off')
            send('/sl/2/hit', 'mute_on')
            send('/sl/3/hit', 'mute_off')
            send('/sl/4/hit', 'mute_on')

        elif SCENE_STATE == 29:
            #play A1
            position = get('/sl/0/get', 'loop_pos')
            attendre_debut(get, 0)
            send('/sl/1/hit', 'mute_on')
            send('/sl/2/hit', 'mute_off')
            send('/sl/3/hit', 'mute_on')
            send('/sl/4/hit', 'mute_off')

        elif SCENE_STATE == 30:
        #dernier tour
            position = get('/sl/0/get', 'loop_pos')
            attendre_debut(get, 0)
            send('/sl/[0,2,4]/hit', 'mute_on')

    else:
        boutons_fixes(subscene, send, get)

def capra(subscene, send, get):


    global SCENE_STATE, ACTIVE_LOOP

    if subscene == 'INIT':
        # INIT

        reset(subscene, send, get)
        print('Scene capra started')
        return

    elif subscene == 1: # CC1 = NEXT

        SCENE_STATE += 1
        print('Scene capra on subscene %s' % SCENE_STATE)


        # CONDUITE LINEAIRE
        if SCENE_STATE == 1:
            #rec kick et méloA
            send('ardour', '/strip/mute', 12, 0)
            send('ardour', '/strip/mute', 1, 0)
            send('ardour', '/strip/mute', 3, 0)
            send('/sl/[0,1]/set', 'rec_thresh', 0.02)
            send('/sl/[0,1]/hit', 'record')
            ACTIVE_LOOP = 0

        elif SCENE_STATE == 2:
            #fin rec méloA, rec méloB
            #fin record kick meloA, synchro kick, rec meloB
            send('/sl/[0,1]/hit', 'record')
            send('ardour', '/strip/mute', 1, 1)
            send('/set', 'sync_source', 1)
            send('/set', 'overdub_quantized', 1)
            send('/sl/-1/set', 'sync', 1)
            send('/sl/-1/set', 'playback_sync', 1)
            send('/sl/-1/set', 'quantize', 3)
            import time
            time.sleep(4)
            send('/sl/2/hit', 'record')
            attendre_debut(get, 0)
            send('/sl/1/hit', 'mute_on')
            import time
            time.sleep(4)
            send('/sl/2/hit', 'record')
            attendre_debut(get, 0)
            send('ardour', '/strip/mute', 3, 1)
            send('ardour', '/strip/mute', 12, 1)
            send('ardour', '/strip/mute', 8, 0)
            send('/sl/[1,2]/hit', 'mute')


        elif SCENE_STATE == 3:
            #mute mélo B, play mélo A, chant
            send('ardour', '/strip/mute', 3, 0) #!!!! à effacer
            send('ardour', '/strip/mute', 7, 0)
            attendre_debut(get, 0)
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            send('/sl/1/hit', 'mute_on')
            send('/sl/2/hit', 'mute_off')

        elif SCENE_STATE == 4:
            #rec caval
            send('/sl/6/hit', 'record')
            send('ardour', '/strip/mute', 5, 0)
            attendre_debut(get, 0)
            send('/sl/[1,2]/hit', 'mute')
            import time
            time.sleep(4)
            send('/sl/6/hit', 'record')
            attendre_debut(get, 0)
            send('ardour', '/strip/mute', 5, 1)


        elif SCENE_STATE == 5:
            #rec bassA&B, play A&B et caval
            send('/sl/3/hit', 'record')
            send('ardour', '/strip/mute', 2, 0)
            send('ardour', '/strip/mute', 8, 1)
            send('ardour', '/strip/mute', 13, 0)
            attendre_debut(get, 0)
            send('/sl/6/hit', 'mute_on')
            import time
            time.sleep(4)
            send('/sl/[3,4]/hit', 'record')
            attendre_debut(get, 0)
            send('/sl/[1,2,3]/hit', 'mute')
            import time
            time.sleep(4)
            send('/sl/4/hit', 'record')
            attendre_debut(get, 0)
            send('/sl/[1,2,3,4]/hit', 'mute')
            send('ardour', '/strip/mute', 2, 1)
            send('ardour', '/strip/mute', 8, 0)
            send('ardour', '/strip/mute', 13, 1)
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            send('/sl/[1,2,3,4]/hit', 'mute')
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            send('/sl/[1,2,3,4]/hit', 'mute')
            send('/sl/6/hit', 'mute')

        elif SCENE_STATE == 6:
            #play violon AA BB AA, bascule sur A vocal
            send('ardour', '/strip/mute', 4, 0)
            send('/sl/6/hit', 'mute')
            attendre_debut(get, 0)
            #1er A
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #2e A
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #1er B
            send('/sl/[1,2,3,4]/hit', 'mute')
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #2e B
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #1er A
            send('/sl/[1,2,3,4]/hit', 'mute')
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #2e A
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #A vocal
            send('ardour', '/strip/mute', 4, 1)

        elif SCENE_STATE == 7:
            #break caval mélo vers couplet AB AB puis solo clar méloA seul
            attendre_debut(get, 0)
            send('/sl/[0,2,3,4]/hit', 'mute_on')
            send('/sl/[1,6]/hit', 'mute_off')
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #A
            send('/sl/6/hit', 'mute_on')
            send('/sl/[0,1,3]/hit', 'mute_off')
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #B
            send('/sl/[1,2,3,4]/hit', 'mute')
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #A
            send('/sl/[1,2,3,4]/hit', 'mute')
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #B
            send('/sl/[1,2,3,4]/hit', 'mute')
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #solo méloA seul
            send('ardour', '/strip/mute', 6, 0)
            send('/sl/-1/hit', 'mute_on')
            send('/sl/1/hit', 'mute_off')

        elif SCENE_STATE == 8:
            #solo arrivée kick et basse
            attendre_debut(get, 0)
            send('/sl/[0,3]/hit', 'mute_off')

        elif SCENE_STATE == 9:
            #fin solo, pont caval
            attendre_debut(get, 0)
            send('ardour', '/strip/mute', 6, 1)
            send('/sl/[0,3,6]/hit', 'mute')

        elif SCENE_STATE == 10:
            #violon AA BB AA
            send('ardour', '/strip/mute', 4, 0)
            attendre_debut(get, 0)
            #A mélo seul
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #A tutti
            send('/sl/[0,3]/hit', 'mute')
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #B 1
            send('/sl/[1,2,3,4]/hit', 'mute')
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #B 2
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            # A 1
            send('/sl/[1,2,3,4]/hit', 'mute')
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            # A 2
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            send('/sl/-1/hit', 'mute_on')

    else:
        boutons_fixes(subscene, send, get)

def kamav(subscene, send, get):


    global SCENE_STATE, ACTIVE_LOOP

    if subscene == 'INIT':
        # INIT

        reset(subscene, send, get)
        print('Scene kamav started')
        return

    elif subscene == 1: # CC1 = NEXT

        SCENE_STATE += 1
        print('Scene kamav on subscene %s' % SCENE_STATE)


        # CONDUITE LINEAIRE
        if SCENE_STATE == 1:
            #rec percus
            send('ardour', '/strip/mute', 4, 0)
            send('ardour', '/strip/mute', 8, 0)
            send('ardour', '/strip/mute', 1, 0)
            send('/sl/0/set', 'rec_thresh', 0.05)
            send('/sl/0/hit', 'record')
            ACTIVE_LOOP = 0

        elif SCENE_STATE == 2:
            send('/sl/0/hit', 'record')
            send('/set', 'sync_source', 1)
            send('/set', 'overdub_quantized', 1)
            send('/sl/-1/set', 'sync', 1)
            send('/sl/-1/set', 'playback_sync', 1)
            send('/sl/-1/set', 'quantize', 3)
            send('ardour', '/strip/mute', 1, 1)
            ACTIVE_LOOP = 1

        elif SCENE_STATE == 3:
            #rec violon intro, ABB & C, play C ad lib
            send('/sl/1/hit', 'record')
            attendre_debut(get, 0)
            import time
            time.sleep(4)
            send('/sl/1/hit', 'record')
            send('/sl/2/hit', 'record')
            attendre_debut(get, 0)
            send('/sl/1/hit', 'mute_on')
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            import time
            time.sleep(4)
            send('/sl/3/hit', 'record')
            attendre_debut(get, 0)
            import time
            time.sleep(4)
            send('/sl/2/hit', 'record')
            send('/sl/3/hit', 'record')
            attendre_debut(get, 0)
            send('/sl/2/hit', 'pause')
            send('/sl/3/hit', 'pause')
            send('/sl/1/hit', 'mute_off')
            send('/sl/0/hit', 'mute_on')
            send('ardour', '/strip/mute', 7, 0)
            send('ardour', '/strip/mute', 3, 0) # à supprimer !!!!!!!!!!!

        elif SCENE_STATE == 4:
            #play violonABB et percus + violonC x 2
            send('/sl/2/hit', 'trigger')
            attendre_debut(get, 0)
            send('/sl/1/hit', 'mute_on')
            send('/sl/0/hit', 'mute_off')
            import time
            time.sleep(12)
            send('/sl/3/hit', 'trigger')
            attendre_debut(get, 2)
            send('/sl/2/hit', 'pause')

        elif SCENE_STATE == 5:
            #rec voxA sur A, B et C
            send('/sl/4/hit', 'record')
            ACTIVE_LOOP = 4
            attendre_debut(get, 0)
            send('ardour', '/strip/mute', 4, 1)
            send('/sl/2/hit', 'trigger')
            send('/sl/3/hit', 'mute_on')
            import time
            time.sleep(12)
            send('/sl/4/hit', 'record')
            send('/sl/6/hit', 'record')
            attendre_debut(get, 2)
            send('/sl/2/hit', 'pause')
            send('/sl/3/hit', 'mute_off')
            send('/sl/4/hit', 'pause')
            import time
            time.sleep(3)
            attendre_debut(get, 0)
            import time
            time.sleep(3)
            send('/sl/6/hit', 'record')

        elif SCENE_STATE == 6:
            #enchaîne sur ABB
            attendre_debut(get, 0)
            send('/sl/[2,4]/hit', 'trigger')
            send('/sl/[3,6]/hit', 'pause')
            import time
            time.sleep(12)
            attendre_debut(get, 2)
            send('/sl/[2,4]/hit', 'pause')
            send('/sl/[3,6]/hit', 'trigger')

        elif SCENE_STATE == 7:
            #odub voxC
            send('/set', 'overdub_quantized', 1)
            send('/sl/6/hit', 'overdub')
            attendre_debut(get, 0)

        elif SCENE_STATE == 8:
            #fin odub voxC
            send('/sl/6/hit', 'overdub')

        elif SCENE_STATE == 9:
            #mute tout sauf voxC
            attendre_debut(get, 6)
            send('/sl/[0,1,3]/hit', 'mute_on')

        elif SCENE_STATE == 10:
            #dernier tour
            position = get('/sl/6/get', 'loop_pos')
            attendre_debut(get, 6)
            send('/sl/[0,3,6]/hit', 'pause')

        elif SCENE_STATE == 11:
            #encore
            send('/sl/[0,3,6]/hit', 'trigger')

        elif SCENE_STATE == 12:
            attendre_debut(get, 6)
            send('/sl/[0,3]/hit', 'pause')
            attendre_debut(get, 6)
            send('/sl/6/hit', 'pause')

    else:
        boutons_fixes(subscene, send, get)

def laika(subscene, send, get):


    global SCENE_STATE, ACTIVE_LOOP

    if subscene == 'INIT':
        reset(subscene, send, get)
        print('Scene laika started')
        return

    elif subscene == 1: # CC1 = NEXT

        SCENE_STATE += 1
        print('Scene laika on subscene %s' % SCENE_STATE)


        # CONDUITE LINEAIRE
        if SCENE_STATE == 1:
            #rec mélo bourdon
            send('ardour', '/strip/mute', 3, 0)
            send('ardour', '/strip/mute', 8, 0)
            send('/sl/0/set', 'rec_thresh', 0)
            send('/sl/0/hit', 'record')

        elif SCENE_STATE == 2:
            send('/sl/0/hit', 'record')
            send('/sl/0/hit', 'overdub')

        elif SCENE_STATE == 3:
            send('/sl/0/hit', 'overdub')
            send('ardour', '/strip/mute', 3, 1)
            send('ardour', '/strip/mute', 6, 0)

        elif SCENE_STATE == 4:
            #rec kick et clar
            send('ardour', '/strip/mute', 8, 1)
            send('ardour', '/strip/mute', 11, 0)
            send('/sl/1/set', 'rec_thresh', 0.1)
            send('/sl/1/hit', 'record')
            send('/sl/6/set', 'rec_thresh', 0.02)
            send('/sl/6/hit', 'record')
            send('ardour', '/strip/mute', 1, 0)
            ACTIVE_LOOP = 1

        elif SCENE_STATE == 5:
            #fin rec kick + clar, défini comme synchro (sauf mélodica)
            send('/sl/1/hit', 'record')
            send('/sl/6/hit', 'record')
            ACTIVE_LOOP = 1
            send('ardour', '/strip/mute', 8, 0)
            send('ardour', '/strip/mute', 11, 1)
            send('ardour', '/strip/mute', 1, 1)
            send('/set', 'sync_source', 2)
            send('/set', 'overdub_quantized', 1)
            send('/sl/-1/set', 'sync', 1)
            send('/sl/0/set', 'sync', 0)
            send('/sl/-1/set', 'playback_sync', 1)
            send('/sl/0/set', 'playback_sync', 0)
            send('/sl/-1/set', 'quantize', 3)

        elif SCENE_STATE == 6:
            #rec bassA et bassB
            send('ardour', '/strip/mute', 2, 0)
            send('/sl/2/hit', 'record')
            attendre_debut(get, 1)
            send('/sl/2/hit', 'record')
            import time
            time.sleep(5)
            send('/sl/3/hit', 'record')
            attendre_debut(get, 1)
            send('/sl/2/hit', 'mute_on')
            send('/sl/6/hit', 'mute_on')
            send('/sl/3/hit', 'record')
            import time
            time.sleep(5)
            attendre_debut(get, 1)
            send('ardour', '/strip/mute', 2, 1)

        elif SCENE_STATE == 7:
            #rec violonA et violonB
            send('ardour', '/strip/mute', 4, 0)
            send('/sl/4/hit', 'record')
            attendre_debut(get, 1)
            send('/sl/2/hit', 'mute_off')
            send('/sl/3/hit', 'mute_on')
            send('/sl/0/hit', 'mute_on')
            import time
            time.sleep(5)
            send('/sl/4/hit', 'record')
            attendre_debut(get, 1)
            send('/sl/5/hit', 'record')
            send('/sl/[2,4]/hit', 'mute_on')
            send('/sl/3/hit', 'mute_off')
            import time
            time.sleep(5)
            send('/sl/5/hit', 'record')
            attendre_debut(get, 1)
            #repasse sur A tutti
            send('/sl/[2,4]/hit', 'mute_off')
            send('/sl/[3,5]/hit', 'mute_on')
            send('ardour', '/strip/mute', 4, 1)
            send('ardour', '/strip/mute', 5, 0)
            send('ardour', '/strip/mute', 7, 0)
            send('ardour', '/strip/mute', 3, 0) # à supprimer !!!!!!!!!!!!!!!

        elif SCENE_STATE == 8:
            #un tour ABBA depuis le A - oppa caval style
            attendre_debut(get, 1)
            send('/sl/[2,4]/hit', 'mute_on')
            send('/sl/[3,5]/hit', 'mute_off')
            import time
            time.sleep(7)
            attendre_debut(get, 1)
            import time
            time.sleep(7)
            attendre_debut(get, 1)
            send('/sl/[2,4]/hit', 'mute_off')
            send('/sl/[3,5]/hit', 'mute_on')
            import time
            time.sleep(7)
            attendre_debut(get, 1)
            send('/sl/[2,4]/hit', 'mute_off')
            send('/sl/[3,5]/hit', 'mute_on')

        elif SCENE_STATE == 9:
            #couplet chanté depuis le A
            #press = on va passer B, puis A ad lib
            attendre_debut(get, 1)
            send('/sl/[2,4]/hit', 'mute_on')
            send('/sl/[3,5]/hit', 'mute_off')
            import time
            time.sleep(1)
            attendre_debut(get, 1)
            send('/sl/[2,4]/hit', 'mute_off')
            send('/sl/[3,5]/hit', 'mute_on')

        elif SCENE_STATE == 10:
            #encore couplet chanté depuis le A
            #press = on va passer B, puis A ad lib
            attendre_debut(get, 1)
            send('/sl/[2,4]/hit', 'mute_on')
            send('/sl/[3,5]/hit', 'mute_off')
            import time
            time.sleep(1)
            attendre_debut(get, 1)
            send('/sl/[2,4]/hit', 'mute_off')
            send('/sl/[3,5]/hit', 'mute_on')

        elif SCENE_STATE == 11:
            #caval style. Press = on va passer au B du ABBA puis fin
            attendre_debut(get, 1)
            send('/sl/[2,4]/hit', 'mute_on')
            send('/sl/[3,5]/hit', 'mute_off')
            import time
            time.sleep(7)
            attendre_debut(get, 1)
            import time
            time.sleep(7)
            attendre_debut(get, 1)
            send('/sl/[2,4]/hit', 'mute_off')
            send('/sl/[3,5]/hit', 'mute_on')
            import time
            time.sleep(7)
            attendre_debut(get, 1)
            send('/sl/-1/hit', 'mute_on')

    else:
        boutons_fixes(subscene, send, get)

def bani(subscene, send, get):

    global SCENE_STATE, ACTIVE_LOOP

    if subscene == 'INIT':
        reset(subscene, send, get)
        print('Scene bani started')
        return

    elif subscene == 1: # CC1 = NEXT

        SCENE_STATE += 1
        print('Scene bani on subscene %s' % SCENE_STATE)


        # CONDUITE LINEAIRE
        if SCENE_STATE == 1:
            #rec kick et meloA
            send('ardour', '/strip/mute', 3, 0)
            send('ardour', '/strip/mute', 1, 0)
            send('ardour', '/strip/mute', 12, 0)
            send('/sl/[0,1]/set', 'rec_thresh', 0.02)
            send('/sl/[0,1]/hit', 'record')

        elif SCENE_STATE == 2:
            #fin record kick meloA, synchro kick, rec meloB
            send('/sl/[0,1]/hit', 'record')
            send('ardour', '/strip/mute', 1, 1)
            send('/set', 'sync_source', 1)
            send('/set', 'overdub_quantized', 1)
            send('/sl/-1/set', 'sync', 1)
            send('/sl/-1/set', 'playback_sync', 1)
            send('/sl/-1/set', 'quantize', 3)
            import time
            time.sleep(4)
            send('/sl/2/hit', 'record')
            attendre_debut(get, 0)
            send('/sl/1/hit', 'mute_on')
            import time
            time.sleep(4)
            send('/sl/2/hit', 'record')
            attendre_debut(get, 0)
            send('ardour', '/strip/mute', 3, 1)
            send('ardour', '/strip/mute', 12, 1)
            send('ardour', '/strip/mute', 8, 0)
            send('/sl/[1,2]/hit', 'mute')

        elif SCENE_STATE == 3:
            #rec bassA et bassB, puis repasse au A
            send('ardour', '/strip/mute', 2, 0)
            send('/sl/3/hit', 'record')
            attendre_debut(get, 0)
            import time
            time.sleep(4)
            send('/sl/[3,4]/hit', 'record')
            attendre_debut(get, 0)
            send('/sl/[1,3]/hit', 'mute_on')
            send('/sl/2/hit', 'mute_off')
            import time
            time.sleep(4)
            send('/sl/4/hit', 'record')
            attendre_debut(get, 0)
            send('/sl/[1,3]/hit', 'mute_off')
            send('/sl/[2,4]/hit', 'mute_on')
            send('ardour', '/strip/mute', 2, 1)
            send('ardour', '/strip/mute', 4, 0)

        elif SCENE_STATE == 4:
            #play violon ABBAB BBBB, puis A ad lib
            attendre_debut(get, 0)
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #1er B
            send('/sl/[1,2,3,4]/hit', 'mute')
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #2e B
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            # A
            send('/sl/[1,2,3,4]/hit', 'mute')
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            # B1
            send('/sl/[1,2,3,4]/hit', 'mute')
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #2
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #3
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #4
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #5
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            send('/sl/[1,2,3,4]/hit', 'mute')
            send('ardour', '/strip/mute', 3, 0) # à supprimer !!!!!!
            send('ardour', '/strip/mute', 7, 0)

        elif SCENE_STATE == 5:
            # couplet voix déclenche B, aussi pour 2x violon, puis A
            attendre_debut(get, 0)
            send('/sl/[1,2,3,4]/hit', 'mute')
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            send('/sl/[1,2,3,4]/hit', 'mute')

        elif SCENE_STATE == 6:
            # couplet voix déclenche B, 2x violon, puis ABBB, A ad lib
            attendre_debut(get, 0)
            send('/sl/[1,2,3,4]/hit', 'mute')
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            send('/sl/[1,2,3,4]/hit', 'mute')
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            send('/sl/[1,2,3,4]/hit', 'mute')
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            send('/sl/[1,2,3,4]/hit', 'mute')

        elif SCENE_STATE == 7:
            # déclenche ABBAB BBBB, puis mute
            attendre_debut(get, 0)
            send('/sl/[0,3]/hit', 'mute_on')
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #1er B
            send('/sl/[0,3]/hit', 'mute_off')
            send('/sl/[1,2,3,4]/hit', 'mute')
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #2e B
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            # A
            send('/sl/[1,2,3,4]/hit', 'mute')
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            # B1
            send('/sl/[1,2,3,4]/hit', 'mute')
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #2
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #3
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #4
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            #5
            import time
            time.sleep(4)
            attendre_debut(get, 0)
            send('/sl/-1/hit', 'mute_on')
            send('ardour', '/strip/mute', 4, 1)


    else:
        boutons_fixes(subscene, send, get)
