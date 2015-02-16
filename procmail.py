#! /usr/bin/python

import sys
import email
import re
import datetime
import meeting_invitation

def main():
    # http://stackoverflow.com/questions/14676375/pipe-email-from-procmail-to-python-script-that-parses-body-and-saves-as-text-fil
    full_msg = sys.stdin.read()

    msg = email.message_from_string(full_msg.strip());

    toAddr   = msg['To']
    fromAddr = msg['From']
    subject  = msg['Subject']

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

    # http://stackoverflow.com/questions/3368969/find-string-between-two-substrings
    confirmed = subject.find('confirmed')
    cancellation = subject.find('Cancellation')

    if confirmed:
        # print confirmed
        advisor = find_between( subject, "with ", " confirmed" )
        print "\'" + advisor + "\'"
        advisorClean = re.split(r', | ', advisor)
        # print advisorClean # ['McGrath', 'D', 'Kevin']
        # print "len(advisorClean): ", len(advisorClean)
        # for x in advisorClean: print x
        if len(advisorClean) == 3:
            advisorCleanName = advisorClean[2] + " " + advisorClean[0]
            print advisorCleanName
        elif len(advisorClean) == 2:
            advisorCleanName = advisorClean[1] + " " + advisorClean[0]
            print advisorCleanName

        advisorTest = find_between(body, "Advising Signup with ", " confirmed")
        print "advisorTest" + advisorTest

        forIndex = subject.find('for ')
        student = subject[(forIndex + len('for ')): len(subject)]
        # print student
        studentClean = re.split(r', | ', student)
        if len(studentClean) == 3:
            studentCleanName = studentClean[2] + " " + studentClean[0]
            print studentCleanName
        elif len(studentClean) == 2:
            studentCleanName = studentClean[1] + " " + studentClean[0]
            print studentCleanName
        method = "REQUEST"

    elif cancellation:
        print cancellation
        method = "CANCEL"
        advisorTest = find_between(body, "Advising Signup with ", " CANCELLED")
        print "advisorTest" + advisorTest
    else:
        print "No confirmed/Cancellation?!"

    # http://stackoverflow.com/questions/17874360/python-how-to-parse-the-body-from-a-raw-email-given-that-raw-email-does-not
    b = msg
    body = ""

    if msg.is_multipart():
        print "is multipart"

        for payload in msg.get_payload():
            body += payload.get_payload()
    else:
        print msg.get_payload()
        print "!is multipart"

    print "-------------------------------------------------------------------------------\n"
    print body
    print "-------------------------------------------------------------------------------\n"
    bodyPlainStart = body.find("Advising")
    bodyPlainEnd = body.find("problems")
    bodyPlain = body[bodyPlainStart:bodyPlainEnd + 8]
    print bodyPlain
    print "-------------------------------------------------------------------------------\n"

    dateStr = find_between( body, "day, ", "Time: " )
    print dateStr
    dateStr = re.sub(r"(,|st|nd|rd|th)", "", dateStr)
    print dateStr

    timeStr = find_between( body, "Time: ", " - " )
    print timeStr

    datetimeStr = dateStr + " " + timeStr
    datetimeStrP = datetime.datetime.strptime(datetimeStr, "%B %d %Y %I:%M%p")
    print datetimeStrP

    # uid = advisorCleanName + " " + str(datetimeStrP)
    # print uid

    # meeting_invitation.meeting_invitation(fromAddr, toAddr, bodyPlain, datetimeStrP, method, uid)

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
