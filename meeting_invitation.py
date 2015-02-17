# http://stackoverflow.com/questions/4823574/sending-meeting-invitations-with-python
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import os,datetime,time

def meeting_invitation(fromAddr, toAddr, body, datetimeStrP, method, uid):
    CRLF = "\r\n"
    # attendees = ['phommata <phommata@engr.orst.edu>', '\n        Andrew Phommathep <13destinies@gmail.com>']
    attendees = toAddr # takes a tuple
    organizer = "ORGANIZER;CN=organiser:mailto:do.not.reply"+CRLF+" @engr.orst.edu"
    fro = "<do.not.reply@engr.orst.edu>"

    ddtstart = datetimeStrP
    dtoff = datetime.timedelta(hours = 8) # Correct -8 hour UTC offset correction
    dur = datetime.timedelta(minutes = 15)
    ddtstart = ddtstart + dtoff
    dtend = ddtstart + dur
    dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    dtstart = ddtstart.strftime("%Y%m%dT%H%M%SZ")
    dtend = dtend.strftime("%Y%m%dT%H%M%SZ")

    if method == "REQUEST":
        status = "REQUEST"
    elif method == "CANCEL":
        status = "CANCELLED"

    description = "DESCRIPTION: " + body +CRLF
    attendee = ""
    for att in attendees:
        attendee += "ATTENDEE;CUTYPE=INDIVIDUAL;" \
                    "ROLE=REQ-PARTICIPANT;" \
                    "PARTSTAT=ACCEPTED;" \
                    "RSVP=TRUE"+CRLF+" ;" \
                    "CN="+att+";" \
                    "X-NUM-GUESTS=0:"+CRLF+" " \
                    "mailto:"+att+CRLF
    ical = "BEGIN:VCALENDAR"+CRLF+\
           "PRODID:pyICSParser"+CRLF+\
           "VERSION:2.0"+CRLF+\
           "CALSCALE:GREGORIAN"+CRLF
    ical+= "METHOD:"+ method + CRLF+\
          "BEGIN:VEVENT"+CRLF+\
          "DTSTART:"+dtstart+CRLF+\
          "DTEND:"+dtend+CRLF+\
          "DTSTAMP:"+dtstamp+CRLF+organizer+CRLF
    # UID: Adviser name + " " + date_time
    ical+= "UID:"+ uid + CRLF
    ical+= attendee+\
           "CREATED:"+dtstamp+CRLF+\
           description+\
           "LAST-MODIFIED:"+dtstamp+CRLF+\
           "LOCATION:"+CRLF+\
           "SEQUENCE:0"+CRLF+\
           "STATUS:"+status+CRLF
    ical+= "SUMMARY: Advising Meeting " + method + CRLF+\
           "TRANSP:OPAQUE"+CRLF+\
           "END:VEVENT"+CRLF+\
           "END:VCALENDAR"+CRLF

    eml_body = body
    msg = MIMEMultipart('mixed')
    msg['Reply-To']=fro
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "Advising Meeting " + status
    msg['From'] = fro
    msg['To'] = ",".join(attendees)

    # http://stackoverflow.com/questions/10295530/how-to-set-a-charset-in-email-using-smtplib-in-python-2-7
    part_email = MIMEText(eml_body,"plain")
    part_cal = MIMEText(ical,'calendar;method=' + method)

    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)

    ical_atch = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
    ical_atch.set_payload(ical)
    Encoders.encode_base64(ical_atch)
    ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))

    eml_atch = MIMEBase('text/plain','')
    Encoders.encode_base64(eml_atch)
    eml_atch.add_header('Content-Transfer-Encoding', "")

    msgAlternative.attach(part_email)
    msgAlternative.attach(part_cal)

    mailServer = smtplib.SMTP('mail.engr.oregonstate.edu', 587)
    mailServer.sendmail(fro, attendees, msg.as_string())
    mailServer.close()
