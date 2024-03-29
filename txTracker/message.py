import smtplib
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from email.mime.text import MIMEText
import logging
logging.basicConfig(level=logging.INFO)

signature = '\r\n\r\n\r\nThe Altme team.\r\nhttps://altme.io/'


def message(subject, to, messagetext, password) :

	fromaddr = "relay@talao.io"
	toaddr = [to]

	msg = MIMEMultipart()
	msg['From'] = formataddr((str(Header('Altme', 'utf-8')), fromaddr))
	msg['To'] = ", ".join(toaddr)
	msg['Subject'] =  subject
	body = messagetext + signature
	msg.attach(MIMEText(body, 'plain'))
	#p = MIMEBase('application', 'octet-stream')

	# creates SMTP session
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls()
	s.login(fromaddr, password)
	text = msg.as_string()

	# sending the mail
	try:
		s.sendmail(msg['from'],  msg["To"].split(","), text)
	except:
		logging.error('sending mail')
		return False
	s.quit()
	return True


