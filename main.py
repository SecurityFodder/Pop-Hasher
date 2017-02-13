#! /bin/python2

'''
I'll explain it after I've figured out what I'm doing
'''

import requests
import poplib
import hashlib
import os

today = date.isoformat(date.today())
working_folder = '/store/popHasher/' + today + '_mail_Attachments/'

if os.path.exists(todays_folder):
    os.mkdir(todays_folder)

#Mail server settings
def mail_connection(server=pop.mymailserver.com):
    pop_conn = poplib.POP3(server)
    pop_conn.user('someuser@server')
    pop_conn.pass_('password')
    return pop_conn

#Download list of mail
def fetch_mail(delete_after=False):
    pop_conn = mail_connection()
    messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
    messages = ["\n".join(mssg[1]) for mssg in messages]
    messages = [parser.Parser().parsestr(mssg) for mssg in messages]
    if delete_after == True:
        delete_messages = [pop_conn.dele(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
    pop_conn.quit()
    return messages

#get attachments from emails - save to working folder
def get_attachments():
    messages = fetch_mail()
    attachments = []
    for msg in messages:
        for part in msg.walk():
            name = part.get_filename()
            data = part.get_payload(decode=True)
            f = file(name,'wb')
            f.write(data)
            f.close()
            attachments.append(name)
    return attachments

#hash each file 3 times, then add to dict
def hash_files():
    hash_dict = {}
    fetched_attachments  = get_attachments()
    for attachment in fetched_attachments:
        name = attachment
        location = todays_folder + name
        md5 = hashlib.md5(open(location, 'rb').read()).hexdigest()
        sha1 = hashlib.sha1(open(location, 'rb').read()).hexdigest()
        sha256 = hashlib.sha256(open(location, 'rb').read()).hexdigest()
        fetched_attachments = { 'md5': md5,
                                'sha1': sha1,
                                'sha256': sha256 }
        hash_dict[name] = fetched_attachments
    return hash_dict

#this is the bit where I'll 


