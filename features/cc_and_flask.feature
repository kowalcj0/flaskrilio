Feature: As a CC client
            I want to access callback endpoint

  Scenario: Successful Flask setup
     Given Flaskrilio is set up
     And a CallConnect service
     When I go to the root page
     Then I should see the message "Welcome"
     When I ask for a new Caller ID
     Then I should retrieve a Caller ID
    
