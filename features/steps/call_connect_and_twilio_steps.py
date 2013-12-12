# -*- coding: utf-8 -*-
from behave import *
from time import sleep
from handlers.twilio_handler import TwilioHandler


@given('I retrieved a number to call for "{inbound_twilio_number}"')
def step_impl(context, inbound_twilio_number):
    """
    Get a new Caller ID
    Get a new number to call to redirect to given number
    """
    context.redirect_to_no = inbound_twilio_number
    context.caller_id = context.cch.get_new_caller_id()
    context.redir_resp = context.cch.get_redirect_to(
        caller_id=context.caller_id,
        number=context.redirect_to_no)
    context.log.debug("redirect_to response for number: %s \n%s"
                      % (context.redirect_to_no, context.redir_resp))
    context.caller = TwilioHandler()
    context.caller.load_config(twilio_config="call-connect-eu.cfg")
    context.caller.connect_to_twilio()
    context.caller.print_config()


@when('I call this number to call from "{outbound_twilio_number}"')
def step_impl(context, outbound_twilio_number):
    context.from_no = outbound_twilio_number
    context.call = context.caller.call_and_run_twiml(
        from_no=context.from_no,
        to_no=context.redirect_to_no,
        twiml_url="https://dl.dropboxusercontent.com/u/14336410/twilio/test-load.xml")


@when('I wait "{N}" seconds for the call to finish')
def step_impl(context, N):
    context.log.debug("Waiting %s seconds for call to finish..." % N)
    sleep(float(N))


@then('I should be redirected to "{inbound_twilio_number}"')
def step_impl(context, inbound_twilio_number):
    call_stats = context.caller.get_call_stats(context.call.sid)
    context.call_stats = call_stats
    context.log.debug("Retrieved call stats: %s" % call_stats)
    assert call_stats.status == "completed"
    assert call_stats.duration >= 10
    assert call_stats.from_formatted == context.from_no, \
        "Call was made from: %s and not from: %s" \
        % (call_stats.from_formatted, context, from_no)
    assert call_stats.to_formatted == context.redirect_to_no, \
        "Call was made to: %s and not to: %s" \
        % (call_stats.to_formatted, context.redirect_to_no)


@then("I should be able to download the call recording")
def step_impl(context):
    context.log.debug("List of available call recordings for call_sid: %s : %s"
                     % (context.call.sid,
                        context.call.recordings.list(call=context.call.sid)))
    """TO-DO
    recordings can be downloaded only for incoming calls.
    here we're handling outgoing call. We'd have to have a HTTP server (maybe)
    flask, that would handle incoming calls and thanks to this we'd be able
    to download the recording
    like using wget
    wget --user=AC1748a660591e427ac079282e74d50ff0 \
        --password=03588872f611332b772058c3f60cb607 \
        https://api.twilio.com/2010-04-01/Accounts/AC1748a660591e427ac079282e74d50ff0/Recordings/RE2aee6402d1cfd392b45f30ed3ac202bc.mp3
    """
