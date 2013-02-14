#!/bin/tcsh -f

############################ template.sh ###########################
# Author Name | author@email.com
# Copyright 2003 Author Name
# Use Loginwindow Manager (http://www.bombich.com/software/lwm.html)
# to make this shell script run each time a user logs in or out.
####################################################################


### Description ###
#
# This script does the following really interesting stuff
# Be brief, and understand that your audience may know nothing of
# the command-line environment. Be sure to include warnings and
# disclaimers in this section too.


### Properties ###
#
# These items must be modified to suit your environment before
# implementing this script! You do not need to make any other
# modifications to this file than these properties.
#
set Volume = /Volumes/Video


## The end users of this script should not have to read past this line
## to safely and correctly implement this script. Make sure you explain
## very well what appropriate values are for the properties.


### Debug/testing sanity check ###
if ( $#argv < 1 ) then
	echo "No user specified!"
	exit 1
endif


### Script action ###
# feel free to comment as much as you like
/usr/sbin/vsdbutil -d $Volume


### Always exit with 0 status
exit 0