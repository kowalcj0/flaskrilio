# -*- coding: utf-8 -*-
from twilio_connector import TwilioConnector

conn = TwilioConnector()
conn.load_config(twilio_config="call-connect-eu.cfg")
conn.connect_to_twilio()
conn.print_config()
call = conn.make_a_call(from_no="+441353210177", to_no="+447402028595")

print conn.get_call_details(call)
