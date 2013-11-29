Feature: As Mobile App I'd like to count number of calls made to iYP Bussinesses
    by using CallConnect service


    Scenario: Get a new UUID
        Given a CallConnect service
        When I ask for a new UUID
        Then I should retrieve a UUID

    Scenario Outline: Get a new redirect to number
        Given I'm a new user
        When I ask for a new redirect to number for a "<merchant number>"
        Then I should retrieve a new redirect to number

    Examples: Merchant numbers
        |  merchant number   |
        | +447402028595      |
        | +442012234243      |
        | +447402342342      |

