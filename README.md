# support-helper
Utility to help Crate operations with various adhoc support activities

# Disconnected Host Notifier
A container that builds hourly on Jenkins, and notifies the #notify-ops slack
channel when there is a disconnected host, otherwise it runs silently.
The following variables are required when running this app.
```
RANCHER_URL - defaults to https://console.ciscocrate.com/v2-gbeta
RANCHER_ACCESS_KEY - Your Rancher API Access Key
RANCHER_SECRET_KEY - Your Rancher API Secret Key
SLACK_CHANNEL - defaults to #notify-ops
SLACK_WEBHOOK_URL - Slack webhook used to post the message to slack
``` 
