Feature: CallConnect and Twilio handlers
    As Mobile App I'd like to use CallConnect service to make call to
    to iYP Bussinesses

    Scenario Outline: View all incoming Twilio numbers
        Given a Twilio connection
        When I get all incoming Twilio numbers
        Then I should be able to find "<number>" on this list

        Examples: twilio numbers
            | number        |
            | +441353210177 |
            | +442033224597 |


    Scenario Outline: Get Twilio number sid
        Given a Twilio connection
        Then I should be able to get number_sid for "<number>"

        Examples: twilio numbers
            | number        |
            | +441353210177 |
            | +442033224597 |


    Scenario Outline: Update Status Callback URL to an example host
        Given a Twilio connection
        When I update the callback url to:"http://example.com" for "<number>"
        Then the callback url should be correctly updated

        Examples: twilio numbers
            | number        |
            | +441353210177 |
            | +442033224597 |


    Scenario Outline: Update Status Callback URL to current public host
        Given a Twilio connection
        When I update the callback url to current public host for "<number>"
        Then the callback url should be correctly updated

        Examples: twilio numbers
            | number        |
            | +441353210177 |
            | +442033224597 |


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


    @skip
    Scenario: Call CallConnect number to call from a withheld number


    @skip
    Scenario: Call CallConnect number from a number different from the one we used to get the redirection for


    @skip
    Scenario: Call CallConnect number pointing at a busy number


    @skip
    Scenario: Call CallConnect number from an internation number
