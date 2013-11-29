# -*- coding: utf-8 -*-
from behave import *
from call_connect_handler import CallConnectHandler

@given('a CallConnect service')
def step_impl(context):
    cch = CallConnectHandler("http://callconnect.poc.hibulabs.co.uk")
    context.cch = cch

@when('I ask for a new UUID')
def step_impl(context):
    uuid = context.cch.get_new_uuid()
    context.uuid = uuid

@then('I should retrieve a UUID')
def step_impl(context):
    assert context.uuid != None
    print context.uuid
    #redir = cc.get_redirect_to(id, "+447402028595")
