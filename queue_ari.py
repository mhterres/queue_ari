#!/usr/bin/env python
# -*- coding: utf-8 -*-

# queue_ari.py
# New queue app for Asterisk using ARI
#
# Marcelo H. Terres <mhterres@mundoopensource.com.br>
# 2016-10-07
#

import os
import ari
import sys
import time
import uuid
import logging
import requests
import threading

import config
import dbpgsql

import psycopg2
import psycopg2.extras

cfg=config.Config()

# logging errors
log = open(cfg.logfile, 'a')
sys.stderr = log

if cfg.debug==1:

	# DEBUG
	sys.stdout = log

def safe_hangup(channel,extension):
    """Safely hang up the specified channel"""
    db.updateData(queue_id,extension.split("/")[1])
    print "Call ended at %s\n" % time.strftime("%c")
    try:
        channel.hangup()
        print "Hung up {}".format(channel.json.get('name'))
    except requests.HTTPError as e:
        if e.response.status_code != requests.codes.not_found:
            raise e

def safe_bridge_destroy(bridge):
    """Safely destroy the specified bridge"""
    try:
        bridge.destroy()
    except requests.HTTPError as e:
        if e.response.status_code != requests.codes.not_found:
            raise e

def stasis_start_cb(channel_obj, ev):
    """Handler for StasisStart"""

    def playback_finished(playback, ev):
        """Callback when the playback have finished"""

        target_uri = playback.json.get('target_uri')
        channel_id = target_uri.replace('channel:', '')
        channel = client.channels.get(channelId=channel_id)

        channel.ring()

        exten='1000'
        extension='PJSIP/%s' % exten

        try:
            print "Dialing %s - Origin %s" % (extension,callerid)
            outgoing = client.channels.originate(endpoint=extension,
                                                 app='queue_ari',
                                                 appArgs='dialed',
																								 callerId=callerid)

        except requests.HTTPError:
            print "Whoops, pretty sure %s wasn't valid" % extension
            channel.hangup()
            return

        channel.on_event('StasisEnd', lambda *args: safe_hangup(outgoing,extension))
        outgoing.on_event('StasisEnd', lambda *args: safe_hangup(channel,extension))

        def outgoing_start_cb(channel_obj, ev):
            """StasisStart handler for our dialed channel"""

            print "{} answered; bridging with {}".format(outgoing.json.get('name'),
                                                         channel.json.get('name'))
				 
            channel.answer()

            bridge = client.bridges.create(type='mixing')
            bridge.addChannel(channel=[channel.id, outgoing.id])

            # Clean up the bridge when done
            channel.on_event('StasisEnd', lambda *args:
                             safe_bridge_destroy(bridge))
            outgoing.on_event('StasisEnd', lambda *args:
                             safe_bridge_destroy(bridge))
    
        outgoing.on_event('StasisStart', outgoing_start_cb)

    channel = channel_obj.get('channel')
    callerid = channel.json.get('caller')['number']

    # provide callerid (in case of receiving iax calls)
    if len(callerid)==0:
       callerid="Asterisk"

    channel_name = channel.json.get('name')
    args = ev.get('args')

    channel.answer()

    channel.on_event('StasisEnd', lambda *args: safe_hangup(outgoing,""))

    chanType=channel.json.get('name').split('-')[0] 	# get CHANTYPE/EXTEN
    #chanType=channel.json.get('name').split('/')[0] 	# get CHANTYPE

		# Normally you will avoid process of a call when channel is PJSIP/SIP
		# I did this because I want to process only external calls
		# Also, I want to avoid that the originate call be processed too (loop)

	  #if chanType != "PJSIP":					# avoid process when channel type is PJSIP

    # I'm using PJSIP/2000 for my tests, but you should consider using ChanType != "PJSIP"
    if chanType == "PJSIP/2000":			# process when channel is PJSIP/2000

        playback_id = str(uuid.uuid4())
        playback = channel.playWithId(playbackId=playback_id,media='sound:poc/support_team')
        playback.on_event('PlaybackFinished', playback_finished)

print "queue_ari started at %s" % time.strftime("%c")

print "Asterisk ARI - connecting"
client = ari.connect('http://localhost:8088', cfg.ari_user, cfg.ari_pwd)
client.on_channel_event('StasisStart', stasis_start_cb)

print "Database - connecting"

if cfg.db_type=='pgsql':

	db=dbpgsql.DBPgsql(cfg)

print "Waiting for calls..."

client.run(apps='queue_ari')




