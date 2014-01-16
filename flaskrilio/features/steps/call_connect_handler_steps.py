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
    context.number_to_call = context.redir_resp.json()['numberToCall']


@when('this number is different from number "{number}"')
def step_impl(context, number):
    assert context.number_to_call != number, \
      "Number pool is full! Because the numberToCall:'%s' is the same as " \
      "our outbound number:'%s' !" \
      % (context.number_to_call, number)


@When("I delete my Caller ID")
def step_impl(context):
    resp = context.cch.delete_caller_id(context.caller_id)
    context.log.debug("Deleting returned: %d" % resp.status_code)


@Then("my Caller ID should be deleted")
def step_impl(context):
    resp = context.cch.get_callers_details(context.caller_id)
    context.log.debug("Response code: %s " % resp.status_code)
    assert resp.status_code == 404, "Expected callerId to be deleted and receive 404 not %d " % resp.status_code



@then('I should retrieve a new number to call')
def step_impl(context):
    assert context.redir_resp.json()["redirectTo"] is not None

    assert \
        context.redir_resp.json()["redirectTo"] == context.redirect_to_no, \
        "Received redirectTo: '%s' is different from the requested: '%s'" \
        % (context.redir_resp.json()["redirectTo"], context.redirect_to_no)

    assert \
        context.redir_resp.json()["numberToCall"] is not context.redirect_to_no, \
        "Received numberToCall: %s is same as requested redirect_to_no: %s" \
        % (context.redir_resp.json()["numberToCall"], context.redirect_to_no)

    assert \
        context.redir_resp.json()["callerId"] == context.caller_id, \
        "Received callerId: %s is different from send: %s" \
        % (context.redir_resp.json()["callerId"], context.caller_id)

    # if these two numbers are the same, then the Number Pool is full
    # and this is expected behaviour. So no assertion here, just a warning msg
    if context.redir_resp.json()["redirectTo"] == context.redir_resp.json()["numberToCall"]:
        context.log.debug("Number Pool is Full!! "\
                         "Received redirectTo: '%s' is the same as " \
                         "received numberToCall: '%s'" \
                         % (context.redir_resp.json()["redirectTo"],
                            context.redir_resp.json()["numberToCall"]))

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
        assert len(context.pool.json()) >= int(numbers), "Number Pool has less than %d Numbers in it!! %d " % (len(context.pool.json()), int(numbers))


@when("I ask for a new number to call for an invalid '{number}'")
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


@Then("I should get an expected '{err_type}' with '{err_details}'")
def step_impl(context, err_type, err_details):
    if err_type == "resp_code":
        assert context.redir_resp.status_code == int(err_details), \
        "Expected %s to be %s but got %s" % (err_type, err_details, context.redir_resp.status_code)
