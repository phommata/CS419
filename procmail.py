import sys
import email
import re
import datetime
import meeting_invitation
import meeting_invitation_test

def main():
    # http://stackoverflow.com/questions/14676375/pipe-email-from-procmail-to-python-script-that-parses-body-and-saves-as-text-fil
    # Read from command line
    full_msg = sys.stdin.read()

    msg = email.message_from_string(full_msg.strip());

    # Parse email
    toAddr   = msg['To']
    fromAddr = msg['From']
    subject  = msg['Subject']

    # Debug print statements: $HOME/mail/logfile.txt
    outfile = open("logfile.txt", 'w')
    sys.stdout = outfile
    print full_msg
    print "-------------------------------------------------------------------------------\n"
    print msg
    print "-------------------------------------------------------------------------------\n"

    print toAddr
    toAddr = re.split(r',', toAddr)
    print toAddr
    print fromAddr
    print subject

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
        studentCleanName = studentClean[len(studentClean) - 1] + " " + studentClean[0]
        print studentCleanName

        # Set meeting invitation method
        method = "REQUEST"
    elif cancellation > 0:
        # Parse Advisor FirstName LastName
        advisor = find_between( body, "Advising Signup with ", " CANCELLED" )
        print "advisor CANCELLED " + advisor
        advisorClean = re.split(r', | ', advisor)
        advisorCleanName = advisorClean[len(advisorClean) - 1] + " " + advisorClean[0]
        print advisorCleanName

        # Parse Student FirstName LastName
        student = find_between( body, "Name: ", "Email:" )
        print "student CANCELLED " + student
        studentClean = re.split(r', | ', student)
        studentCleanName = studentClean[len(studentClean) - 1] + " " + studentClean[0]
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
    meeting_invitation.meeting_invitation(toAddr, bodyPlain, datetimeStrP, method, uid)
    # meeting_invitation_test.meeting_invitation(toAddr, bodyPlain, datetimeStrP, method, uid)

    outfile.close()

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end].strip()
    except ValueError:
        return ""

if __name__ == '__main__':     # if the function is the main function ...
    main() # ...call it
