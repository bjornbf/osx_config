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

TITLE=mail_setup
REVERSE_DOMAIN=no.hioa
PACKAGE_VERSION=0.1.6
PAYLOAD=\
		pack-remote-management \
		pack-mail-setup-ews-1.0 \
		pack-Library-LaunchAgents-no.hioa.mail-setup-ews.plist

pack-remote-management:
		@sudo mkdir -p ${WORK_D}/Library/Management/
pack-mail-setup-ews-1.0:
		@sudo ${CP} -r mail-setup-ews-1.0 ${WORK_D}/Library/Management/
		@sudo chmod -R 755 ${WORK_D}/Library/Management/mail-setup-ews-1.0
