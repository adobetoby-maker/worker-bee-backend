#!/bin/zsh
mkdir -p ~/.ssl
openssl req -x509 -newkey rsa:4096 \
    -keyout ~/.ssl/key.pem -out ~/.ssl/cert.pem \
    -days 365 -nodes -subj "/CN=localhost" 2>/dev/null
launchctl unload ~/Library/LaunchAgents/com.workerbee.agent.plist
launchctl load ~/Library/LaunchAgents/com.workerbee.agent.plist
echo "Cert renewed and agent restarted"
