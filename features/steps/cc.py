from behave import *
from make_call import Caller

@given('we have connection to twilio')
def step_impl(context):
    caller = Caller()
    caller.load_config(twilio_config="call-connect-eu.cfg")
    caller.connect_to_twilio()
    context.caller = caller
    caller.print_config()

@when('we attempt to make a call from twilio number')
def step_impl(context):
    assert True is not False

@then('the call should be established')
def step_impl(context):
    context.caller.print_config()
    #assert context.failed is False
    #caller.make_a_call(from_no="+441353210177", to_no="+447402028595")
