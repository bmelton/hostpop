Hostpop
#######

Usage: 
------
    
    # If not already done
    export AWS_ACCESS_KEY="Your Access Key"
    export AWS_SECRET_KEY="Your Secret Key"

    python pop.py

    Pop will query EC2 instances within the us-east-1 region for all instances
    with the tag 'Ansible=True' and create an /etc/ansible/hosts file with all
    of their IPs.  

    If you have write access to the file (danger) then it will write the file 
    directly.  If you do not have write access to the file (safe), it will just
    output the IPs that need to be added, and you can copy/paste them in 
    manually
