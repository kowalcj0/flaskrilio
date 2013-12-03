Feature: As a CC client
            I want to access callback endpoint

  Scenario: Successful Flask setup
     Given flaskr is setup
     And a CallConnect service
     When i go to the root page
     Then i should see the message "Welcome"
     When I ask for a new Caller ID
     Then I should retrieve a Caller ID
     When I send this Caller ID to the callback endpoint
     Then I should see Caller ID in the response
    
