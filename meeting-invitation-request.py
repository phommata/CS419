# http://stackoverflow.com/questions/4823574/sending-meeting-invitations-with-python
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import os,datetime

# def meeting_invitation(adviserName, studentName, from, to, subject, datetimeStr):
CRLF = "\r\n"
# login = ""
# password = ""
# attendees = ["phommata@engr.orst.edu"] # @engr.orst.edu does not work
attendees = ["phommata@onid.oregonstate.edu"]
organizer = "ORGANIZER;CN=organiser:mailto:do.not.reply"+CRLF+" @engr.orst.edu"
fro = "<do.not.reply@engr.orst.edu>"

ddtstart = datetime.datetime.now()
dtoff = datetime.timedelta(days = 1)
dur = datetime.timedelta(hours = 1)
dur = datetime.timedelta(minutes = 1)
ddtstart = ddtstart + dtoff
dtend = ddtstart + dur
dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
dtstart = ddtstart.strftime("%Y%m%dT%H%M%SZ")
dtend = dtend.strftime("%Y%m%dT%H%M%SZ")

description = "DESCRIPTION: test invitation from pyICSParser"+CRLF
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
ical+="METHOD:REQUEST"+CRLF+\
      "BEGIN:VEVENT"+CRLF+\
      "DTSTART:"+dtstart+CRLF+\
      "DTEND:"+dtend+CRLF+\
      "DTSTAMP:"+dtstamp+CRLF+organizer+CRLF
# ical+= "UID:FIXMEUID"+dtstamp+CRLF
ical+= "UID:Kevin D McGrath"+CRLF
ical+= attendee+\
       "CREATED:"+dtstamp+CRLF+\
       description+\
       "LAST-MODIFIED:"+dtstamp+CRLF+\
       "LOCATION:"+CRLF+\
       "SEQUENCE:0"+CRLF+\
       "STATUS:CONFIRMED"+CRLF
ical+= "SUMMARY:test "+ddtstart.strftime("%Y%m%d @ %H:%M")+CRLF+\
       "TRANSP:OPAQUE"+CRLF+\
       "END:VEVENT"+CRLF+\
       "END:VCALENDAR"+CRLF

eml_body = "Advising Signup with McGrath, D Kevin confirmed\r\n" \
           "Name: REDACTED\r\n" \
           "Email: REDACT@engr.orst.edu\r\n" \
           "Date: Wednesday, November 21st, 2012\r\n" \
           "Time: 1:00pm - 1:15pm\r\n\r\n" \
           "Please contact support@engr.oregonstate.edu if you experience problems"
eml_body_bin = "This is the email body in binary - two steps"
msg = MIMEMultipart('mixed')
msg['Reply-To']=fro
msg['Date'] = formatdate(localtime=True)
msg['Subject'] = "Advising Signup with McGrath, D Kevin confirmed for Brabham, Matthew Lawrence " #+ dtstart
msg['From'] = fro
msg['To'] = ",".join(attendees)

part_email = MIMEText(eml_body,"html")
part_cal = MIMEText(ical,'calendar;method=REQUEST')

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

# mailServer = smtplib.SMTP('smtp.gmail.com', 587)
mailServer = smtplib.SMTP('mail.engr.oregonstate.edu', 587)
# mailServer.ehlo()
# mailServer.starttls()
# mailServer.ehlo()
# mailServer.login(login, password)
mailServer.sendmail(fro, attendees, msg.as_string())
mailServer.close()