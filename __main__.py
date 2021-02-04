from server import Server
import scenes
import midi

s = Server(
    port = 5555,
    target = 9951,
    #default_scene = '1',
    midiroute = midi.route,
    scenes = {
        '1': scenes.haiduk,
        '2': scenes.capra,
        '3': scenes.kamav,
        '4': scenes.laika,
        '5': scenes.bani,
        #'2': scenes.etc
    }
)

s.start()
