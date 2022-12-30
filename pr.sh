

sudo defaults write /Library/Preferences/SystemConfiguration/com.apple.captive.control.plist Active -bool false
sudo networksetup -setwebproxy "Wi-Fi" 127.0.0.1 8118
sudo networksetup -setsecurewebproxy "Wi-Fi" 127.0.0.1 8118
defaults write /Library/Preferences/com.apple.mDNSResponder.plist NoMulticastAdvertisements -bool YES

sudo dscacheutil -flushcache;
sudo killall -HUP mDNSResponder;
sudo rm -rfv "~/Library/Logs/*" "/var/log/*" "~/Library/Caches/*" "/Library/Caches/*" "~/Library/Saved Application State/*"
netstat -anv | grep CLOSE_WAIT | awk '{print $9}' | xargs kill && netstat -anv | grep CLOSED | awk '{print $9}' | xargs kill
sudo chmod -R 000 ~/Library/LanguageModeling ~/Library/Spelling ~/Library/Suggestions
sudo chflags -R uchg ~/Library/LanguageModeling ~/Library/Spelling ~/Library/Suggestions
sudo chmod -R 000 "~/Library/Application Support/Quick Look"
sudo chflags -R uchg "~/Library/Application Support/Quick Look"
sudo chflags -R uchg ~/Library/Assistant/SiriAnalytics.db
defaults delete ~/Library/Preferences/com.apple.iTunes.plist recentSearches
defaults delete ~/Library/Preferences/com.apple.iTunes.plist StoreUserInfo
defaults delete ~/Library/Preferences/com.apple.iTunes.plist WirelessBuddyID


# history -r removes the terminal history temporarily for the current session.
# history -w removes it permanently.
rm ~/.bash_history;
rm ~/.zsh_history;

rm -rfv "~/Library/LanguageModeling/*" "~/Library/Spelling/*" "~/Library/Suggestions/*" && rm -rfv "~/Library/Application Support/Quick Look/*" && rm -rfv ~/Library/Assistant/SiriAnalytics.db
rm -rf ~/Library/Containers/com.apple.QuickTimePlayerX/Data/Library/Preferences/com.apple.QuickTimePlayerX.plist && rm -rf ~/Library/Containers/com.apple.appstore/Data/Library/Preferences/com.apple.commerce.knownclients.plist && rm -rf ~/Library/Preferences/com.apple.commerce.plist && rm -rf ~/Library/Preferences/com.apple.QuickTimePlayerX.plist

