#!/bin/bash
# Find current user
current_user=`whoami`
# Check OS X version
sw_version=`sw_vers -productVersion | cut -d . -f 1,2`
#Check if /Library/Management/ada.hioa.no exist, else exit (Requires package ad_check)
if [ -f /Library/Management/ada.hioa.no ]
then
# Get info about usertype
if [ "${sw_version}" = "10.6" ]; then
ou_from_ada=`dscl /Active\ Directory/All\ Domains -read /Users/$current_user dsAttrTypeNative:distinguishedName | cut -d ',' -f 3 | grep OU`
else 
ou_from_ada=`dscl /Active\\ Directory/ADA/All\\ Domains -read /Users/$current_user dsAttrTypeNative:distinguishedName | cut -d ',' -f 3 | grep OU`
fi
# Connect to groupshare
#echo $ou_from_ada
if [ "${ou_from_ada}" = "OU=Employees" ]; then
exec osascript <<\EOF
try
mount volume "smb://server/share"
end try
EOF
fi
if [ "${ou_from_ada}" = "OU=Students" ]; then
exec osascript <<\EOF
try
mount volume "smb://server/share"
end try
EOF
fi
fi
