#! /usr/bin/python

import sys
import email
import re
import datetime
# import meeting-invitation

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
    print fromAddr
    print subject

    # http://stackoverflow.com/questions/3368969/find-string-between-two-substrings
    # subject = "Advising Signup with McGrath, D Kevin confirmed for Brabham, Matthew Lawrence"
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
            print advisorClean[2], advisorClean[0]

        forIndex = subject.find('for ')
        student = subject[(forIndex + len('for ')): len(subject)]
        # print student
        studentClean = re.split(r', | ', student)
        if len(studentClean) == 3:
            print studentClean[2], studentClean[0]
    elif cancellation:
        print cancellation
    else:
        print "No confirmed/Cancellation?!"

    # http://stackoverflow.com/questions/17874360/python-how-to-parse-the-body-from-a-raw-email-given-that-raw-email-does-not
    b = msg
    body = ""

    if msg.is_multipart():
        print "is multipart"

        for payload in msg.get_payload():
            # if payload.is_multipart(): ...
            body += payload.get_payload()
    else:
        print msg.get_payload()
        print "!is multipart"

    print "-------------------------------------------------------------------------------\n"
    print body
    print "-------------------------------------------------------------------------------\n"
    dateStr = find_between( body, "day, ", "Time: " )
    print dateStr
    dateStr = re.sub(r"(,|st|nd|rd|th)", "", dateStr)
    print dateStr
    # dateStrP = datetime.datetime.strptime(dateStr, "%B %d %Y")
    # print dateStrP.strftime("%Y-%m-%d")
    #
    timeStr = find_between( body, "Time: ", " - " )
    print timeStr
    # timeStrP = datetime.datetime.strptime(timeStr, "%I:%M%p")
    # print timeStrP.strftime("%H-%M-%S")

    datetimeStr = dateStr + " " + timeStr
    datetimeStrP = datetime.datetime.strptime(datetimeStr, "%B %d %Y %I:%M%p")
    print datetimeStrP

    # def meeting_invitation(from, to, subject, body)

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

# http://stackoverflow.com/questions/11472442/grab-first-word-in-string-after-id
# text = 'Advising Signup with McGrath, D Kevin confirmed for Brabham, Matthew Lawrence'
# match = re.search(r'with (\w+\w+\w+)', text)
# if match:
#     print match.group(1) # McGrath
#
# words = text.split()
# try:
#     word = words[words.index("with") + 1]
#     print word # McGrath,
# except (ValueError, IndexError): word = ''


#
# def find_between_r( s, first, last ):
#     try:
#         start = s.rindex( first ) + len( first )
#         end = s.rindex( last, start )
#         return s[start:end]
#     except ValueError:
#         return ""
#
# print find_between_r( s, "with ", " confirmed" )