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

class Config:

	def __init__(self):

		configuration = ConfigParser.RawConfigParser()

		configuration = ConfigParser.RawConfigParser()
		configuration.read('./conf/queue_ari.conf')

		self.strategy=configuration.get('general','strategy')
		self.queue_timeout=configuration.get('general','queue_timeout')
		self.extension_ringtime=configuration.get('general','extension_ringtime')
		self.moh=configuration.get('general','moh')
		self.chantype=configuration.get('general','chantype')

		# logs
		self.debug=configuration.get('logs','debug')
		self.app_logfile=configuration.get('logs','app_logfile')
		self.app_errlogfile=configuration.get('logs','app_errlogfile')
		self.queue_logfile=configuration.get('logs','queue_logfile')
		self.queue_logtype=configuration.get('logs','queue_logtype')
	
		# tools
		self.tools_xmpp=configuration.get('tools','xmpp')
		self.tools_statsd=configuration.get('tools','statsd')

		# ami
		self.ami_host=configuration.get('ami','host')
		self.ami_user=configuration.get('ami','user')
		self.ami_pwd=configuration.get('ami','password')

		# ari
		self.ari_host=configuration.get('ari','host')
		self.ari_user=configuration.get('ari','user')
		self.ari_pwd=configuration.get('ari','password')

		# db
		self.db_type=configuration.get('db','type')
		self.db_host=configuration.get('db','host')
		self.db_name=configuration.get('db','name')
		self.db_user=configuration.get('db','user')
		self.db_pwd=configuration.get('db','password')

		# xmpp
		self.xmpp_resource=configuration.get('xmpp','resource')
		self.xmpp_name=configuration.get('xmpp','name')
		self.xmpp_send=configuration.get('xmpp','send')
		
