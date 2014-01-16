# -*- coding: utf-8 -*-
from behave import *
from time import sleep
from handlers.twilio_handler import TwilioHandler


@When('I get a number to call for "{number_name}"\'s number')
def step_impl(context, number_name):
    # access number object from context, ie. context.caller
    number = getattr(context, number_name)
    context.redirect_to_no = number.phone_number
    if not hasattr(number, "caller_id"):
        number.caller_id = context.cch.get_new_caller_id()
        context.log.debug(
            "Got new callerId %s as it wasn't present in the context!" \
            % number.caller_id)
    context.redir_resp = context.cch.get_redirect_to(
        caller_id=number.caller_id,
        number=context.redirect_to_no)
    context.number_to_call = context.redir_resp.json()['numberToCall']


@when('this number to call is different from "{number_name}"\'s number')
def step_impl(context, number_name):
    number = getattr(context, number_name)
    assert context.number_to_call != number.phone_number, \
      "Number pool is full! Because received numberToCall:'%s' is the same as " \
      "requested %s's number:'%s' !" \
      % (context.number_to_call, number_name, number.phone_number)


@When('I call this number to call from "{number_name}"\'s number')
def step_impl(context, number_name):
    """
    This step requires:
        from number: in this case number specified in the story examples
        to number: numberToCall retrieved from the Call Connect Service
        twiml_url: served by the local flaskrilio instance
    """
    number = getattr(context, number_name)
    context.from_no = number.phone_number
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


@Then("I should see CSU records for both call legs in flaskrilio DB")
def step_impl(context):
    # select last matching outband and inbound calls
    context.outbound_call = \
            context.db.get_last_outbound_call(context.from_no,
                                              context.number_to_call)
    context.inbound_call = \
            context.db.get_last_inbound_call(context.from_no,
                                             context.redirect_to_no)
    context.log.debug("Outbound call: %s" % context.outbound_call)
    context.log.debug("Inbound call: %s" % context.inbound_call)
    assert context.outbound_call and context.inbound_call is not None, \
            "Couldn't find call records for both call legs in DB! \n" \
            "Outbound call record: %s\n" \
            "Inbound call record: %s\n" \
                    % (context.outbound_call, context.inbound_call)


@then('both call legs should be in "{status}" status')
def step_impl(context, status):
    assert context.outbound_call['CallStatus'] == status, \
            "Outbound call status is: %s where expected: %s" \
            % (context.outbound_call['CallStatus'], status)
    assert context.inbound_call['CallStatus'] == status, \
            "Inbound call status is: %s where expected: %s" \
            % (context.inbound_call['CallStatus'], status)


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



