#!/usr/bin/env python
# -*- coding: utf-8 -*-

# stats.py
# stats class
#
# Marcelo Hartmann Terres <mhterres@mundoopensource.com.br>
# 2016/10/08
#


from time import gmtime, strftime

class Stats:

	def __init__(self,queues):

		qstats={}

		for q in queues.queues:

			qstats[q]=dict( {"total": 0, "answered": 0, "abandoned": 0, "holdtime": 0} )

		mstats={}

		for q in queues.queues_members:

			for m in queues.queues_members[q]:

				mstats[m['interface']]=dict ( {"lastcall": strftime("%Y-%m-%d %H:%M:%S", gmtime()) } )
				mstats[m['interface']][q]=0

		self.queuestats=qstats
		self.memberstats=mstats

