#!/usr/bin/env python

import json
import sys
import websocket
import threading
import Queue
import requests


class ARIInterface(object):
    def __init__(self, server_addr, username, password):
        self._req_base = "http://%s:8088/ari/" % server_addr
        self._username = username
        self._password = password

    def send_xmpp_message(self,_from,_to,_message):
        req_str = self._req_base+"endpoints/sendMessage?to=%s&from=%s&body=%s" % (_to,_from,_message)
        print req_str
        self._send_put_request(req_str)

    def answer_call(self, channel_id):
        req_str = self._req_base+"channels/%s/answer" % channel_id
        self._send_post_request(req_str)

    def play_sound(self, channel_id, sound_name):
        req_str = self._req_base+("channels/%s/play?media=sound:%s" % (channel_id, sound_name))
        self._send_post_request(req_str)

    def _send_post_request(self, req_str):
        r = requests.post(req_str, auth=(self._username, self._password))

    def _send_put_request(self, req_str):
        r = requests.put(req_str, auth=(self._username, self._password))




class ARIApp(object):
    def __init__(self, server_addr):
        app_name = 'test_ari'
        username = 'asterisk'
        password = 'nsw88HpnBa0s3o8U'
        url = "ws://%s:8088/ari/events?app=%s&api_key=%s:%s" % (server_addr, app_name, username, password)
        ari = ARIInterface(server_addr, username, password)
        ws = websocket.create_connection(url)

        print "Ari app started"
        ari.send_xmpp_message("asterisk@jabber.mundoopensource.com.br","mhterres@jabber.mundoopensource.com.br","Call")

        try:
            for event_str in iter(lambda: ws.recv(), None):
                event_json = json.loads(event_str)

                json.dump(event_json, sys.stdout, indent=2, sort_keys=True,
                          separators=(',', ': '))
                print("\n\nWebsocket event***************************************************\n")

                if event_json['type'] == 'StasisStart':
                    ari.answer_call(event_json['channel']['id'])
                    ari.play_sound(event_json['channel']['id'], 'tt-monkeys')
        except websocket.WebSocketConnectionClosedException:
            print("Websocket connection closed")
        except KeyboardInterrupt:
            print("Keyboard interrupt")
        finally:
            if ws:
                ws.close()


if __name__ == "__main__":
    app = ARIApp('localhost')
