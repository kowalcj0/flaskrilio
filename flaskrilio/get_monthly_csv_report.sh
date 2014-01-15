#!/usr/bin/env bash
# Author: Janusz Kowalczyk
# Created: 2014-01-15

# Check whether all required parameters are present
# if not, then prompt for them
if [ -z "$HV_HOST" ] ; then HV_HOST="http://voice.dev.hibulabs.co.uk"; fi;
if [ -z "$OUTPUT_FILE" ] ; then OUTPUT_FILE="call_report.csv"; fi;

if [[ -z "${HV_USERNAME}" ]] && [[ -z "${HV_PASSWORD}" ]] ; then
    echo "Please provide the HibuVoice username and hit [ENTER]:";
    read HV_USERNAME
    echo "Please provide the HibuVoice password and hit [ENTER]:";
    read -s HV_PASSWORD
else
    echo "Using credentials provided as parameters to this script!"
fi

if [[ -z "${FROM_DATE}" ]] && [[ -z "${TO_DATE}" ]] ; then
    echo "Please provide the date (using format: 01-Jan-2013) from which you want to download the CSV report and hit [ENTER]:";
    read FROM_DATE
    echo "Please provide the date (using format: 01-Jan-2013) to which you want to download the CSV report and hit [ENTER]:";
    read TO_DATE
else
    echo "Using dates provided as parameters to this script!"
fi

# this will get the initial Play Session cookie used for authentication
INITIAL_COOKIE=`curl --silent -I -XGET "${HV_HOST}/login" | grep -oP "(?<=PLAY_SESSION=\")(.*)(?=\")"`;

# This will use initial cookie and user credentials to authenticate user
# and get a valid Play Session cookie
AUTH_COOKIE=`curl --silent -I --cookie "PLAY_SESSION=\"${INITIAL_COOKIE}\"" -XPOST "${HV_HOST}/login?username=${HV_USERNAME}&password=${HV_PASSWORD}" | grep -oP "(?<=PLAY_SESSION=\")(.*)(?=\")"`

# this will use Play Session cookie to download CSV calls report
$(curl --silent -o "./${OUTPUT_FILE}" --cookie "PLAY_SESSION=\"${AUTH_COOKIE}\"" -XGET "${HV_HOST}/calls/allcalls.csv?fromDate=${FROM_DATE}&toDate=${TO_DATE}") && {
    echo "CSV report successfully saved in: ${OUTPUT_FILE}";
} || {
    echo "[ERROR] Couldn't download the report!!!"
}
