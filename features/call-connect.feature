Feature: Call Connect Handler
    As Behave I'd like to be able to use Call Connect service


    Scenario: Successful Flask setup
        Given a CallConnect service

    
    Scenario: Get a new Caller ID
        Given a CallConnect service
        When I ask for a new Caller ID
        Then I should retrieve a Caller ID


    Scenario Outline: Get a new redirect to number
        Given I'm a new user
        When I ask for a new number to call for a "<redirect_to_no>"
        Then I should retrieve a new number to call

    Examples: example fake umbers
        |  redirect_to_no    |
        | +447402028595      |
        | +442012234243      |
        | +447402342342      |
