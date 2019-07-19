import datetime
import smtplib

# Use the following table for popular carriers:
# T-Mobile: phonenumber@tmomail.net
# Virgin Mobile: phonenumber@vmobl.com
# Cingular: phonenumber@cingularme.com
# Sprint: phonenumber@messaging.sprintpcs.com
# Verizon: phonenumber@vtext.com
# Nextel: phonenumber@messaging.nextel.com
# AT&T: phonenumber@txt.att.net
# SPRINT NEXTEL pagenumber@page.nextel.com
# where phonenumber = your 10 digit phone number
# For ORNL accounts it is sufficient the 3-digit letters


def EmailAlert():
    SERVER = "160.91.4.26"
    FROM = "CNCS@ornl.gov"
    TO = ["gqs@ornl.gov","ewf@ornl.gov"]#"8654566395@txt.att.net"] must be a list

    SUBJECT = "Alarm from CNCS BL-5"
    TIME = str(datetime.datetime.now())
    TEXT = "This is CNCS, BL-5 at ORNL.\n One of my scan alarm triggered at: {0}\n Please contact IMMEDIATELY the Hall Coordinator !!!".format(TIME)

    # Prepare actual message
    message = """From: %s\r\nTo: %s\r\nSubject: %s\r\n\n
    
    %s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    # Send the mail
    server = smtplib.SMTP(SERVER)
    server.sendmail(FROM, TO, message)
    server.quit()

    print("Humans notified at: {0}".format(TIME))









