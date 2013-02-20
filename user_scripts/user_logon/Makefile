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

TITLE=user_logon_script
REVERSE_DOMAIN=no.hioa
DESCRIPTION=Endret servernavn for fellesomraade
PACKAGE_VERSION=1.9
PAYLOAD=\
		pack-remote-management \
		pack-logon-script \
		pack-Library-LaunchAgents-no.hioa.user-logon-script.plist \

pack-remote-management:
		@sudo mkdir -p ${WORK_D}/Library/Management/userplist

pack-logon-script:
		@sudo ${CP} logon.sh ${WORK_D}/Library/Management/

