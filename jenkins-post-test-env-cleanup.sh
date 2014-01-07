#!/usr/bin/env bash

echo "Jenkins post-test env cleanup"

rm -f $WORKSPACE/ec2.pem
sed -i -e "/account_sid=/ s/=.*/=/" $WORKSPACE/flaskrilio/twilio.cfg
sed -i -e "/auth_token=/ s/=.*/=/" $WORKSPACE/flaskrilio/twilio.cfg
sed -i -e "/'access_key' : / s/:.*/: '',/" $WORKSPACE/ec2_configuration.py
sed -i -e "/'secret_key' : / s/:.*/: '',/" $WORKSPACE/ec2_configuration.py
