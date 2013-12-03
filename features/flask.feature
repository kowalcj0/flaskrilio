Feature: As a website owner,
            I want to secure my website

  Scenario: Successful Flask setup
     Given flaskr is setup
      When i go to the root page
      Then i should see the message "Welcome"
