#!/usr/bin/python
# -*- coding: UTF-8 -*-
##
# Exchange configuration script for 10.6 & 10.7
#
# Will configure Mail.app, AddressBook & iCal with our Exchange server using the native Exchange support in 10.6 (EWS)
#
# Runs if the following paths doesnt exists (so if you want to re-setup for example iCal, delete the folders/files below)
#
# iCal:			~/Library/Calendars/*.exchange
#				~/Library/Calendars/Calendar Cache
# AddressBook:	~/Library/Application Support/AddressBook/Sources/
# Mail:			~/Library/Preferences/com.apple.mail.plist
#
# Update varibles "templatesDir", "ExchangeServerInfo" and function "getUserData" to suite your own environemt.
#
# Run script as the logged in user "./mailSetupEWS.py" to setup Mail, iCal & AddressBook.app
#
#	
# 2012-05-09	daniel.svensson3@ikea.com 	1.0 Public version.
#

try:
	import os, sqlite3, sys, shutil, plistlib, re
except Exception, error:
	print "Error, missing required modules: " + str(error)
	sys.exit()

######### SETTINGS #########
## Get info about our user
homedir = os.popen('echo $HOME').readline().strip('\n')
loggedInUser = os.popen('whoami').readline().strip('\n')
adSearchPath = os.popen('dscl /Search -read / CSPSearchPath | grep \"Active Directory\"').readline().strip('\n').strip()
shortname = os.popen('dscl "' + adSearchPath + '" -read /Users/' + loggedInUser + ' sAMAccountName | cut -d \' \' -f 2').readline().strip('\n').strip()

# What are we running on
os_version = os.popen("/usr/bin/sw_vers | grep ProductVersion | cut -f 2 -d :").readline().strip('\n\t')

# this is where we store info about the user
UserData = {}

#########################################################
#### Update for your own environment

## copy the templates from here
templatesDir = "/Library/Management/mail-setup-ews-1.0/templates"
logString = "no.hioa.mailSetup {" + loggedInUser + "} ";

### Exchange server
ExchangeServerInfo = {}
ExchangeServerInfo['fqdn'] 			= ""
ExchangeServerInfo['serverRootPath']	= "/EWS/Exchange.asmx"
ExchangeServerInfo['EWS url'] 		= "https://" + str(ExchangeServerInfo['fqdn']) + ExchangeServerInfo['serverRootPath']


##### end here
#########################################################

## By default we should setup all apps
setupiCal = True
setupAddressBook = True
setupMail = True

### iCal settings
# Path and name of plist to create
iCalBasePath	= "/Library/Calendars/"
iCalPlist_template	= templatesDir + '/iCal_template.plist'
iCalDB_template		= templatesDir + '/iCalDB_template'

### AddressBook settings
AddressBookBasePath = "/Library/Application Support/AddressBook/Sources/"
AddressBook_template = templatesDir + '/AddressBook_template.plist'

### Mail.app settings
## If we are running on anything but 10.6 or 10.7, exit.
if(os_version.find("10.7") != -1):
	Mail_template	= templatesDir + '/Mail_template10.7.plist'
	MailPlist		=  "/Library/Mail/V2/MailData/Accounts.plist"

elif(os_version.find("10.6") != -1):
	Mail_template	= templatesDir + '/Mail_template.plist'
	MailPlist		=  "/Library/Preferences/com.apple.mail.plist"
	
else:
	sys.exit("[ERROR] Unsupported OS version")


######### END OF SETTINGS #########

######### Functions 
def logger(msg):
	
	global logString
	
	# Send the msg to /usr/bin/logger
	os.popen("/usr/bin/logger \"" + logString + str(msg) + "\"")
	
	return
	
def getUserData(shortname, homedir):
	
	global adSearchPath, loggedInUser
	
	# Try to retrive the mail adress this user
	try:

#########################################################
# Insert code here to get users email address


		_email = os.popen('dscl "' + adSearchPath + '" -read /Users/' + loggedInUser + ' EMailAddress | cut -d \' \' -f 2').readline().strip('\n').strip()
                _fullname = os.popen('dscl "' + adSearchPath + '" -read /Users/' + loggedInUser + ' RealName | grep -v \"RealName\"').readline().strip('\n').strip()	
                _fullname = unicode((_fullname),"utf-8")
# end
#########################################################

	except Exception, error:
		logger("[ERROR " +str(error))
		
	if(re.search('@', _email)):
		# Yepp, this seems to be a mail adress
		UserData['email'] = _email
	else:
		logger('[ERROR] Could not find a valid email adress for ' + str(loggedInUser))
		sys.exit('[ERROR] Could not find a valid email adress for ' + str(loggedInUser))
		
	if(_fullname != ""):
		# Yepp, this seems to be a mail adress
		UserData['fullname'] = _fullname
	else:
		logger('[ERROR] Could not find full name for ' + str(loggedInUser))
		sys.exit('[ERROR] Could not find full name for ' + str(loggedInUser))
	
	# Genereate a GUID to use for this account. Use the same in all applications for brevity
	UserData['uuid']		= os.popen('uuidgen').readline().strip('\n')
	UserData['homedir']		= homedir
	UserData['shortname']	= shortname
	
	#print("Found this info for the user:\n" + str(UserData))
	return UserData

