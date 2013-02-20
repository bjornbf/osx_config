#!/bin/bash
ad_check=`dsconfigad -show | grep "Active Directory Domain" | cut -d "=" -f 2 | sed -e 's/^[ \t]*//'`
if [ "${ad_check}" = "ada.hioa.no" ];then
touch /Library/Management/ada.hioa.no
fi
