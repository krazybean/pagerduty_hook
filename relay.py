import os
import sys
import requests
import time
import json

class Relay:

    def __init__(self):
        """
        tests environment for from/to endpoints
        """
        try:
            self.external_relay = os.environ['external_hook']
            self.external_dest = os.environ['destination']
            self.interval = 15
        except KeyError:
            sys.exit("External hook not set: export external_hook='endpoint'")
            sys.exit("External hook not set: export destination='endpoint'")

    def heartbeat(self):
        """
        grabs from primary relay
        """
        r = requests.get(self.external_relay)
        return r.json()

    def repost(self, data):
        """
        sends to destination
        """
        headers = {'Content-Type': 'application/json'}
        r = requests.post(self.external_dest,
                          data=json.dumps(data),
                          headers=headers)

    def initiate(self):
        """ Looper """
        try:
            while True:
                dataset = self.heartbeat()
                if dataset.has_key('Queue'):
                    self.process_display()
                    self.retext("Nothing new")
                else:
                    self.retext("New event, posting...=> [{0}]".format(self.external_dest))
                    self.repost(dataset)
        except KeyboardInterrupt:
            print " <= [Cancelled]"

    def process_display(self, char=None):
        """ More dots """
        for x in xrange(self.interval):
            print("Waiting {0}s".format(self.interval) + "." * x)
            sys.stdout.write("\033[F")
            time.sleep(1)

    def retext(self, text=None):
        """ retexting the sameline """
        print("[{0}]".format(text))

if __name__ == '__main__':
    relay = Relay()
    print relay.initiate()
