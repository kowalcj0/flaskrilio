# -*- coding: utf-8 -*-
import logging
from behave import *


@given(u'Flaskrilio is set up')
@given(u'a Flaskrilio connection')
def step_impl(context):
    assert context.fh


@when(u'I fetch call records')
def step_impl(context):
    context.calls = context.fh.get_calls()['calls']


@then(u'I should retrieve call records')
def step_impl(context):
    assert context.calls is not None


@when(u'I go to the home page')
def go_to_root_page(context):
    context.homepage = context.fh.get_home()
    assert context.homepage


@then(u'I should see the message "{message}"')
def welcome_msg(context, message):
    assert message in context.homepage['msg'], \
            "Couldn't find '%s' in the response! Response: %s" \
            % (message, context.homepage)


@when(u'I go to a default "{ctx}"')
def default_ctx_msg(context, ctx):
    context.response = context.fh.get_twiml("/%s" % ctx)


@then(u'I should get a default response containing "{text}"')
def check_if_default_response_contains(context, text):
    assert text in context.response.read(), "Response doesn't contain: %s" % text
