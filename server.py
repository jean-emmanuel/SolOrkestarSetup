import liblo
import rtmidi
import scenes
import time

from rtmidi.midiconstants import *
from signal import signal, SIGINT, SIGTERM


MIDI_TO_OSC = {
    NOTE_ON: 'note',
    NOTE_OFF: 'note',
    CONTROL_CHANGE: 'control',
    PROGRAM_CHANGE: 'program',
}

class Server(object):

    def __init__(self, port, target, scenes, default_scene=None, midiroute={}):

        self.target = target
        self.scenes = scenes


        self.active_scene = default_scene

        self.server = liblo.Server(5555)
        self.server.add_method(None, None, self.route_osc)


        self.midiroute = midiroute
        if self.midiroute:
            self.midi = rtmidi.MidiIn(rtmidi.API_UNIX_JACK, 'NicoOsc')
            self.midi.open_virtual_port('in')
            self.midi.set_callback(self.receive_midi)

        self.running = False

        signal(SIGINT, self.stop)
        signal(SIGTERM, self.stop)

    def route_osc(self, path, args):

        if not type(args) is list:
            args = [args]

        if path == '/scene':

            n = str(args[0])
            if n in self.scenes:
                print('Scene changed to: %s' % n)
                self.active_scene = n
                self.scenes[self.active_scene](0, self.send)
            else:
                print('Unknown scene: %s' % n)


        elif path == '/subscene':

            if self.active_scene is not None:

                n = args[0]
                print('Subscene called in scene %s: %s' % (self.active_scene, n))
                self.scenes[self.active_scene](n, self.send)

            else:

                print('No active scene')


        else:
            print('Unknown command %s' % path)

    def send(self, *args):

        self.server.send(self.target, *args)
        print(self.target, *args)


    def receive_midi(self, event, data):

        midi = {}

        message, deltatime = event
        mtype = message[0] & 0xF0

        if mtype in MIDI_TO_OSC:


            status = message[0]
            channel = (status & 0xF) + 1

            if mtype == NOTE_OFF:
                message[2] = 0

            type = MIDI_TO_OSC[mtype]
            channel = channel
            control = message[1]
            value = message[2]

            def receive(path, *args):
                self.route_osc(path, *args)

            self.midiroute(type, channel, control, value, receive)


    def start(self):

        self.running = True

        while self.running:

            self.server.recv(0)
            time.sleep(0.001)

        self.server.free()

    def stop(self, *args):

        self.running = False
