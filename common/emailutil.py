# -*- coding: utf-8 -*-

from email.MIMEText import MIMEText
from email.Utils import formatdate
from email.Header import Header
import smtplib

class EmailUtil(object):
    encoding  = 'ISO-2022-JP'

    def _getFrom(self, from_addr, sender):
        self.mailfrom  = u"%s <%s>" % (str(Header(sender, self.encoding)), from_addr)
        return self.mailfrom

    def create_message(self, to_addr, from_addr, sender, subject, body, cc_addr = None):
        msg = MIMEText(body.encode(self.encoding, 'replace'), 'plain', self.encoding)
        msg['To'] = to_addr
        msg['From'] = self._getFrom(from_addr, sender)
        msg['Subject'] = Header(subject, self.encoding)
        msg['Date'] = formatdate()

        # http://stackoverflow.com/questions/1546367/python-how-to-send-mail-with-to-cc-and-bcc
        if cc_addr:
            msg['Cc'] = cc_addr

        return msg

    def send(self, to_addr, msg, cc_addr = None):
        s = smtplib.SMTP()
        s.connect()

        if cc_addr is None:
            to = to_addr
        else:
            to = [to_addr] + [cc_addr]

        s.sendmail(self.mailfrom, to, msg.as_string())
        s.close()

