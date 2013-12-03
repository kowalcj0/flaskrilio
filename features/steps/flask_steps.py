from behave import *


@given(u'flaskr is setup')
def flask_setup(context):
    assert context.client


@when(u'i go to the root page')
def go_to_root_page(context):
    context.page = context.client.get('/', follow_redirects=True)
    assert context.page


@then(u'i should see the message "{message}"')
def welcome_msg(context, message):
    assert message in context.page.data
