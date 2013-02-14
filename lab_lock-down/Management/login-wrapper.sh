#!/bin/tcsh -f

############################ login-wrapper.sh ######################
# Mike Bombich | mike@bombich.com                
# Copyright 2003 Mike Bombich.     
# Use Loginwindow Manager (http://www.bombich.com/software/lwm.html)
# to make this shell script run each time a user logs in or out.
####################################################################


### Description ###
#
# This script launches other scripts, passing the appropriate
# parameters. You can use this script to combine the functionality
# of multiple scripts without combining their contents.


### Properties ###
#
# These items must be modified to suit your environment before
# implementing this script! You do not need to make any other
# modifications to this file than these properties.
#
# You will also need to add the scripts that you want to run to the
# Script Action section following the examples provided
# scriptDir: The directory in which you store your shell scripts
# scriptLog: The location of a log file (optional). Leave at /dev/null
# 		for no log
set scriptDir = /Library/Management
set scriptLog = /Library/Management/login-wrapper.log


### Debug/testing sanity check ###
if ( $#argv < 1 ) then
	echo "No user specified!"
	exit 1
endif


### Script action ###
# Remove the "#" in front of a line to allow that script to execute
# Each script must be followed by "$1" (passes the name of the user)

$scriptDir/refresh-default-homedir.sh "$1" >> $scriptLog
#$scriptDir/login-byhost.sh "$1" >> $scriptLog
#$scriptDir/keyaccess.sh "$1" >> $scriptLog
$scriptDir/ignore_ownership_on_video_volume.sh "$1" >> $scriptLog

### Always exit with 0 status
exit 0
