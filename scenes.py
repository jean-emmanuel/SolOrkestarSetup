n = 0

def klezmer(subscene, send):

    global n

    if subscene == 'next':
        n += 1
        subscene = n


    if subscene == 0:
        # lancé automatiquement au chargement de la scene
        n = 0
        pass


    if subscene == 1:
        n = n + 1
        print(n)
        send('/sl/0/hit', 'pause')


    elif subscene == 2:

        send('/sl/0/hit', 'record')

    elif subscene == 3:

        send('/sl/0/hit', 'record')
        send('/set', 'sync_source', 1)
        send('/sl/#/set', 'sync', 1)

    elif subscene == 4:
        send('/sl/0/set', 'wet', 0.5)
        send('/sl/1/hit', 'record')

    elif subscene == 5:
        send('/set', 'sync_source', 1)
