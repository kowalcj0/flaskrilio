Feature: Call Connect Handler
    As Behave I'd like to be able to use Call Connect service


    Scenario: Successful Flask setup
        Given a CallConnect service

    
    Scenario: Get a new Caller ID
        Given a CallConnect service
        When I ask for a new Caller ID
        Then I should retrieve a Caller ID


    Scenario: Delete Caller ID
        Given a new Caller ID
        When I delete my Caller ID
        Then my Caller ID should be deleted


    Scenario Outline: Get a new redirect to number
        Given I'm a new user
        When I ask for a new number to call for a "<redirect_to_no>"
        Then I should retrieve a new number to call

    Examples: example fake umbers
        |  redirect_to_no    |
        | +447402028595      |
        | +442012234243      |
        | +447402342342      |


    Scenario Outline: Delete my Caller ID after retrieving new number to call
        Given I'm a new user
        When I ask for a new number to call for a "<redirect_to_no>"
        And this number is different from number "<redirect_to_no>"
        Then I should retrieve a new number to call
        When I delete my Caller ID
        Then my Caller ID should be deleted

    Examples: example fake umbers
        |  redirect_to_no    |
        | +447402028595      |
        | +442012234243      |
        | +447402342342      |


    Scenario: Get the Number Pool
        Given a CallConnect service
        When I ask for a Number Pool
        Then I should retrieve a Number Pool


    Scenario: Check the number of numbers in the Number Pool
        Given a CallConnect service
        When I ask for a Number Pool
        Then I should retrieve a Number Pool with at least '5' numbers in it

    @invalid
    Scenario Outline: CC service should work only with UK mobile numbers
        Given I'm a new user
        When I ask for a new number to call for an invalid '<redirect_to_no>'
        Then I should get an expected '<err_type>' with '<err_details>'

    Examples: example fake umbers
        |  redirect_to_no   |   err_type    |  err_details      |
        | +48507176130      |   resp_code   |   400             |
        | +442012234243     |   resp_code   |   400             |
        | +441234567890     |   resp_code   |   400             |
        | 000000000000      |   resp_code   |   400             |
        | +000000000000     |   resp_code   |   400             |


        #allowed UK numbers
        #freephones
        #mobile
        #landline
        #
        #no premium rate 
    #no immarsta
    #other crap

    
