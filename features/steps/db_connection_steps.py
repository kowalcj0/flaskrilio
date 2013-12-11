# -*- coding: utf-8 -*-
import logging
from behave import *
from flaskrilio import dict_from_row

@given('a Sqlite3 connection')
def step_impl(context):
    assert context.db


@when('I search for call records')
def step_impl(context):
    cur = context.db.execute('select * from calls order by id desc')
    context.calls = dict_from_row(cur)
    context.log.debug("Calls in DB:\n%s\n" % context.calls)


@then('I should have access to call records')
def step_impl(context):
    assert context.calls is not None, "Couldn't access DB!!!"
