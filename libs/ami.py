#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ami.py
# AMI class
#
# Marcelo Hartmann Terres <mhterres@mundoopensource.com.br>
# 2016/10/13
#

from asterisk import manager

class AMI:

	def __init__(self,cfg):

		ami=manager.Manager()
		ami.connect(cfg.ami_host)
		ami.login(cfg.ami_user,cfg.ami_pwd)

		self.ami=ami
		self.cfg=cfg

	def sendXMPPMessage(self,_to,_body):

		dAction={"Action": "MessageSend", "To": "%s" % _to, "From": "xmpp:%s" % self.cfg.xmpp_resource, "Body": "%s" % _body}
		response=self.ami.send_action(dAction)
		return response