def configureiCal(iCalBasePath, UserData):
	
	global iCalPlist_template, ExchangeServerInfo
	
	# Settings 
	iCalPlist		= iCalBasePath + UserData['uuid'] + ".exchange/Info.plist"
	iCalDB			= iCalBasePath + "Calendar Cache"

	# Read in the template
	try:
		_data	= plistlib.readPlist(iCalPlist_template)
	except Exception, error:
		logger("[ERROR] Could not read " + str(iCalPlist_template))
		sys.exit("[ERROR] Could not read " + str(iCalPlist_template))
	
	# Replace with info for the running user
	_data['Title'] 					= UserData['email']
	_data['Login']					= UserData['shortname']
	_data['CalendarUserAddresses'] 	= ["mailto:" + UserData['email']]
	_data['ServerURL'] 				= ExchangeServerInfo['EWS url']
	_data['Mailbox']				= UserData['email']
	_data['FullName'] 				= UserData['fullname']
	_data['Key']					= UserData['uuid']

	_sql = ['INSERT INTO "ZACCOUNT" VALUES(NULL,3,1,900,NULL,NULL,1,"' + _data['Login'] + '","' + _data['ServerURL'] + '",NULL,NULL,NULL);',
	'''INSERT INTO "ZNODE" VALUES(NULL,38,1,1,3,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,
	NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,0,1,3,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,
	NULL,NULL,"''' + UserData['uuid'] + '''",NULL,"''' + _data['Mailbox'] + '''","#808080FF",
	NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,"''' + _data['FullName'] + '''",NULL,NULL,NULL,NULL,
	NULL,NULL,NULL,NULL,NULL,NULL,NULL,"''' + _data['Mailbox'] + '''",NULL);''']

	
	# Create the destination directories if the doesnt exist
	try:
		if(not os.path.exists(os.path.dirname(iCalPlist))):
			os.makedirs(os.path.dirname(iCalPlist))
	except Exception, error:
		logger("[ERROR] Could create directory " + str(os.path.dirname(iCalPlist)))
		sys.exit("[ERROR] Could create directory " + str(os.path.dirname(iCalPlist)))
		
	# Write out the finished plist	
	try:
		plistlib.writePlist(_data, iCalPlist)
	except Exception, error:
		logger("[ERROR] Could not write plist for iCal")
		sys.exit("[ERROR] Could not write plist for iCal")

	# Continue with the Calendar Cache
	# If it doesnt exist, use our template
	if(not os.path.exists(iCalDB)):
		try:
			shutil.copy(iCalDB_template, iCalDB)
		except Exception, error:
			logger("[ERROR] Could not copy the Calendar Cache template")
			sys.exit("[ERROR] Could not copy the Calendar Cache template")

	
	# Open the database and run the SQL-insert code
	try:
		connection = sqlite3.connect(iCalDB)
		cursor = connection.cursor()
		
		for sqlInsert in _sql:
			data = cursor.execute(sqlInsert)
		
	except sqlite3.OperationalError:
		# Ooops, looks like we tried to write into a newer version of the calendar cache file.
		# Let's rename it and use our default cache instead

		connection.close()
		
		try:
			os.rename(iCalDB, str(iCalDB+".old"))	
			shutil.copy(iCalDB_template, iCalDB)
			
		except Exception, error:
			logger("[ERROR] Could not copy the Calendar Cache template")
			sys.exit("[ERROR] Could not copy the Calendar Cache template")
			
		# Ok, let's try again!
		
		connection = sqlite3.connect(iCalDB)
		cursor = connection.cursor()

		for sqlInsert in _sql:
			data = cursor.execute(sqlInsert)

	except Exception, error:
		logger("[ERROR] Could read or write the Calendar Cache database")
		sys.exit("[ERROR] Could read or write the Calendar Cache database, got this error: \"" + str(error) + "\"")

	finally:
		
		# Make sure to commit and close the DB
		connection.commit()
		connection.close()
		
	return

