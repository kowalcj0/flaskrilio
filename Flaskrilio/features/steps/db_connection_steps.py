# -*- coding: utf-8 -*-
import logging
from behave import *
from flaskrilio import dict_from_row

@given('a Sqlite3 connection')
def step_impl(context):
    assert context.db


@when('I search for call records')
def step_impl(context):
    context.calls = context.db.get_all_calls()
    context.log.debug("Calls in DB:\n%s\n" % context.calls)


@then('I should have access to call records')
def step_impl(context):
    assert context.calls is not None, "Couldn't access DB!!!"


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

