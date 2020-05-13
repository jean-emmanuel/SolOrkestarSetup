from server import Server
import scenes
import midi

s = Server(
    port = 5555,
    target = 9951,
    default_scene = '1',
    midiroute = midi.route,
    scenes = {
        '1': scenes.klezmer,
        #'2': scenes.etc
    }
)

s.start()
