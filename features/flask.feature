Feature: As a website owner,
    I want to make sure that Flaskrilio is working fine and is serving
    all the Twilio requests properly

  Scenario: Successful Flaskrilio setup
     Given Flaskrilio is set up
      When I go to the root page
      Then I should see the message "Welcome"

  Scenario Outline: Successful Flaskrilio setup
        Given Flaskrilio is set up
        When I go to a default "<ctx>"
        Then I should get a default response containing "<text>"

        Examples: all default contexts
            |   ctx     |   text                     |
            |   vru     | voice request response     |
            |   vfu     | voice fallback response    |
            |   scu     | status callback response   |
            |   mru     | messaging request response |
