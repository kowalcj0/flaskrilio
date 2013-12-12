# -*- coding: utf-8 -*-
import logging
from behave import *


@given('a CallConnect service')
def step_impl(context):
    assert context.cch


@given('I\'m a new user')
@when('I ask for a new Caller ID')
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


@when('I ask for a new number to call for a "{redirect_to_no}"')
def step_impl(context, redirect_to_no):
    context.redirect_to_no = redirect_to_no
    context.redir_resp = context.cch.get_redirect_to(
        caller_id=context.caller_id,
        number=context.redirect_to_no)


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

