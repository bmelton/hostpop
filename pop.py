import argparse
import boto.ec2
import os

class EC2ToAnsible:
    def __init__(self):
        self.access_key         = None
        self.secret_key         = None
        self.get_access_key()
        self.ansible_host_file  = "/etc/ansible/hosts"
        self.tag_to_peep        = "Ansible"
        self.preserve_hosts     = True

    def print_help_menu(self):
        print "####################################"
        print "#       EC2 to Ansible Hosts       #"
        print "####################################"
        print ""
        print " To run, python pop.py "
        print ""
        print " You should add your AWS_ACCESS_KEY and AWS_SECRET_KEY " 
        print " variables to the environment, using export. E.g., "
        print ""
        print " $ export AWS_ACCESS_KEY='01234567890'"
        print " $ export AWS_SECRET_KEY='01234567890'"
        print ""
        print " If you want to have pop write the file for you (warning, will not preserve existing entries),"
        print " then you should have write privileges to the file, otherwise you'll see an error."
        print ""
        return False

    def print_ips(self, ips):
        print " Add the following to your %s" % (self.ansible_host_file)
        print " "
        for ip in ips:
            print("%s" % ip)
        

    def get_access_key(self):
        both = False
        if os.environ.get("AWS_ACCESS_KEY"):
            self.access_key     = os.environ.get("AWS_ACCESS_KEY")

        if os.environ.get("AWS_SECRET_KEY"):
            self.secret_key     = os.environ.get("AWS_SECRET_KEY")

        if os.environ.get("AWS_ACCESS_KEY") and os.environ.get("AWS_SECRET_KEY"):
            both = True

        if not both:
            self.print_help_menu()
        else:
            print("AWS Keys provided by environment.");

    def preserve_existing_file(self):
        with open("%s" % self.ansible_host_file, "r") as myfile:
            pass
        pass


    def main(self):
        ips = []
        region = "us-east-1"
        ec2_conn = boto.ec2.connect_to_region(region, 
            aws_access_key_id=self.access_key, 
            aws_secret_access_key=self.secret_key)
        reservations = ec2_conn.get_all_reservations()

        print "Adding the following to ansible hosts:\r\n"
        print "    %s    %s" % ("State   ", "Name")

        for reservation in reservations:    
            for instance in reservation.instances:
                if instance.state == "running":
                    if self.tag_to_peep in instance.tags and "Name" in instance.tags:
                        if instance.tags[self.tag_to_peep] == "True":
                            print "    %s     %s" % (instance.state, instance.tags["Name"])
                            ips.append(instance.ip_address)

        try: 
            with open("%s" % self.ansible_host_file, "wb") as myfile:
                for ip in ips:
                    myfile.write("%s\r\n" % ip)

            print "\r\nUpdated %s with values pulled from EC2.\r\n" % (self.ansible_host_file)
        except Exception, e:
            print "You do not have write access to %s" % (self.ansible_host_file)
            self.print_ips(ips)
     
     
if  __name__ =='__main__':
    app = EC2ToAnsible()
    app.main()
