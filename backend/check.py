from gmail_smtplib_micro import GmailSMTPLib, Email

subject = "The string of the subject"
body = "This is the body of the email\nIncluding line breaks"

e = Email(subject, body)

g = GmailSMTPLib("email.conf")
g.send_object(e,"22052517@kiit.ac.in")