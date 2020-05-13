def route(type, channel, control, value, receive):
    """
        type: 'note', 'program' ou 'control'
        channel: 1 à 15
        data: [x, y] où x est le numéro du contrôle et y la valeur

        receive: function pour recevoir l'osc
    """
    print(type, channel, control, value)
    if type == 'control' and control == 101 and value == 127:
        receive('/scene', 1)
        pass
