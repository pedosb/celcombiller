#!/usr/bin/env python
"""
celcombiller AGI, inform maximum call duration
"""
import sys
sys.stderr = open('/tmp/oi', 'w')
# pylint: disable=C0103
import asterisk.agi
from models import session, User

agi = asterisk.agi.AGI()

balance = session.query(User.balance).filter_by(clid=agi.env['agi_callerid']).one()

agi.set_variable("CEL_MAX_DUR", balance)
