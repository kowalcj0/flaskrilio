# -*- coding: utf-8 -*-
'''
Created on 24 May 2013

@author: jk
'''
import boto.ec2
import time


# http://engineerwithoutacause.com/amazon-ec2-deployment-with-boto.html
class EC2Conn:
    """
    A Class to crate EC2 Connection
    """


    def __init__(self, region, main_sg, main_kp, access_key, secret_key, key_path, user_name):
            self.conn = None
            self.region = region
            self.main_sg    = main_sg
            self.main_kp    = main_kp
            self.key_path   = key_path
            self.access_key = access_key
            self.secret_key = secret_key
            self.user_name = user_name


    """
    Establishes an EC2 connection
    """
    def connect(self):
            #self.conn = EC2Connection(self.access_key, self.secret_key)
            self.conn = boto.ec2.connect_to_region(
                region_name=self.region,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key)


    """
    Creates an instance defined in the SERVER_TYPES dict

    :rtype: Instance
    :return: An instance of :class`boto.ec2.instance.Instance`
    """
    def create_instance(self, instance_type):
            reservation = self.conn.run_instances( **instance_type )
            print reservation
            instance = reservation.instances[0]
            time.sleep(10)
            while instance.state != 'running':
                    time.sleep(5)
                    instance.update()
                    print "Instance state: %s" % (instance.state)

            print "instance %s done! IP Address: %s " % (instance.id, instance.ip_address)
            return instance


    """
    Creates desired number of instances of the same type

    :type count: int
    :param count: Number of instances to create. Default is 1.

    :rtype: Instance
    :return: A list of instances of :class`boto.ec2.instance.Instance`
    """
    def create_instances(self, instance_type, count=1):
            reservation = self.conn.run_instances(min_count=count, max_count=count, **instance_type )
            print reservation
            time.sleep(10)
            for i in reservation.instances:
                while i.state != 'running':
                    time.sleep(5)
                    i.update()
                    print "Instance %s state: %s" % (i.id, i.state)

            for i in reservation.instances:
                print "instance %s done! IP Address: %s " % (i.id, i.ip_address)
            return reservation.instances


    """
    Tag instance with tags

    :type instance: string
    :param instance: An Instance object of :class`boto.ec2.instance.Instance`

    :type tags: dict
    :param tags: A dictionary of tags that will be assigned to the Instance
        Use 'Name' to set instance name visible on EC2 Dashboard
    """
    def tag_instance(self, instance, tags):
        print "Adding Name tag to instance: %s " % (instance.id)
        self.conn.create_tags([(instance.id)], tags)
