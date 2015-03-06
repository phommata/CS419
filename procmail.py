import sys
import email
import re
import datetime
import meeting_invitation
import meeting_invitation_test
import MySQLdb

db = MySQLdb.connect("mysql.eecs.oregonstate.edu", "cs419-g6", "group6data", "cs419-g6")
cursor = db.cursor()

def main():
    # http://stackoverflow.com/questions/14676375/pipe-email-from-procmail-to-python-script-that-parses-body-and-saves-as-text-fil
    # Read from command line
    full_msg = sys.stdin.read()

    msg = email.message_from_string(full_msg.strip());

    # Parse email
    toAddrOrig   = msg['To'].strip()
    fromAddr = msg['From']
    subject  = msg['Subject']

    # Debug print statements: $HOME/mail/logfile.txt
    outfile = open("logfile.txt", 'w')
    sys.stdout = outfile
    print full_msg
    print "-------------------------------------------------------------------------------\n"
    print msg
    print "-------------------------------------------------------------------------------\n"

    # Adviser's e-mail
    print 'toAddr: ' + toAddrOrig
    toAddr = find_between_r(toAddrOrig, ',', '.edu')
    toAddr = toAddr.strip()
    print 'toAddr: ' + toAddr

    toAddrTuple = re.split(r',', toAddrOrig)
    print 'toAddrTuple: ' + str(toAddrTuple)
    print 'fromAddr: ' + fromAddr
    print 'subject: ' + subject

    # http://stackoverflow.com/questions/17874360/python-how-to-parse-the-body-from-a-raw-email-given-that-raw-email-does-not
    body = ""

    if msg.is_multipart():
        print "is multipart"

        for payload in msg.get_payload():
            body += payload.get_payload()
    else:
        print msg.get_payload()
        print "!is multipart"
        body = msg.get_payload()

    print "-------------------------------------------------------------------------------\n"
    print body
    print "-------------------------------------------------------------------------------\n"
    # Parse body plain text
    bodyPlainStart = body.find("Advising")
    bodyPlainEnd = body.find("problems")
    bodyPlain = body[bodyPlainStart:bodyPlainEnd + 8]
    print bodyPlain
    print "-------------------------------------------------------------------------------\n"

    confirmed = body.find('confirmed')
    cancellation = body.find('CANCELLED')

    if confirmed > 0:
        # http://stackoverflow.com/questions/3368969/find-string-between-two-substrings
        # Parse Advisor FirstName LastName
        advisor = find_between( body, "Advising Signup with ", " confirmed" )
        print "advisor confirmed " + advisor
        advisorClean = re.split(r', | ', advisor)
        advisorCleanName = advisorClean[len(advisorClean) - 1] + " " + advisorClean[0]
        print advisorCleanName

        # Parse Student FirstName LastName
        student = find_between( body, "Name: ", "Email:" )
        print "student confirmed " + student
        studentClean = re.split(r', | ', student)
        studentCleanName = studentClean[1] + " " + studentClean[0]
        print studentCleanName

        # Set meeting invitation method
        method = "REQUEST"
    elif cancellation > 0:
        # Parse Advisor FirstName LastName
        advisor = find_between( body, "Advising Signup with ", " CANCELLED" )
        print "advisor CANCELLED " + advisor
        advisorClean = re.split(r', | ', advisor)
        advisorCleanName = advisorClean[1] + " " + advisorClean[0]
        print advisorCleanName

        # Parse Student FirstName LastName
        student = find_between( body, "Name: ", "Email:" )
        print "student CANCELLED " + student
        studentClean = re.split(r', | ', student)
        studentCleanName = studentClean[1] + " " + studentClean[0]
        print studentCleanName

        # Set meeting invitation method
        method = "CANCEL"
    else:
        print "No confirmed/CANCELLED in body?!"

    # Parse date
    dateStr = find_between( body, "day, ", "Time: " )
    print dateStr
    dateStr = re.sub(r"(,|st|nd|rd|th)", "", dateStr)
    print dateStr

    # Parse start time
    timeStr = find_between( body, "Time: ", " - " )
    print timeStr

    # Parse datetime
    datetimeStr = dateStr + " " + timeStr
    datetimeStrP = datetime.datetime.strptime(datetimeStr, "%B %d %Y %I:%M%p")
    print datetimeStrP # Datetime format for db "YYYY-MM-DD HH:MM:SS"

    # Create UID for meeting invitation
    uid = advisorCleanName + " " + str(datetimeStrP)
    print uid

    # Pass args to meeting_invitation email
    meeting_invitation.meeting_invitation(toAddrTuple, bodyPlain, datetimeStrP, method, uid)
    # meeting_invitation_test.meeting_invitation(toAddr, bodyPlain, datetimeStrP, method, uid)

    # If appointment confirmation, add to database. Else if cancellation, remove from database
    if confirmed > 0:
        addToDatabase(advisorCleanName, studentCleanName, toAddr, fromAddr, datetimeStrP)
    elif cancellation > 0:
		removeFromDatabase(toAddr, fromAddr, datetimeStrP)
	
    cursor.close()
    outfile.close()

def addToDatabase(advisorCleanName, studentCleanName, toAddr, fromAddr, datetimeStrP):
    add_meeting = ("INSERT INTO advising_schedule (ad_name, st_name, ad_email, st_email, date_time) VALUES (%s, %s, %s, %s, %s)")
    meeting_details = (advisorCleanName, studentCleanName, toAddr, fromAddr, datetimeStrP)
    cursor.execute(add_meeting, meeting_details)

def removeFromDatabase(toAddr, fromAddr, datetimeStrP):
    remove_meeting = ("DELETE FROM advising_schedule WHERE ad_email = %s AND st_email = %s AND date_time = %s")
    meeting_details = (toAddr, fromAddr, datetimeStrP)
    cursor.execute(remove_meeting, meeting_details)

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end].strip()
    except ValueError:
        return ""

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        # end = s.rindex( last, start )
        return s[start:len(s)]
    except ValueError:
        return ""

if __name__ == '__main__':     # if the function is the main function ...
    main() # ...call it
