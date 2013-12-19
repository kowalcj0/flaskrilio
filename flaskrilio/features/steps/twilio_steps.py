# -*- coding: utf-8 -*-
from behave import *
from time import sleep
from handlers.twilio_handler import TwilioHandler


@given('a Twilio connection')
def step_impl(context):
    assert context.th, "Connection with Twilio is not established!"


@when('I call this number from "{number}"')
@given('I call this number from "{number}"')
def step_impl(context, number):
    """
    This step requires:
        from number: in this case number specified in the story examples
        to number: numberToCall retrieved from the Call Connect Service
        twiml_url: served by the local flaskrilio instance
    """
    context.from_no = number
    context.log.debug("Calling from:%s to:%s" \
                      % (context.from_no, context.number_to_call))
    context.call = context.th.call_with_twiml(
        from_no=context.from_no,
        to_no=context.number_to_call,
        twiml_url="%s/vru/test-say-something.xml" % context.publichost,
        scu_url="%s/scu" % context.publichost)


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


@then("I should be able to fetch details for both Twilio call legs")
def step_impl(context):
    from dateutil import parser
    # get call details
    context.outbound_call_details = context.th.get_call_details(context.outbound_call['CallSid'])
    context.inbound_call_details = context.th.get_call_details(context.inbound_call['CallSid'])
    context.log.debug("Outbound call details: %s" % context.outbound_call_details.__dict__)
    context.log.debug("Inbound call details: %s" % context.inbound_call_details.__dict__)
    # parse and reformat the times
    out_start = parser.parse(context.outbound_call_details.start_time).strftime("%Y-%m-%d %H:%M:%S %z")
    out_end = parser.parse(context.outbound_call_details.end_time).strftime("%Y-%m-%d %H:%M:%S %z")
    in_start = parser.parse(context.inbound_call_details.start_time).strftime("%Y-%m-%d %H:%M:%S %z")
    in_end = parser.parse(context.inbound_call_details.end_time).strftime("%Y-%m-%d %H:%M:%S %z")
    # save them in the DB
    context.db.add_times_to_call(context.outbound_call_details.sid, out_start, out_end)
    context.db.add_times_to_call(context.inbound_call_details.sid, in_start, in_end)



@then('the difference between start times of both call legs should be less than "{seconds}" seconds')
def step_impl(context, seconds):
    from dateutil import parser
    out_start = parser.parse(context.outbound_call_details.start_time)
    in_start = parser.parse(context.inbound_call_details.start_time)
    # to int
    seconds = int(seconds)
    delta = (in_start - out_start).seconds
    assert delta <= seconds, \
            "Time delta between the call legs is greater than: %d" % seconds



@when("I get all incoming Twilio numbers")
def step_impl(context):
    context.all_incoming_numbers = context.th.get_all_incoming_twilio_numbers()


@Then('I should be able to find "{number}" on this list')
def step_impl(context, number):
    found = False
    for n in context.all_incoming_numbers:
        if n.phone_number == number:
            found = True
    assert found == True, "Couldn't find number:%s on the list of all numbers!!!" % number


@then('I should be able to get number_sid for "{number}"')
def step_impl(context, number):
    context.number_sid = context.th.get_number_sid_for_phone(number)
    assert context.number_sid is not None, "Couldn't find number: %s " \
            "on the list of all incoming numbers!!!" % number


@when('I update the callback url to:"{scu_url}" for "{number}"')
def step_impl(context, scu_url, number):
    if not hasattr(context, 'number_sid'):
        context.number_sid = context.th.get_number_sid_for_phone(number)
    context.scu_url = scu_url
    context.th.update_number_scu_url(
        number_sid=context.number_sid,
        callback=context.scu_url)


@When('I update the callback url to current public host for "{number}"')
def step_impl(context, number):
    if not hasattr(context, 'number_sid'):
        context.number_sid = context.th.get_number_sid_for_phone(number)
    context.scu_url = "%s/scu" % context.publichost
    context.th.update_number_scu_url(
        number_sid=context.number_sid,
        callback=context.scu_url)


@then('the callback url should be correctly updated')
def step_impl(context):
    number_details = context.th.get_number_details(number_sid=context.number_sid)
    assert number_details.status_callback == context.scu_url
