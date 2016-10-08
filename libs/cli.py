#!/usr/bin/env python
# -*- coding: utf-8 -*-

# cli.py
# Command Line Interface
#
# Marcelo Hartmann Terres <mhterres@mundoopensource.com.br>
# 2016/10/08
#

import cmd
import config
import dbpgsql

class CLI(cmd.Cmd):

	cfg=config.Config()

	if cfg.db_type=='pgsql':

		db=dbpgsql.DBPgsql(cfg)

	queueCmds = ['reload','reset','set','show']
	memberCmds = ['add','remove','show','pause','unpause']

	intro = 'Welcome to the queue_ari shell.   Type help or ? to list commands.\n'
	prompt = '(queue_ari) '

	def do_queue(self, person):
		"Queue informations and configurations"
		print "queue command"
    
	def complete_queue(self, text, line, begidx, endidx):
		if not text:

			completions = self.queueCmds[:]
		else:

			completions = [ f
											for f in self.queueCmds
											if f.startswith(text)
											]
		return completions

	def do_member(self, person):
		"Queue member informations and configurations"
		print "member command"
    
	def complete_member(self, text, line, begidx, endidx):
		if not text:

			completions = self.memberCmds[:]
		else:

			completions = [ f
											for f in self.memberCmds
											if f.startswith(text)
											]
		return completions