def configureAddressBook(AddressBookBasePath, UserData):
	global AddressBook_template, ExchangeServerInfo

	# Setup 
	AddressBookPlist = AddressBookBasePath + UserData['uuid'] + "/Configuration.plist"

	# Read in the template
	try:
		_data = plistlib.readPlist(AddressBook_template)
	except Exception, error:
		logger("[ERROR] Could not read " + str(AddressBook_template))
		sys.exit("[ERROR] Could not read " + str(AddressBook_template))

	# Replace with info for the running user
	_data['emailAddress'] 	= UserData['email']
	_data['name']			= UserData['email']
	_data['fullName'] 		= UserData['fullname']
	_data['userName']		= UserData['shortname']
	_data['serverRootPath']	= ExchangeServerInfo['serverRootPath']
	_data['serverName'] 	= ExchangeServerInfo['fqdn']

	# Create the destination directories if the doesnt exist
	try:
		if(not os.path.exists(os.path.dirname(AddressBookPlist))):
			os.makedirs(os.path.dirname(AddressBookPlist))
	except Exception, error:
		logger("[ERROR] Could create directory " + str(os.path.dirname(AddressBookPlist)))
		sys.exit("[ERROR] Could create directory " + str(os.path.dirname(AddressBookPlist)))

	try:
		# Write out the finished plist	
		plistlib.writePlist(_data, AddressBookPlist)

	except Exception, error:
		logger("[ERROR] Error writing the AddressBookPlist")
		sys.exit("[ERROR] Error writing the AddressBookPlist, got this error: \"" + str(error) + "\"")

		
	return

def configureMail(MailPlist, UserData):
	global Mail_template, ExchangeServerInfo, os_version

	# Read in the template
	try:
		_data	= plistlib.readPlist(Mail_template)
	except Exception, error:
		logger("[ERROR] Could not read " + str(Mail_template))
		sys.exit("[ERROR] Could not read " + str(Mail_template))

	for Account in _data['MailAccounts']:
		# Replace the necessary keys with info about our running user
	
		if(os_version.find("10.7") != -1):
			Account['AccountPath']				= "~/Library/Mail/V2/EWS-" + UserData['shortname'] + "@" + ExchangeServerInfo['fqdn']

		elif(os_version.find("10.6") != -1):
			Account['AccountPath']				= "~/Library/Mail/EWS-" + UserData['shortname'] + "@" + ExchangeServerInfo['fqdn']
		
		Account['AccountName'] 				= UserData['email']
		Account['EmailAddresses'] 			= [UserData['email']]
		Account['FullUserName'] 				= UserData['fullname']
		Account['Username']					= UserData['shortname']
		Account['uniqueId']					= UserData['uuid']
		Account['ToDosCalendarsGroupUID']	= [UserData['email']]
		Account['InternalServerPath']		= ExchangeServerInfo['serverRootPath']
		Account['Hostname'] 				= ExchangeServerInfo['fqdn']
	
	# Save our new Account into the plist
	_data['MailAccounts'] == [Account]
	
	# Test our destination path before writing to disk
	if not (os.path.exists(os.path.dirname(MailPlist))):
		try:
			os.popen("mkdir -p " + os.path.dirname(MailPlist))
		except Exception, error:
			logger("[ERROR] Could not create " + os.path.dirname(MailPlist))
			sys.exit("[ERROR] Could not create " + os.path.dirname(MailPlist) + ", got this error: \"" + str(error) + "\"")
			
	try:
		# Write out the finished plist	
		plistlib.writePlist(_data, MailPlist)

	except Exception, error:
		logger("[ERROR] Error writing the Mail.plist")
		sys.exit("[ERROR] Error writing the Mail.plist, got this error: \"" + str(error) + "\"")
		
	return

############ MAIN SCRIPT ############


###### Check iCal ######
# Unless we find a directory in ~/Library/Calendars/ that ends with .exchange we setup iCal
try:
	for folder in os.listdir(homedir + iCalBasePath):
		if folder.endswith(".exchange"):
			# Set to False since there already seems to be a exchange config for iCal
			setupiCal = False
except:
	# The ~/Library/Calendars/ doesnt exists, probably because someone deleted it so let's re-setup iCal
	setupiCal = True

###### Check AddressBook ######
# If we dont find '~/Library/Application Support/AddressBook/Sources' we setup AddressBook
setupAddressBook = True
if(os.path.exists(homedir + AddressBookBasePath)):
	setupAddressBook = False

###### Check Mail.app ######
# If ~/Library/Preferences/com.apple.Mail.plist doesnt exis we setup Mail.app
if(os.path.exists(homedir + MailPlist)):
	setupMail = False

### If we need to setup any of the applications, go ahead and query CDS & AD for more user info. If not, just quit
if(setupiCal or setupAddressBook or setupMail):
	UserData = getUserData(shortname, homedir)

	if(setupiCal):
		logger("[INFO] Setting up Exchange support in iCal")
		configureiCal(UserData['homedir'] + iCalBasePath, UserData)
	else:
		logger("[SKIPPING] iCal already configured")
	
	if(setupAddressBook):
		logger("[INFO] Setting up Exchange support in AddressBook")
		configureAddressBook(UserData['homedir'] + AddressBookBasePath, UserData)
	else:
		logger("[SKIPPING] AddressBook already configured")
	
	if(setupMail):
		logger("[INFO] Setting up Exchange support in Mail.app")
		configureMail(UserData['homedir'] + MailPlist, UserData)
	else:
		logger("[SKIPPING] Mail.app already configured")
else:
	logger("[INFO] Exchange support already setup")
############ END OF SCRIPT ############
