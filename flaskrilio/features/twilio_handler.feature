Feature: Twilio handler
    As the tester I'd like to use Twilio Handler to manage Twilio Account 
    And use it for testing CallConnect-Twilio interoperability


    Background: Check Twilio account prerequisities
        Given a Twilio connection
        And that we have at least "2" incoming Twilio numbers
        And we name subsequent available numbers as "caller, callee"


    @wip
    Scenario: test
        When I don't do something

    Scenario Outline: Update Status Callback URL to an example host
        When I update the "<number>"'s callback url to:"http://example.com"
        Then the "<number>"'s callback url should be updated correctly

        Examples: number names
            | number    |
            | caller    |
            | callee    |


    @twilio
    Scenario Outline: Update Status Callback URL to an example host
        When I update the callback url to:"http://example.com" for "<number>"
        Then the callback url should be correctly updated

        Examples: twilio numbers
            | number        |
            | +441353210177 |
            | +442033224597 |


    @twilio
    Scenario Outline: Update Status Callback URL to current public host
        Given a Twilio connection
        When I update the callback url to current public host for "<number>"
        Then the callback url should be correctly updated

        Examples: twilio numbers
            | number        |
            | +441353210177 |
            | +442033224597 |