sudo rm -rfv /var/spool/cups/c0*
sudo rm -rfv /var/spool/cups/tmp/*
sudo rm -rfv /var/spool/cups/cache/job.cache*
sudo rm -rfv /var/db/lockdown/*

defaults delete ~/Library/Preferences/com.apple.finder.plist FXDesktopVolumePositions
defaults delete ~/Library/Preferences/com.apple.finder.plist FXRecentFolders
defaults delete ~/Library/Preferences/com.apple.finder.plist RecentMoveAndCopyDestinations
defaults delete ~/Library/Preferences/com.apple.finder.plist RecentSearches
defaults delete ~/Library/Preferences/com.apple.finder.plist SGTRecentFileSearches



### DATA SCIENCE AND MACHINE LEARNING ###
PYTHON_VERSION=$(cat .python-version)
brew install miniforge
conda create -n base_env python=$PYTHON_VERSION
conda install seaborn
conda install -c conda-forge cookiecutter

### INSTALLING TENSOR FLOW ###
conda install -c apple tensorflow-deps
conda config --prepend channels apple


### PIP ENV ###
pipenv --python $PYTHON_VERSION


### GIT ###
git config --global user.name ""
git config --global user.email ""
git config --global commit.gpgsign true
git config --global user.signingkey {YOUR_GPG_KEY_FINGERPRINT}


### COOKIE CUTTER DATA SCIENCE ###'
conda create -n my-project-env pandas jupyter scikit-learn matplotlib seaborn
conda activate my-project-env
cookiecutter -c v1 https://github.com/drivendata/cookiecutter-data-science
code my-project-directory
git init
git add .
git commit -m "First commit."
git remote add origin https://www.github.com/yourname/your-repo-name.git
git push origin master


### SOFTARE UPDATE ###
softwareupdate -i -a

# SET DEFAULT SHELL TO ZSH
sudo chsh -s /bin/zsh

### GITHUB ###
gh auth login



### R ###
Sys.setlocale(category="LC_ALL", locale = "en_US.UTF-8")


### asdf ###
asdf plugin-add erlang
asdf plugin-add elixir
asdf plugin-add nodejs
asdf plugin-add yarn
asdf plugin-add direnv

asdf install erlang latest
asdf install elixir latest
asdf install nodejs latest
asdf install yarn latest
asdf install direnv latest
direnv_version=$(direnv --version)
asdf global direnv ${direnv_version}


### postgresql ###
#createuser -d -P -s postgres

### git ###
git config --global commit.gpgsign true
git config --global user.signingkey 99DC9E7993AEB537
git config --global core.excludesfile ~/.gitignore


### noisy ###
git clone https://github.com/1tayH/noisy.git

### web-traffic-generator ###
git clone https://github.com/ReconInfoSec/web-traffic-generator.git


### antivmdetection ###
git clone https://github.com/nsmfoo/antivmdetection.git


### dns_over_tls_over_tor ###
https://github.com/piskyscan/dns_over_tls_over_tor.git

### dispatch ###
git clone https://github.com/Netflix/dispatch-docker.git

## GPG ###
gpg --full-generate-key
gpg --armor --export {this-is-your-gpg-key-id}


## persistence
## persistence
sudo defaults write -g ApplePersistence -bool no
# do not open previous previewed files when opening a new one
sudo defaults write com.apple.Preview ApplePersistenceIgnoreState YES

# App Store
## List All Apps Downloaded from App Store
### Via find
find /Applications -path '*Contents/_MASReceipt/receipt' -maxdepth 4 -print |\sed 's#.app/Contents/_MASReceipt/receipt#.app#g; s#/Applications/##'
### Via Spotlight
mdfind kMDItemAppStoreHasReceipt=1

# Apple Remote Desktop
## Deactivate and Stop the Remote Management Service
sudo /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart -deactivate -stop
## Disable ARD Agent and Remove Access Privileges for All Users (Default)
sudo /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart -deactivate -configure -access -off
## Remove Apple Remote Desktop Settings
sudo rm -rf /var/db/RemoteManagement ; \
sudo defaults delete /Library/Preferences/com.apple.RemoteDesktop.plist ; \
defaults delete ~/Library/Preferences/com.apple.RemoteDesktop.plist ; \
sudo rm -r /Library/Application\ Support/Apple/Remote\ Desktop/ ; \
rm -r ~/Library/Application\ Support/Remote\ Desktop/ ; \
rm -r ~/Library/Containers/com.apple.RemoteDesktop

# Google
## Uninstall Google Update
~/Library/Google/GoogleSoftwareUpdate/GoogleSoftwareUpdate.bundle/Contents/Resources/ksinstall --nuke

# Vacuum Mail Index
vacuum_mail_index() {
#!/bin/zsh

#
# Speed up Mail.app by vacuuming the Envelope Index
# Written by Marcel Bischoff
# AppleScript original by "pmbuko" with modifications by Romulo
#

OS_VERSION=$(sw_vers -productVersion | cut -d. -f 1,2)
MAIL_RUNNING=$(ps aux | grep -v grep | grep -c "Mail\$")
MAIL_VERSION="V2"

if [ $MAIL_RUNNING -gt 0 ]; then osascript -e 'tell application "Mail" to quit'; fi

if [ 1 -eq "$(echo "11 <= ${OS_VERSION}" | bc)" ]; then MAIL_VERSION="V8"; fi

SIZE_BEFORE=$(ls -lnah ~/Library/Mail/${MAIL_VERSION}/MailData | grep -E 'Envelope Index$' | awk {'print $5'})
/usr/bin/sqlite3 ~/Library/Mail/${MAIL_VERSION}/MailData/Envelope\ Index vacuum
SIZE_AFTER=$(ls -lnah ~/Library/Mail/${MAIL_VERSION}/MailData | grep -E 'Envelope Index$' | awk {'print $5'})

printf "Mail index before: %s\nMail index after: %s\n" $SIZE_BEFORE $SIZE_AFTER
}


# DOCK


# Files, Disks and Volumes

## Disable Sudden Motion Sensor
### Leaving this turned on is useless when you're using SSDs.
sudo pmset -a sms 0

## Eject All Mountable Volumes
osascript -e 'tell application "Finder" to eject (every disk whose ejectable is true)'


# Files and Folders
## Show All File Extensions
defaults write -g AppleShowAllExtensions -bool true
## Show Hidden Files
## Show All
defaults write com.apple.finder AppleShowAllFiles true
## Show Full Path in Finder Title
defaults write com.apple.finder _FXShowPosixPathInTitle -bool true

# Layout
## Save to Disk by Default
### Sets default save target to be a local disk, not iCloud.
defaults write -g NSDocumentSaveNewDocumentsToCloud -bool false

# Metadata Files
## Disable Creation of Metadata Files on Network Volumes
### Avoids creation of .DS_Store and AppleDouble files.
defaults write com.apple.desktopservices DSDontWriteNetworkStores -bool true
## Disable Creation of Metadata Files on USB Volumes
### Avoids creation of .DS_Store and AppleDouble files.
defaults write com.apple.desktopservices DSDontWriteUSBStores -bool true

# Fonts
## Clear Font Cache for Current User
### To clear font caches for all users, put sudo in front of these commands.
sudo atsutil databases -removeUser && \
sudo atsutil server -shutdown && \
sudo atsutil server -ping

# Media
## Disable Sound Effects on Boot
sudo nvram SystemAudioVolume=" "
##  Startup Chime
### Disable (Default)
sudo nvram StartupMute=%01

# Networking
## Bonjour Service
### Disable
sudo defaults write /System/Library/LaunchDaemons/com.apple.mDNSResponder.plist ProgramArguments -array-add "-NoMulticastAdvertisements"
## Hostname
### Set Computer Name/Host Name
sudo scutil --set ComputerName "newhostname" && \
sudo scutil --set HostName "newhostname" && \
sudo scutil --set LocalHostName "newhostname" && \
sudo defaults write /Library/Preferences/SystemConfiguration/com.apple.smb.server NetBIOSName -string "newhostname"

## SSH
### Permanently Add Private Key Passphrase to SSH Agent
ssh-add -K /path/to/private_key
# Then add to ~/.ssh/config:
# Host server.example.com
#     IdentityFile /path/to/private_key
#     UseKeychain yes
### Remove Login
#### Disable (Default)
sudo launchctl unload -w /System/Library/LaunchDaemons/ssh.plist

## TCP/IP
### Show External IP Address
#### Works if your ISP doesn't replace DNS requests (which it shouldn't).
dig +short myip.opendns.com @resolver1.opendns.com
#### Alternative that works on all networks.
curl -s https://api.ipify.org && echo

## Wi-Fi
### Scan Available Access Points
#### Create a symbolic link to the airport command for easy access:
sudo ln -s /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport /usr/local/bin/airport

### Run a wireless scan:
airport -s

### Show Current SSID
/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | awk '/ SSID/ {print substr($0, index($0, $2))}'

### Show Local IP Address
ipconfig getifaddr en0 # or en1

### Show Wi-Fi Connection History
defaults read /Library/Preferences/SystemConfiguration/com.apple.airport.preferences | grep LastConnected -A 7

### Show Wi-Fi Network Passwords
#### Exchange SSID with the SSID of the access point you wish to query the password from.
security find-generic-password -D "AirPort network password" -a "SSID" -gw

### Turn on Wi-Fi Adapter
networksetup -setairportpower en0 on

## Security

### Application Firewall
### Firewall Service
#### Show Status
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
#### Enable
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
#### Disable (Default)
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off
#### Add Application to Firewall
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /path/to/file

### Gatekeeper
#### Add Gatekeeper Exception
spctl --add /path/to/Application.app
#### Remove Gatekeeper Exception
spctl --remove /path/to/Application.app
#### Manage Gatekeeper
#### Especially helpful with the annoying macOS 10.15 (Catalina) system popup blocking execution of non-signed apps.
#### Status
spctl --status
#### Enable (Default)
sudo spctl --master-enable
#### Disable
sudo spctl --master-disable

### Passwords
#### Generate Secure Password and Copy to Clipboard
LC_ALL=C tr -dc "[:graph:]" < /dev/urandom | head -c 128 | pbcopy


# Search
## Find
### Recursively Delete .DS_Store Files
find . -type f -name '.DS_Store' -ls -delete
## Locate
### Build Locate Database
sudo launchctl load -w /System/Library/LaunchDaemons/com.apple.locate.plist
### Search via Locate
#### The -i modifier makes the search case insensitive.
locate -i *.jpg


# System

## Basics

### Restore Sane Shell
#### In case your shell session went insane (some script or application turned it into a garbled mess).
stty sane

### Restart
sudo reboot

### Shutdown
sudo poweroff

### Show Build Number of OS
sw_vers

### Uptime
#### How long since your last restart.
uptime

## Clipboard

### Sort and Strip Duplicate Lines from Clipboard Content
pbpaste | sort | uniq | pbcopy

## iCloud
### Force Sign Out
defaults delete MobileMeAccounts

## Kernel Extensions
### Display Status of Loaded Kernel Extensions
sudo kextstat -l

## LaunchServices
### Rebuild LaunchServices Database
#### To be independent of OS X version, this relies on locate to find lsregister. If you do not have your locate database built yet, do it.
sudo $(locate lsregister) -kill -seed -r

## Memory Management
### Purge memory cache
sudo purge
### Show Memory Statistics
#### One time
vm_stat
#### Table of data, repeat 10 times total, 1 second wait between each poll
vm_stat -c 10 1

## Notification Center
### Notification Center Service
#### Disable
launchctl unload -w /System/Library/LaunchAgents/com.apple.notificationcenterui.plist && \
killall -9 NotificationCenter

## Remote Management
### Remote Apple Events
#### Status
sudo systemsetup -getremoteappleevents
#### Disable (Default)
sudo systemsetup -setremoteappleevents off

## Root User
### Disable (Default)
dsenableroot -d

## Save Dialogs
### Significantly improve the now rather slow animation in save dialogs.
defaults write NSGlobalDomain NSWindowResizeTime .001

## Spell Checking
### Global Spell Checking
# Disable
defaults delete -g NSAllowContinuousSpellChecking

## Spotlight
### Spotlight Indexing
####Erase Spotlight Index and Rebuild
sudo mdutil -E -a /
# Remove the Spotlight index directory on the specified volume.  Does not disable indexing.
# Spotlight will reevaluate volume when it is unmounted and remounted, the
# machine is rebooted, or an explicit index command such as 'mdutil -i' or 'mdutil -E' is
# un for the volume.
sudo mdutil -X -a /
#### Disable
sudo mdutil -i off -d -a /


# BASH/ZSH AUTO COMPLETION
autoload bashcompinit && bashcompinit

# SSH
mkdir $HOME/.ssh
chmod 0700 $HOME/.ssh

## BREW FORMULA
brew install wget
brew install tree
brew install jq
brew install terminal-notifier
# ASDF
brew install asdf
# --- then, add 'asdf' in plugins list in ~/.zshrc ---
# asdf uses a file .tool-version in home directory to keep track of default runtime versions
# JS
brew install node
brew install nvm
brew install pnpm
# GO
brew install golang
# RUBY
brew install rbenv
brew install autoconf automake gdbm gmp libksba libtool libyaml openssl pkg-config readline
# KUBERNETES
brew install kubernetes-cli
brew install minikube
brew install kubernetes-helm
brew install skaffold
# POSTGRESQL
berw install postgresql
# MARIADB
brew install mariadb
# MYSQL
brew install mysql
# SQLITE3
brew install sqlite3
# REDIS
brew install redis
# ELASTICSEARCH
brew install elasticsearch
# VIRTUAL MACHINE MANAGER
brew install hyperkit
# PYTHON
brew install pyenv
brew install pyenv-virtualenv
# YARN
brew install yarn --without-node


# RUST

## BREW CASKS
#1	visual-studio-code
#2	iterm2
#3	docker
#5	firefox
#6	ngrok
#9	postman
brave-browser
tor
firefox developer edition

brew cask install homebrew/cask-versions/java8


# PYENV
pyenv install miniconda3-x.x.x

# MINICONDA
conda install jupyter

# XCODE
xcode-select --install
softwareupdate --install-rosetta --agree-to-license

# TYPESCRIPT
npm i -g typescript

# VERCEL
npm i -g vercel
