#!/usr/bin/env python
# -*- coding: utf-8 -*-

# queues.py
# queues class
#
# Marcelo Hartmann Terres <mhterres@mundoopensource.com.br>
# 2016/10/08
#


class Queues:

	def __init__(self,cfg,db):

		q=db.getQueues()
		self.queues=q[0]
		self.queues_info=q[1]

		# Get queue members
		qm = {}

		for q in self.queues:

			qm[q]=db.getQueueMembers(self,q,'all')

		self.queues_members=qm

		# Get queues rules
		self.queues_rules=db.getQueueRules()
