Feature: Count call redirects
    As Mobile App I'd like to count the number of calls made to iYP Bussinesses
    using the CallConnect service


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

    Scenario Outline: Call retrieved number to call
        Given I retrieved a number to call for "<inbound_twilio_number>"
        When I call this number to call from "<outbound_twilio_number>"
        #And I wait "0.3" seconds for the call to finish
        #Then I should be redirected to "<inbound_twilio_number>"
        #And I should be able to download the call recording

    Examples: real twilio numbers
        | inbound_twilio_number | outbound_twilio_number    |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
        | +442033224597         | +441353210177             |
