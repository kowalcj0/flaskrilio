# -*- coding: utf-8 -*-
from behave import *
from call_connect_handler import CallConnectHandler
import logging

def before_feature(context, feature):
    print "before feature"

def after_feature(context, feature):
    print "after feature"

@given('a CallConnect service')
def step_impl(context):
    cch = CallConnectHandler("http://callconnect.poc.hibulabs.co.uk")
    context.cch = cch

@when('I ask for a new UUID')
def step_impl(context):
    uuid = context.cch.get_new_uuid()
    context.uuid = uuid
    print uuid

@then('I should retrieve a UUID')
def step_impl(context):
    logging.debug(context.uuid)
    assert context.uuid != None


@given('I\'m a new user')
def step_impl(context):
    context.cch = CallConnectHandler("http://callconnect.poc.hibulabs.co.uk")
    context.uuid = context.cch.get_new_uuid()

@when('I ask for a new redirect to number for a "{merchant_no}"')
def step_impl(context, merchant_no):
    print merchant_no
    context.redirect_to = context.cch.get_redirect_to(context.uuid, "+447402028595")
    logging.debug("redirect_to response for number: %s \n%s" % (merchant_no, context.redirect_to))
    print("redirect_to response for number: %s %s" % (merchant_no, context.redirect_to))

@then('I should retrieve a new redirect to number')
def step_impl(context):
    assert context.redirect_to != None
