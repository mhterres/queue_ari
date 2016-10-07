#!/usr/bin/env python
# -*- coding: utf-8 -*-

# config.py
# configuration class
#
# Marcelo Hartmann Terres <mhterres@mundoopensource.com.br>
# 2016/10/07
#


import os
import sys
import ConfigParser

import dbpgsql

class Config:

	def __init__(self):

		configuration = ConfigParser.RawConfigParser()

		configuration = ConfigParser.RawConfigParser()
		configuration.read('./conf/queue_ari.conf')

		self.debug=configuration.get('general','debug')
		self.logfile=configuration.get('general','logfile')
		self.strategy=configuration.get('general','strategy')
		self.queue_timeout=configuration.get('general','queue_timeout')
		self.extension_ringtime=configuration.get('general','extension_ringtime')
		self.moh=configuration.get('general','moh')

		# ari
		self.ari_user=configuration.get('ari','user')
		self.ari_pwd=configuration.get('ari','password')

		# db
		self.db_type=configuration.get('db','type')
		self.db_host=configuration.get('db','host')
		self.db_name=configuration.get('db','name')
		self.db_user=configuration.get('db','user')
		self.db_pwd=configuration.get('db','password')

		# Processing realtime queues

		if self.db_type=='pgsql':

			db=dbpgsql.DBPgsql(self)

		q=db.getQueues()
		self.queues=q[0]
		self.queues_info=q[1]

		# Get queue members
		qm = {}

		for q in self.queues:

			qm[q]=db.getQueueMembers(self,q,'all')

		self.queue_members=qm

		# Get queues rules

		self.queue_rules=db.getQueueRules()
