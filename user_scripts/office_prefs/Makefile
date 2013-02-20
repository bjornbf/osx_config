#
#   Copyright 2011 Bjørn Bergli Fodstad <bjorn.bergli.fodstad@hioa.no>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# Sample package that packages luggage.make and prototype.plist

include /usr/local/share/luggage/luggage.make

TITLE=office_setup
REVERSE_DOMAIN=no.hioa
PACKAGE_VERSION=1.0.5
PAYLOAD=\
		pack-script-preflight \
		pack-remote-management \
		pack-office-script \
		pack-Library-LaunchAgents-no.hioa.office_setup.plist	

pack-remote-management:
		@sudo mkdir -p ${WORK_D}/Library/Management/

pack-office-script:
		@sudo ${CP} office_setup.sh ${WORK_D}/Library/Management/
		@sudo mkdir -p ${WORK_D}/System/Library/User\ Template/English.lproj/Documents/
		@sudo ${TAR} -xvf Microsoft_User_Data.tar.gz -C ${WORK_D}/System/Library/User\ Template/English.lproj/Documents/
		@sudo ${TAR} -xvf Outlook_Setup_script.tar.gz -C ${WORK_D}/Library/Management/
		@sudo chown -R root:wheel ${WORK_D}/System/Library/User\ Template/English.lproj/Documents
		@sudo chown -R root:staff ${WORK_D}/Library/Management/
