from behave import *


@given(u'Flaskrilio is set up')
def flask_setup(context):
    assert context.client


@when(u'I go to the root page')
def go_to_root_page(context):
    context.page = context.client.get('/', follow_redirects=True)
    assert context.page


@then(u'I should see the message "{message}"')
def welcome_msg(context, message):
    assert message in context.page.data


@when(u'I go to a default "{ctx}"')
def default_ctx_msg(context, ctx):
    context.page = context.client.get('/%s' % ctx, follow_redirects=True)


@then(u'I should get a default response containing "{text}"')
def check_if_default_response_contains(context, text):
    print context.page.data
    assert text in context.page.data, "Response doesn't contain: %s" % text
