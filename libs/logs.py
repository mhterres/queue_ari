#!/usr/bin/env python
# -*- coding: utf-8 -*-

# logs.py
# app and queue logs class
#
# Marcelo Hartmann Terres <mhterres@mundoopensource.com.br>
# 2016/10/11
#

import csv
import sys
import logging
import json_log_formatter

class Logs:

	def __init__(self,cfg,db):

		# queue log
		if cfg.queue_logtype=='json':

			formatter = json_log_formatter.JSONFormatter()

			json_handler = logging.FileHandler(filename=cfg.queue_logfile)
			json_handler.setFormatter(formatter)

			qlogger = logging.getLogger('my_json')
			qlogger.addHandler(json_handler)
			qlogger.setLevel(logging.INFO)

		elif cfg.queue_logtype=='csv':

			qlogger = open(cfg.queue_logfile,'a',0)
		else:

			print "Logging configuration error. Exit."
			sys.exit(1)

		# app log
		alogger = open(cfg.app_logfile,'a',0)

		self.logtype=cfg.queue_logtype
		self.alog=alogger
		self.qlog=qlogger
		self.db=db

	def qlog(self,data):

		if self.logtype=="csv":

			csv.writer(self.qlog).writerow(data)
		else:

			self.qlog.info('', extra={"calldate": data[0], "uniqueid": data[1], "queues_id": data[2], "agent": data[3], "event": data[4], "data1": data[5], "data2": data[6], "data3": data[7], "data4": data[8], "data5": data[9]})

		self.db.insertQLog(data)

		
