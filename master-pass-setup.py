import keyring as kr
import getpass

ics_sys = 'ICS'
user = input('Add Username:\n')

kr.set_password(ics_sys, user, getpass.getpass())
print('PASSWORD WAS SET SUCCESSFULLY.')
