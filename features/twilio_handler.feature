Feature: CallConnect and Twilio handlers
    As Mobile App I'd like to use CallConnect service to make call to
    to iYP Bussinesses


    Scenario Outline: call from twilio number to any number
        Given a Twilio connection
        And a CallConnect service
        And a Flaskrilio connection
        When I get a number to call for "<to_number>"
        And this number is different from number "<to_number>"
        And I call this number from "<from_number>"
        And I wait "15" seconds for the call to finish
        Then I should see CSU records for both call legs in flaskrilio DB
        And both call legs should be in "completed" status
        And I should be able to fetch details for both Twilio call legs
        And the difference between start times of both call legs should be less than "5" seconds

    Examples: real twilio numbers
        | to_number     | from_number   |
        | +442033224597 | +441353210177 |


    Scenario: Call CallConnect number to call from a withheld number

    Scenario: Call CallConnect number from a number different from the one we used to get the redirection for

    Scenario: Call CallConnect number pointing at a busy number
