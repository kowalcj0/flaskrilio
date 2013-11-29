Feature: make a call

      Scenario: call from twilio number to any number
             Given we have connection to twilio
             When we attempt to make a call from twilio number
             Then the call should be established
