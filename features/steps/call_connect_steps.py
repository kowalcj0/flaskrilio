# -*- coding: utf-8 -*-
import logging
from behave import *
from time import sleep
from call_connect_handler import CallConnectHandler
from make_call import Caller
import json
import urllib2


@given('a CallConnect service')
def step_impl(context):
    """Create a new call connect handler and add it to the context"""
    context.cch = CallConnectHandler("http://callconnect.poc.hibulabs.co.uk")


@when('I ask for a new Caller ID')
def step_impl(context):
    context.caller_id = context.cch.get_new_caller_id()
    context.log.debug("Received new Caller ID: %s" % context.caller_id)


@then('I should retrieve a Caller ID')
def step_impl(context):
    assert context.caller_id is not None


@then("I should see Caller ID in the response")
def step_impl(context):
    context.log.debug("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA %s" % context.page.data)
    assert context.caller_id in context.page.data, \
        "Page data: %s" % context.page.data


@given('I\'m a new user')
def step_impl(context):
    context.cch = CallConnectHandler("http://callconnect.poc.hibulabs.co.uk")
    context.caller_id = context.cch.get_new_caller_id()


@when('I ask for a new number to call for a "{redirect_to_no}"')
def step_impl(context, redirect_to_no):
    context.redirect_to_no = redirect_to_no
    context.redir_resp = context.cch.get_redirect_to(
        caller_id=context.caller_id,
        number=context.redirect_to_no)
    context.log.debug("redirect_to response for number: %s \n%s"
                     % (context.redirect_to_no, context.redir_resp))


@then('I should retrieve a new number to call')
def step_impl(context):
    assert context.redir_resp["redirectTo"] is not None

    assert \
        context.redir_resp["redirectTo"] == context.redirect_to_no, \
        "Received redirectTo: '%s' is different from the requested: '%s'" \
        % (context.redir_resp["redirectTo"], context.redirect_to_no)

    assert \
        context.redir_resp["numberToCall"] is not context.redirect_to_no, \
        "Received numberToCall: %s is same as requested redirect_to_no: %s" \
        % (context.redir_resp["numberToCall"], context.redirect_to_no)

    assert \
        context.redir_resp["callerId"] == context.caller_id, \
        "Received callerId: %s is different from send: %s" \
        % (context.redir_resp["callerId"], context.caller_id)

    assert \
        context.redir_resp["redirectTo"] != context.redir_resp["numberToCall"],\
        "Rcvd redirectTo: '%s' is the same as received numberToCall: '%s'" \
        % (context.redir_resp["redirectTo"], context.redir_resp["numberToCall"])


@given('I retrieved a number to call for "{inbound_twilio_number}"')
def step_impl(context, inbound_twilio_number):
    """
    Get a new Caller ID
    Get a new number to call to redirect to given number
    """
    context.redirect_to_no = inbound_twilio_number
    context.cch = CallConnectHandler("http://callconnect.poc.hibulabs.co.uk")
    context.caller_id = context.cch.get_new_caller_id()
    context.redir_resp = context.cch.get_redirect_to(
        caller_id=context.caller_id,
        number=context.redirect_to_no)
    context.log.debug("redirect_to response for number: %s \n%s"
                      % (context.redirect_to_no, context.redir_resp))
    context.caller = Caller()
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
