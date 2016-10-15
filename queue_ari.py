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
import cmd
import sys
import json
import time
import uuid
import requests

sys.path.insert(0, './libs')

import config
import dbpgsql
import queues
import statsd
import ami
import cli
import logs

cfg=config.Config()

# Error Logging
errorlog = open(cfg.app_errlogfile, 'a')
#sys.stderr = errorlog

if cfg.debug==1:

	# DEBUG
	sys.stdout = errorlog

def safe_hangup(channel,extension):
    """Safely hang up the specified channel"""
    print "Hangup Channel"

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
    extension='%s/%s' % (cfg.chantype,exten)

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

  # Validate args
  args = ev.get('args')

  if not args:
    print "Error: Queue is not informed!"
    logs.alog.write("Error: Queue is not informed!\n")

    channel = channel_obj.get('channel')

    channel.hangup()
   
    return

  if not db.validQueue(args[0]):

    print "Error: Queue %s doesn't exist." % args[0]
    logs.alog.write("Error: Queue %s doesn't exist.\n" % args[0])

    channel = channel_obj.get('channel')

    channel.hangup()
    
    return 

  #logs.qlog(

  # provide callerid (in case of receiving iax calls)
  if len(callerid)==0:
     callerid="Asterisk"

  channel_name = channel.json.get('name')

  channel.answer()

  channel.on_event('StasisEnd', lambda *args: safe_hangup(outgoing,""))

  chanType=channel.json.get('name').split('-')[0] 	# get CHANTYPE/EXTEN
  #chanType=channel.json.get('name').split('/')[0] 	# get CHANTYPE

  exten="1000"
  #exten=getDialExten(args[0])
  dstJID=db.getJID(exten)

  if dstJID !="":

    print "XMPP"
    ami.sendXMPPMessage("xmpp:%s" % dstJID,"Call from %s" %callerid)

  if chanType == "PJSIP/2000":			# process when channel is PJSIP/2000

    playback_id = str(uuid.uuid4())
    playback = channel.playWithId(playbackId=playback_id,media='sound:poc/support_team')
    playback.on_event('PlaybackFinished', playback_finished)

if len(sys.argv)>1 and sys.argv[1]=='-c':

 cmd=cli.CLI()
 cmd.cmdloop()

print "queue_ari started at %s" % time.strftime("%c")

print "Asterisk ARI - connecting"
client = ari.connect('http://%s:8088' % cfg.ari_host, cfg.ari_user, cfg.ari_pwd)
client.on_channel_event('StasisStart', stasis_start_cb)

print "Database - connecting"
if cfg.db_type=='pgsql':

	db=dbpgsql.DBPgsql(cfg)

print "Processing queues configurations"
queues=queues.Queues(cfg,db)

print "Creating statistics"
statsd=statsd.StatsD(queues)

print "Connecting AMI"
ami=ami.AMI(cfg)

print "Configuring log files"
logs=logs.Logs(cfg,db)

print "Waiting for calls..."
client.run(apps='queue_ari')




