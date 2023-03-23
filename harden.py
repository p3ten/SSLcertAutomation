#! /usr/bin/python3
import subprocess

# Prompt user to enter the domain name
domain_name = input("Please enter your domain name: ")

# Install and configure SSL/TLS using Certbot
subprocess.run(["apt-get", "update"])
subprocess.run(["apt-get", "install", "-y", "certbot"])
subprocess.run(["certbot", "certonly", "--standalone", "-d", domain_name])

# Set "secure" and "httponly" attributes on session cookies
with open("/etc/apache2/conf-available/security.conf", "a") as f:
    f.write("Header edit Set-Cookie ^(.*)$ $1;HttpOnly;Secure\n")

# Set session timeout value
with open("/etc/php/7.4/apache2/php.ini", "a") as f:
    f.write("session.gc_maxlifetime = 1800\n")

# Generate new session ID and regenerate session ID after login and privilege level changes
with open("/var/www/html/login.php", "a") as f:
    f.write("session_regenerate_id(true);\n")
with open("/var/www/html/privilege_change.php", "a") as f:
    f.write("session_regenerate_id(true);\n")

# Store session data securely outside the webroot directory
with open("/etc/php/7.4/apache2/php.ini", "a") as f:
    f.write("session.save_path = /var/lib/php/sessions\n")
