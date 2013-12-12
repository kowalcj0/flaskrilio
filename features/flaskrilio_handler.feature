Feature: Flaskrilio connection
    As Behave I'd like to be able to connect to a local instance of Flaskrilio

    Scenario: Behave has a connection to local instance of Flaskrilio
        Given a Flaskrilio connection
        When I fetch call records
        Then I should retrieve call records
        
    Scenario: Successful Flaskrilio setup
        Given Flaskrilio is set up
        When I go to the home page
        Then I should see the message "Welcome"

   Scenario Outline: Default context responses
        Given Flaskrilio is set up
        When I go to a default "<ctx>"
        Then I should get a default response containing "<text>"

        Examples: all default contexts
            |   ctx     |   text                     |
            |   vru     | voice request response     |
            |   vfu     | voice fallback response    |
            |   scu     | status callback response   |
            |   mru     | messaging request response |
