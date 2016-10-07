#!/usr/bin/env python
# -*- coding: utf-8 -*-

# dbpgsql.py
# DB Postgres class
# see db/queue_ari.sql for db schema
#
# Marcelo Hartmann Terres <mhterres@gmail.com>
# 2016/10/07
#

import logging
import psycopg2
import psycopg2.extras

class DBPgsql:

	def __init__(self,cfg):

		self.dsn = 'dbname=%s host=%s user=%s password=%s' % (cfg.db_name,cfg.db_host,cfg.db_user,cfg.db_pwd)

		self.conn = psycopg2.connect(self.dsn)
		self.cfg=cfg

	def getQueues(self):

		curs = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

		try:

			sql="SELECT * FROM queues ORDER BY name;"

			curs.execute(sql)
		except:

			logging.error("Error searching database - SQL %s" % sql)

			returnmsg ="Error searching database."
			sys.exit()
			conn.commit()

		else:

			queues=[]
			queues_info={}

			if curs.rowcount:
			
				rec=curs.fetchone()

				while rec is not None:

					queues.append(rec['name'])

					queues_info[rec['name']] = dict (	{'id': rec['id'], \
																						'name': rec['name'],\
																					 	'musiconhold':	rec['musiconhold'],\
																						'announce':	rec['announce'],\
																						'context': rec['context'],\
																						'timeout': rec['timeout'],\
																						'ringinuse': rec['ringinuse'],\
																						'setinterfacevar': rec['setinterfacevar'],\
																						'setqueuevar': rec['setqueuevar'],\
																						'setqueueentryvar': rec['setqueueentryvar'],\
																						'monitor_format': rec['monitor_format'],\
																						'membermacro': rec['membermacro'],\
																						'membergosub': rec['membergosub'],\
																						'queue_youarenext': rec['queue_youarenext'],\
																						'queue_thereare': rec['queue_thereare'],\
																						'queue_callswaiting': rec['queue_callswaiting'],\
																						'queue_quantity1': rec['queue_quantity1'],\
																						'queue_quantity2': rec['queue_quantity2'],\
																						'queue_holdtime': rec['queue_holdtime'],\
																						'queue_minutes': rec['queue_minutes'],\
																						'queue_minute': rec['queue_minute'],\
																						'queue_seconds': rec['queue_seconds'],\
																						'queue_thankyou': rec['queue_thankyou'],\
																						'queue_callerannounce': rec['queue_callerannounce'],\
																						'queue_reporthold': rec['queue_reporthold'],\
																						'announce_frequency': rec['announce_frequency'],\
																						'announce_to_first_user': rec['announce_to_first_user'],\
																						'min_announce_frequency': rec['min_announce_frequency'],\
																						'announce_round_seconds': rec['announce_round_seconds'],\
																						'announce_holdtime': rec['announce_holdtime'],\
																						'announce_position': rec['announce_position'],\
																						'announce_position_limit': rec['announce_position_limit'],\
																						'periodic_announce': rec['periodic_announce'],\
																						'periodic_announce_frequency': rec['periodic_announce_frequency'],\
																						'relative_periodic_announce': rec['relative_periodic_announce'],\
																						'random_periodic_announce': rec['random_periodic_announce'],\
																						'retry': rec['retry'],\
																						'wrapuptime': rec['wrapuptime'],\
																						'penaltymemberslimit': rec['penaltymemberslimit'],\
																						'autofill': rec['autofill'],\
																						'monitor_type': rec['monitor_type'],\
																						'autopause': rec['autopause'],\
																						'autopausedelay': rec['autopausedelay'],\
																						'autopausebusy': rec['autopausebusy'],\
																						'autopauseunavail': rec['autopauseunavail'],\
																						'maxlen': rec['maxlen'],\
																						'servicelevel': rec['servicelevel'],\
																						'strategy': rec['strategy'],\
																						'joinempty': rec['joinempty'],\
																						'leavewhenempty': rec['leavewhenempty'],\
																						'reportholdtime': rec['reportholdtime'],\
																						'memberdelay': rec['memberdelay'],\
																						'weight': rec['weight'],\
																						'timeoutrestart': rec['timeoutrestart'],\
																						'defaultrule': rec['defaultrule'],\
																						'timeoutpriority': rec['timeoutpriority'] } )

					rec=curs.fetchone()

			curs.close()

		return (queues,queues_info)

	def getQueueMembers(self,cfg,queue_name,member_type):

		# member_types:
		#
		# fixed: fixed members
		# dynamic: dynamic members
		# all: all members

		curs = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

		try:

			if member_type=="all":

				sql="SELECT * FROM queue_members WHERE queues_id=%s ORDER BY interface;" % cfg.queues_info[queue_name]['id']
			else:

				sql="SELECT * FROM queue_members WHERE queues_id=%s AND type='%s' ORDER BY interface;" % (cfg.queues_info[queue_name]['id'],member_type)

			curs.execute(sql)
		except:

			logging.error("Error searching database - SQL %s" % sql)

			returnmsg ="Error searching database."
			sys.exit()
			conn.commit()

		else:

			members_info=[]

			if curs.rowcount:
			
				rec=curs.fetchone()

				while rec is not None:

					members_info.append( dict (	{'type': rec['type'], \
																			'interface': rec['interface'],\
																		 	'membername':	rec['membername'],\
																			'state_interface':	rec['state_interface'],\
																			'penalty': rec['penalty'],\
																			'paused': rec['paused'],\
																			'uniqueid': rec['uniqueid'] } ) )

					rec=curs.fetchone()

			curs.close()

		return members_info

	def getQueueRules(self):

		curs = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

		try:

			sql="SELECT * FROM queue_rules;"

			curs.execute(sql)
		except:

			logging.error("Error searching database - SQL %s" % sql)

			returnmsg ="Error searching database."
			sys.exit()
			conn.commit()

		else:

			rules=[]

			if curs.rowcount:
			
				rec=curs.fetchone()

				while rec is not None:

					rules.append( dict (	{'rule_name': rec['rule_name'], \
																'time': rec['time'],\
															 	'min_penalty':	rec['min_penalty'],\
															 	'max_penalty':	rec['max_penalty'] } ) )

					rec=curs.fetchone()

			curs.close()

		return rules


