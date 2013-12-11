Feature: Local SqLite3 DB connection
    As Behave I'd like to be able to connect to local Sqlite3 database
    Managed by Fliskrilio script and which contains test call records 


    Scenario: Behave has connection to local sqlite db
        Given a Sqlite3 connection
        When I search for call records
        Then I should have access to call records
