import liblo
import rtmidi
import scenes
import time

from rtmidi.midiconstants import *
from signal import signal, SIGINT, SIGTERM
from uuid import uuid1 as uuid
from utils import KillableThread as Thread

MIDI_TO_OSC = {
    NOTE_ON: 'note',
    NOTE_OFF: 'note',
    CONTROL_CHANGE: 'control',
    PROGRAM_CHANGE: 'program',
}

SL_QUERY_RETRY = 0.02
SL_QUERY_TIMEOUT = 1





class Server(object):

    def __init__(self, port, target, scenes, default_scene=None, midiroute={}, oscroute={}):

        self.target = target
        self.scenes = scenes


        self.active_scene = default_scene
        self.subscenes_threads = []

        self.port = port
        self.server = liblo.Server(self.port)
        self.server.add_method(None, None, self.route_osc)

        self.pending_queries = {}

        self.oscroute = oscroute
        self.midiroute = midiroute
        if self.midiroute:
            self.midi = rtmidi.MidiIn(rtmidi.API_LINUX_ALSA, 'Conduite')
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
                # self.scenes[self.active_scene](0, self.send, self.get)
            else:
                print('Unknown scene: %s' % n)


        elif path == '/subscene':

            if self.active_scene is not None:

                n = args[0]
                print('Subscene called in scene %s: %s' % (self.active_scene, n))

                t = Thread(target=self.scenes[self.active_scene], args=[n, self.send, self.get])
                t.start()

                self.subscenes_threads.append(t)


            else:

                print('No active scene')


        elif path == '/stop':

            for t in self.subscenes_threads:
                t.kill()

            self.subscenes_threads = []

            print('Subscenes stopped')



        elif '/reply/' in path:

            query_id = path.split('/')[-1]
            if query_id in self.pending_queries:
                self.pending_queries[query_id]['value'] = args[1:]

        elif '/pedalBoard' in path:

            if self.oscroute:

                self.oscroute(path, args, self.send, self.get)

        else:

            print('Unknown command %s' % path)

    def send(self, target, *args, PRINT=True):

        args = list(args)
        if target == 'server':
            self.route_osc(args[0], args[1:])
            return
        elif target == 'ardour':
            target = 3819
        elif type(target) != int:
            args.insert(0, target)
            target = self.target

        self.server.send(target, *args)

        if PRINT:
            print('SEND:', target, *args)


    def get(self, path, property):

        query_id = str(uuid())[:8]
        query_time = time.time()
        query = {
            'start_date': query_time,
            'last_try': 0,
            'path': path,
            'property': property,
            'value': None
        }

        self.pending_queries[query_id] = query

        while query['value'] is None:

            # self.process() # replaced with sleep (assuming get is always called from a threaded subscene)
            time.sleep(0.001)
            now = time.time()

            if now - query['start_date'] >= SL_QUERY_TIMEOUT:
                print('Sooperlooper query TIMEOUT on get(%s, %s)' % (path, property))
                del self.pending_queries[query_id]
                return None

        del self.pending_queries[query_id]

        return query['value'][1] if len(query['value']) > 1 else query['value'][0]


    def send_queries(self):

        now = time.time()
        for query_id in self.pending_queries:
            query = self.pending_queries[query_id]
            if now - query['last_try'] >= SL_QUERY_RETRY:
                self.send(query['path'], query['property'], 'osc.udp://127.0.0.1:%i' % self.port, '/reply/%s' % query_id, PRINT=False)
                query['last_try'] = now



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
            value = message[2] if len(message) > 2 else None

            self.midiroute(type, channel, control, value, self.send, self.get)


    def start(self):

        self.running = True

        while self.running:

            self.process()

        self.server.free()

    def process(self):

        self.server.recv(0)
        self.send_queries()
        time.sleep(0.001)

    def stop(self, *args):

        self.running = False
