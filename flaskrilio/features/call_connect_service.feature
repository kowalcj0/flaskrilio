Feature: CallConnect and Twilio handlers
    As Mobile App I'd like to use CallConnect service to make call to
    to iYP Bussinesses


    Background: Check Twilio account prerequisities
        Given a Twilio connection
        And a CallConnect service
        And a Flaskrilio connection
        And that we have at least "2" incoming Twilio numbers
        And we name subsequent available numbers as "caller, merchant"
        And "caller"'s "status callback" URL is set to a publicly available host
        And "merchant"'s "status callback" URL is set to a publicly available host
        And "merchant"'s "voice request" URL is set to a publicly available host

    @wip
    Scenario: Call a Merchant via CallConnect service
        When I get a number to call for "merchant"'s number
        And this number to call is different from "merchant"'s number
        And I call this number to call from "caller"'s number
        And I wait "20" seconds for the call to finish
        Then I should see CSU records for both call legs in flaskrilio DB
        And both call legs should be in "completed" status
        And I should be able to fetch details for both Twilio call legs
        And the difference between start times of both call legs should be less than "5" seconds
        

    @skip
    Scenario: Call CallConnect number to call from a withheld number


    @skip
    Scenario: Call CallConnect number from a number different from the one we used to get the redirection for


    @skip
    Scenario: Call CallConnect number pointing at a busy number


    @skip
    Scenario: Call CallConnect number from an internation number
