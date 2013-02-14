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

TITLE=user_prefs
REVERSE_DOMAIN=no.hioa
PACKAGE_VERSION=1.0.9
PAYLOAD=\
		pack-script-preflight \
		pack-remote-management \
		pack-user_prefs \
		pack-Library-LaunchAgents-no.hioa.user_prefs.plist	
pack-remote-management:
		@sudo mkdir -p ${WORK_D}/Library/Management/

pack-user_prefs:
		@sudo ${CP} user_prefs.sh ${WORK_D}/Library/Management/
