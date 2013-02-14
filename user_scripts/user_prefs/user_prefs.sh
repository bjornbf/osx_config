#!/bin/bash
defaults="/usr/bin/defaults"
PlistBuddy="/usr/libexec/PlistBuddy"
# Finn innlogget bruker
current_user=`whoami`
# Checks if script has ran before 
if [ ! -f $HOME/Library/Preferences/.UserPrefsSetupDone ]
then
# Setting user prefs
# Finder
defaults write com.apple.finder ShowMountedServersOnDesktop 1
defaults write com.apple.finder ShowExternalHardDrivesOnDesktop 1
defaults write com.apple.finder ShowHardDrivesOnDesktop 1
defaults write com.apple.finder ShowRemovableMediaOnDesktop 1
defaults write com.apple.finder RemoveIDiskFromSidebarOnStartup 1
defaults write com.apple.finder ShowStatusBar 1
# Setting Norwegian languageformat
defaults write .GlobalPreferences AppleLocale nb_NO
defaults write com.apple.menuextra.clock DateFormat "EEE HH:mm"
# Disable iCloud popup
defaults write com.apple.SetupAssistant DidSeeCloudSetup -bool TRUE
# Configuring Right-click for Apple Mouse
defaults write com.apple.driver.AppleHIDMouse Button2 -int 2
defaults write com.apple.driver.AppleBluetoothMultitouch.mouse MouseButtonMode -string TwoButton
defaults write com.apple.driver.AppleBluetoothMultitouch.mouse MouseMomentumScroll -bool NO
# Demand password for screensaver
defaults write com.apple.screensaver askForPassword -integer 1
defaults write com.apple.screensaver askForPasswordDelay -float 0
# Setting Norwegian spelling (Requires /Library/Spelling/nb_NO.aff and /Library/Spelling/nb_NO.dic)
defaults write .GlobalPreferences NSPreferredSpellServerLanguage nb_NO
defaults write .GlobalPreferences NSPreferredSpellServerVendors "{"nb-NO" = Open;}"
defaults write .GlobalPreferences NSSpellCheckerAutomaticallyIdentifiesLanguages 0
# Setting homepage in Safari
defaults write com.apple.Safari HomePage "http://www.hioa.no/"
defaults write com.apple.Safari ShowStatusBar -bool YES
# Write "ok" file .UserPrefsSetupDone
touch $HOME/Library/Preferences/.UserPrefsSetupDone
# Log out users, for the new settings to be visible
# Ignore if currentuser is lab-account
if [ "${current_user}" = "lmok" ]; then
exit 0
fi
message=`/usr/bin/osascript <<EOF 
tell application "System Events"
activate
display alert "Configuring user enviroment, the computer will log out in 5 sec." giving up after 5
end tell
tell application "loginwindow" to «event aevtrlgo»
end
EOF`
echo $message
fi
exit 0
