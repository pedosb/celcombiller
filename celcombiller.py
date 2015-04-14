#!/usr/bin/env python
"""
celcombiller AGI:
    * Consult the user balance and authorize a call
    * Save the call CDRs
    * Update the user balance
"""
# pylint: disable=C0103
from datetime import datetime
import asterisk.agi
from asterisk.agi import AGIAppError
from models import session, User, CDR

agi = asterisk.agi.AGI()

from_user = session.query(User).filter_by(
    clid=agi.env['agi_callerid']).one()
to_user = session.query(User).filter_by(
    clid=agi.env['agi_extension']).one()

try:
    agi.appexec('DIAL', 'SIP/%s,40,S(%d)' % (to_user.clid, from_user.balance))
except AGIAppError:
    pass

if agi.get_variable('DIALSTATUS') == 'ANSWER':
    # Time from answer to hangup
    billsec = int(agi.get_variable('CDR(billsec)'))
    # Time the user answered
    answer = datetime.fromtimestamp(float(agi.get_variable('CDR(answer,u)')))
    # Create a new CDR record
    cdr = CDR(from_user=from_user, to_user=to_user,
              billsec=billsec, answer=answer)
    # Update user balance
    from_user.balance -= billsec

    session.commit()
