# -*- coding: utf-8 -*-
from behave import *
from time import sleep
from handlers.twilio_handler import TwilioHandler


@given('a Twilio connection')
def step_impl(context):
    assert context.th, "Connection with Twilio is not established!"


@given('that we have at least "{number}" incoming Twilio numbers')
def step_impl(context, number):
    number = int(number)
    if not hasattr(context, 'all_incoming_numbers'):
        context.log.debug("No incoming numbers stored in the test context. "
                          "Getting all incoming numbers from Twilio...")
        context.all_incoming_numbers = context.th.get_all_incoming_twilio_numbers()
    no_of_numbers = len(context.all_incoming_numbers)
    context.log.debug("Configured Twilio account has '%s' incoming numbers " \
                      "configured" % no_of_numbers)
    assert no_of_numbers >= number, \
            "Configured account has only '%d' incoming numbers " \
            "where at least '%d' is required!!" % (no_of_numbers, number)


@given('we name subsequent available numbers as "{number_names}"')
def step_impl(context, number_names):
    # split using two delimiters: ',' ' '
    names = number_names.split(', ')
    context.log.debug("List of number names after splitting: '%s'" % names)
    # enumerate get's the list as an enumerate object
    # http://docs.python.org/2/library/functions.html#enumerate
    # thanks to this, we can use the index value to access matching number
    # from the all_incoming_numbers list
    for index, name in enumerate(names):
        number = context.all_incoming_numbers[index]
        setattr(context, name, number)
        context.log.debug("Successfully set '%s' as the '%s'" \
                          % (number.phone_number, name))


@When('I update the "{number}"\'s "{url_name}" URL to:"{url}"')
def step_impl(context, number, url_name, url):
    context.ctx_url = url
    if url_name == "voice request":
        context.th.update_number_vru_url(
            number_sid=getattr(context, number).sid,
            vru=context.ctx_url)
    elif url_name == "voice fallback":
        context.th.update_number_vfu_url(
            number_sid=getattr(context, number).sid,
            vfu=context.ctx_url)
    elif url_name == "status callback":
        context.th.update_number_scu_url(
            number_sid=getattr(context, number).sid,
            scu=context.ctx_url)
    elif url_name == "messaging request":
        context.th.update_number_mru_url(
            number_sid=getattr(context, number).sid,
            mru=context.ctx_url)
    elif url_name == "messaging fallback request":
        context.th.update_number_mfu_url(
            number_sid=getattr(context, number).sid,
            mfu=context.ctx_url)
    else:
        assert False, "Unknown URL type: '%s'" % url_name



@given(u'"{number}"\'s "{url_name}" URL is set to a publicly available host')
@when(u'I update "{number}"\'s "{url_name}" URL to publicly available host')
def step_impl(context, number, url_name):
    if url_name == "voice request":
        context.ctx_url = "%s/vru" % context.publichost
        context.th.update_number_vru_url(
            number_sid=getattr(context, number).sid,
            vru=context.ctx_url)
    elif url_name == "voice fallback":
        context.ctx_url = "%s/vfu" % context.publichost
        context.th.update_number_vfu_url(
            number_sid=getattr(context, number).sid,
            vfu=context.ctx_url)
    elif url_name == "status callback":
        context.ctx_url = "%s/scu" % context.publichost
        context.th.update_number_scu_url(
            number_sid=getattr(context, number).sid,
            scu=context.ctx_url)
    elif url_name == "messaging request":
        context.ctx_url = "%s/mru" % context.publichost
        context.th.update_number_mru_url(
            number_sid=getattr(context, number).sid,
            mru=context.ctx_url)
    elif url_name == "messaging fallback request":
        context.ctx_url = "%s/mfu" % context.publichost
        context.th.update_number_mfu_url(
            number_sid=getattr(context, number).sid,
            mfu=context.ctx_url)
    else:
        assert False, "Unknown URL type: '%s'" % url_name


@Then('the "{number}"\'s "{url_name}" URL should be updated correctly')
def step_impl(context, number, url_name):
    number_details = context.th.get_number_details(number_sid=getattr(context, number).sid)
    if url_name == "voice request":
        assert number_details.voice_url == context.ctx_url
    elif url_name == "voice fallback":
        assert number_details.voice_fallback_url == context.ctx_url
    elif url_name == "status callback":
        assert number_details.status_callback == context.ctx_url
    elif url_name == "messaging request":
        assert number_details.sms_url == context.ctx_url
    elif url_name == "messaging fallback request":
        assert number_details.sms_fallback_url == context.ctx_url
    else:
        assert False, "Unknown URL type: '%s'" % url_name


