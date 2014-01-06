Feature: Twilio handler
    As the tester I'd like to use Twilio Handler to manage Twilio Account 
    And use it for testing CallConnect-Twilio interoperability


    Background: Check Twilio account prerequisities
        Given a Twilio connection
        And that we have at least "2" incoming Twilio numbers
        And we name subsequent available numbers as "caller, callee"


    @twilio
    Scenario Outline: Update Status Callback URL to an example host
        When I update the "<number>"'s "status callback" URL to:"http://example.com"
        Then the "<number>"'s "status callback" URL should be updated correctly

        Examples: number names
            | number    |
            | caller    |
            | callee    |


    @twilio
    Scenario Outline: Update Status Callback URL to current public host
        When I update "<number>"'s "status callback" URL to publicly available host
        Then the "<number>"'s "status callback" URL should be updated correctly

        Examples: number names
            | number    |
            | caller    |
            | callee    |


    @twilio
    Scenario Outline: Update Status Voice Request URL to current public host
        When I update "<number>"'s "voice request" URL to publicly available host
        Then the "<number>"'s "voice request" URL should be updated correctly

        Examples: number names
            | number    |
            | caller    |
            | callee    |
