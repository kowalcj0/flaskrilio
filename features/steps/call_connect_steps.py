# -*- coding: utf-8 -*-
import logging
from behave import *


@given('a CallConnect service')
def step_impl(context):
    assert context.cch


@given('I\'m a new user')
@when('I ask for a new Caller ID')
@given(u'a new Caller ID')
def step_impl(context):
    context.caller_id = context.cch.get_new_caller_id()


@then('I should retrieve a Caller ID')
def step_impl(context):
    assert context.caller_id is not None


@then("I should see Caller ID in the response")
def step_impl(context):
    assert \
        context.caller_id in context.page.data, \
       "Couldn't find callerId: %s in the response: %s" \
        % (context.caller_id, context.page.data)


@when('I ask for a new number to call for a "{number}"')
@when('I get a number to call for "{number}"')
@given('I got a number to call for "{number}"')
def step_impl(context, number):
    context.redirect_to_no = number
    if not hasattr(context, "caller_id"):
        context.caller_id = context.cch.get_new_caller_id()
        context.log.debug(
            "Got new callerId %s as it wasn't present in the context!" \
            % context.caller_id)
    context.redir_resp = context.cch.get_redirect_to(
        caller_id=context.caller_id,
        number=context.redirect_to_no)
    context.number_to_call = context.redir_resp['numberToCall']


@When("I delete my Caller ID")
def step_impl(context):
    code,resp = context.cch.delete_caller_id(context.caller_id)
    context.log.debug("Deleting returned: %d" % code)


@Then("my Caller ID should be deleted")
def step_impl(context):
    code,resp = context.cch.get_callers_details(context.caller_id)
    context.log.debug("Response code: %s " % code)
    assert code == 404, "Expected callerId to be deleted and receive 404 not %d " % code



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

    # if these two numbers are the same, then the Number Pool is full
    # and this is expected behaviour. So no assertion here, just a warning msg
    if context.redir_resp["redirectTo"] == context.redir_resp["numberToCall"]:
        context.log.debug("Number Pool is Full!! "\
                         "Received redirectTo: '%s' is the same as " \
                         "received numberToCall: '%s'" \
                         % (context.redir_resp["redirectTo"],
                            context.redir_resp["numberToCall"]))

@When("I ask for a Number Pool")
def step_impl(context):
    context.pool = context.cch.get_number_pool()


@Then("I should retrieve a Number Pool")
def step_impl(context):
    assert context.pool is not None, \
            "Expecting at least empty Number Pool, but got: %s" \
            % context.pool


@Then("I should retrieve a Number Pool with at least '{numbers}' numbers in it")
def step_impl(context, numbers):
    assert context.pool is not None, \
            "Expecting at least empty Number Pool, but got: %s" \
            % context.pool
    if context.pool is not None:
        assert len(context.pool) >= int(numbers), "Number Pool has less than %d Numbers in it!! %d " % (len(context.pool), int(numbers))
