#!/bin/bash
defaults="/usr/bin/defaults"
PlistBuddy="/usr/libexec/PlistBuddy"
dockutil="/usr/local/bin/dockutil"
# Checks if script has ran before 
if [ ! -f $HOME/Library/Preferences/.OfficePrefsSetupDone ]
then
echo "bla"
# Find current user
UserName=`whoami`
Org="Your Organization"
# Check OS X version
sw_version=`sw_vers -productVersion | cut -d . -f 2,2`
# Check if /Library/Management/ada.hioa.no exist, else exit (Requires package ad_check)
if [ -f /Library/Management/ada.hioa.no ]
then
# Continue if OS X is 10.7 or newer
if [ "${sw_version}" -ge "7" ]; then
echo "${sw_version}"
# Get data from Active Directory
# e-mail
Email=`dscl /Active\\ Directory/ADA/All\\ Domains -read /Users/$UserName | grep -m1 EMailAddress | awk '{ print $2 }'`
Fullname=`dscl /Active\\ Directory/ADA/All\\ Domains -read /Users/$UserName | grep -A1 "RealName" | grep -v "RealName"`
FirstName=`dscl /Active\\ Directory/ADA/All\\ Domains -read /Users/$UserName | grep -A1 "RealName" | grep -v "RealName" | rev | cut -d ' ' -f2- | rev`
LastName=`dscl /Active\\ Directory/ADA/All\\ Domains -read /Users/$UserName | grep -A1 "RealName" | grep -v "RealName" | awk -F ' ' '{print $NF}'`
Initials=`dscl /Active\\ Directory/ADA/All\\ Domains -read /Users/$UserName | grep dsAttrTypeNative:initials | awk -F ' ' '{print $NF}'`
Address=`dscl /Active\\ Directory/ADA/All\\ Domains -read /Users/$UserName | grep -A1 "Street" | grep -v "Street" | sed -e 's/^[ \t]*//'`
fi

# Disable autoupdate
$PlistBuddy -c "Add :HowToCheck string"  $HOME/Library/Preferences/com.microsoft.autoupdate2.plist
$PlistBuddy -c "Set :HowToCheck Manual"  $HOME/Library/Preferences/com.microsoft.autoupdate2.plist
# Activate error reporting
#touch $HOME/Library/Preferences/com.microsoft.error_reporting.plist
$PlistBuddy -c "Add :SQMReportsEnabled string" $HOME/Library/Preferences/com.microsoft.error_reporting.plist
$PlistBuddy -c "Set :SQMReportsEnabled true" $HOME/Library/Preferences/com.microsoft.error_reporting.plist
$PlistBuddy -c "Add :ShipAssertEnabled string" $HOME/Library/Preferences/com.microsoft.error_reporting.plist
$PlistBuddy -c "Set :ShipAssertEnabled true" $HOME/Library/Preferences/com.microsoft.error_reporting.plist
# Branding Office 2011
$PlistBuddy -c "Add :14\\\UserInfo\\\UserName string" $HOME/Library/Preferences/com.microsoft.office.plist
$PlistBuddy -c "Set :14\\\UserInfo\\\UserName $Fullname" $HOME/Library/Preferences/com.microsoft.office.plist
$PlistBuddy -c "Add :14\\\UserInfo\\\UserInitials string" $HOME/Library/Preferences/com.microsoft.office.plist
$PlistBuddy -c "Set :14\\\UserInfo\\\UserInitials $Initials" $HOME/Library/Preferences/com.microsoft.office.plist
$PlistBuddy -c "Add :14\\\UserInfoUserOrganization string" $HOME/Library/Preferences/com.microsoft.office.plist
$PlistBuddy -c "Set :14\\\UserInfoUserOrganization $Org" $HOME/Library/Preferences/com.microsoft.office.plist
$PlistBuddy -c "Add :14\\\UserInfo\\\UserAddress string" $HOME/Library/Preferences/com.microsoft.office.plist
$PlistBuddy -c "Set :14\\\UserInfo\\\UserAddress $Address" $HOME/Library/Preferences/com.microsoft.office.plist
$PlistBuddy -c "Add :14\\\UserInfoSetupComplete string" $HOME/Library/Preferences/com.microsoft.office.plist
$PlistBuddy -c "Set :14\\\UserInfoSetupComplete 1" $HOME/Library/Preferences/com.microsoft.office.plist
$PlistBuddy -c "Add :14\\\FirstRun\\\SetupComplete integer" $HOME/Library/Preferences/com.microsoft.office.plist
$PlistBuddy -c "Set :14\\\FirstRun\\\SetupComplete 1" $HOME/Library/Preferences/com.microsoft.office.plist
$PlistBuddy -c "Add :14\\\FirstRun\\\MigrationForMASComplete integer" $HOME/Library/Preferences/com.microsoft.office.plist
$PlistBuddy -c "Set :14\\\FirstRun\\\MigrationForMASComplete 1" $HOME/Library/Preferences/com.microsoft.office.plist

# Setter MeContact.plist
mkdir -p $HOME/Library/Application\ Support/Microsoft/Office
$PlistBuddy -c "Add :First\ Name string" $HOME/Library/Application\ Support/Microsoft/Office/MeContact.plist
$PlistBuddy -c "Set :First\ Name $FirstName" $HOME/Library/Application\ Support/Microsoft/Office/MeContact.plist
$PlistBuddy -c "Add :Last\ Name string" $HOME/Library/Application\ Support/Microsoft/Office/MeContact.plist
$PlistBuddy -c "Set :Last\ Name $LastName" $HOME/Library/Application\ Support/Microsoft/Office/MeContact.plist
$PlistBuddy -c "Add :Initials string" $HOME/Library/Application\ Support/Microsoft/Office/MeContact.plist
$PlistBuddy -c "Set :Initials $Initials" $HOME/Library/Application\ Support/Microsoft/Office/MeContact.plist
$PlistBuddy -c "Add :Name string" $HOME/Library/Application\ Support/Microsoft/Office/MeContact.plist
$PlistBuddy -c "Set :Name $Fullname" $HOME/Library/Application\ Support/Microsoft/Office/MeContact.plist
$PlistBuddy -c "Add :Business\ Company string" $HOME/Library/Application\ Support/Microsoft/Office/MeContact.plist
$PlistBuddy -c "Set :Business\ Company $Org" $HOME/Library/Application\ Support/Microsoft/Office/MeContact.plist

# iPrepare Outlook for autoconfig by disabeling wizard
$defaults write com.microsoft.Outlook FirstRunExperienceCompleted 1

echo "dock"
# Add Word, Excel, Outlook and Powerpoint to dock
$dockutil --add /Applications/Microsoft\ Office\ 2011/Microsoft\ Word.app --replacing 'Microsoft Word'
$dockutil --add /Applications/Microsoft\ Office\ 2011/Microsoft\ Excel.app --replacing 'Microsoft Excel'
$dockutil --add /Applications/Microsoft\ Office\ 2011/Microsoft\ PowerPoint.app --replacing 'Microsoft PowerPoint'
$dockutil --add /Applications/Microsoft\ Office\ 2011/Microsoft\ Outlook.app --replacing 'Microsoft Outlook'

fi
# Setting .OfficePrefsSetupDone
touch $HOME/Library/Preferences/.OfficePrefsSetupDone
fi




