#!/bin/tcsh -f

##
############################ login.sh ###########################
# Mike Bombich | mike@bombich.com                
# Copyright 2002 Mike Bombich.     
# With the appropriate modification to /etc/ttys, this script will
# execute each time a user logs in.
##################################################################
# This script takes the username as an argument, then removes any
# old default home directory, restores a fresh copy of the default
# home directory, then chowns it to logging in user.
##

## Properties
set defGrp = staff

# This part is for debugging/testing purposes only
if ( $#argv < 1 ) then
	echo "No user specified!"
	exit 1
endif

# If this is the default user, replace the default home directory
# with a copy of the user template
if ( $1 == "lmok" ) then
	rm -rf /Users/$1
	/usr/bin/ditto -rsrcFork "/Library/Management/lmok.lproj" /Users/$1
	/usr/sbin/chown -R ${1}:${defGrp} /Users/$1
endif
