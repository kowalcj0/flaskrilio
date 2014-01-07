#!/usr/bin/env bash

echo "Jenkins pre-test env setup"

if [ -z "$EC2_PEM" ] ; then 
    echo "Required EC2_PEM parameter missing!!!"
    exit 55;
fi
if [ -z "$EC2_ACCESS_KEY" ] ; then 
    echo "Required EC2_ACCESS_KEY parameter missing!!!"
    exit 66; 
fi
if [ -z "$EC2_SECRET_KEY" ] ; then 
    echo "Required EC2_SECRET_KEY parameter missing!!!"
    exit 77; 
fi
if [ -z "$TWILIO_ACCOUNT_SID" ] ; then 
    echo "Required TWILIO_ACCOUNT_SID parameter missing!!!"
    exit 88; 
fi
if [ -z "$TWILIO_AUTH_TOKEN" ] ; then 
    echo "Required TWILIO_AUTH_TOKEN parameter missing!!!"
    exit 99; 
fi

# delete all old pyc files
find . -name "*.pyc" -exec rm -rf {} \;

# parse EC2 ssh key passed as string
# and save it in a pem file
rm -f $WORKSPACE/ec2.pem
echo "-----BEGIN RSA PRIVATE KEY-----" > $WORKSPACE/ec2.pem
for i in $(echo $EC2_PEM | tr " " "\n"); do
    echo $i >> $WORKSPACE/ec2.pem
done
echo "-----END RSA PRIVATE KEY-----" >> $WORKSPACE/ec2.pem
chmod 400 $WORKSPACE/ec2.pem

# use config template if required file is not available
if [ ! -e "$WORKSPACE/flaskrilio/twilio.cfg" ]; then
    cp $WORKSPACE/flaskrilio/docs/templates/twilio.cfg.template $WORKSPACE/flaskrilio/twilio.cfg
fi
# set twilio credentials
sed -i -e "/account_sid=/ s/=.*/=$TWILIO_ACCOUNT_SID/" $WORKSPACE/flaskrilio/twilio.cfg
sed -i -e "/auth_token=/ s/=.*/=${TWILIO_AUTH_TOKEN}/" $WORKSPACE/flaskrilio/twilio.cfg

# use config template if required file is not available
if [ ! -e "$WORKSPACE/ec2_configuration.py" ]; then
    cp $WORKSPACE/flaskrilio/docs/templates/ec2_configuration.py.template $WORKSPACE/ec2_configuration.py
fi
# set EC2 credentials
sed -i -e "/'access_key' : / s/:.*/: '$EC2_ACCESS_KEY',/" $WORKSPACE/ec2_configuration.py
sed -i -e "/'secret_key' : / s/:.*/: '$EC2_SECRET_KEY',/" $WORKSPACE/ec2_configuration.py
