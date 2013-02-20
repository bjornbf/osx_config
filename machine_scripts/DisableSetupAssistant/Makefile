include /usr/local/share/luggage/luggage.make
TITLE=DisableSetupAssistant
REVERSE_DOMAIN=no.hioa
PACKAGE_VERSION=1.0
PAYLOAD=\
	DisableSetupAssistant

DisableSetupAssistant:
	@sudo mkdir -p ${WORK_D}/var/db
	@sudo touch ${WORK_D}/var/db/.AppleSetupDone
