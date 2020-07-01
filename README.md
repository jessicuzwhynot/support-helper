# support-helper
Utility to help Crate operations with various adhoc support activities

# Disconnected Host Notifier
A container that builds hourly on Jenkins, and notifies the #notify-ops slack
channel when there is a disconnected host, otherwise it runs silently.
The following variables are required when running this app.
```shell script
    RANCHER_URL - defaults to https://console.ciscocrate.com/v2-gbeta
    RANCHER_ACCESS_KEY - Your Rancher API Access Key
    RANCHER_SECRET_KEY - Your Rancher API Secret Key
    SLACK_CHANNEL - defaults to #notify-ops
    SLACK_WEBHOOK_URL - Slack webhook used to post the message to slack
``` 

# Provisioning Automation
Automated custom host provisioning.  

This automation creates cloud configuration and executes `vmdeploy-service`, thus it must be run in the same environment and on the same host as `provisioning-service` and the location of the cloud configuration and the docker.sock must be mounted as volumes. 
```yaml
    volumes:
    - bootroot:/app/assets/config/hostname/
    - /var/run/docker.sock:/var/run/docker.sock
    labels:
      io.rancher.scheduler.affinity:host_label: crate.host.name=trusting_newton
      io.rancher.container.start_once: 'true'
      io.rancher.container.pull_image: always
```
The following variables are required when running this app.
```shell script
    NEW_HOST_CPU: # amount of cpu for new hosts
    NEW_HOST_HDD: # amount of disk for new hosts
    NEW_HOST_RAM: # amount of ram for new hosts
    NEW_HOST_REGION: # region to create new hosts in
    NUMBER_OF_NEW_HOSTS: # number of new hosts to create
    RANCHER_ACCESS_KEY: # Rancher API Access Key
    RANCHER_ENVIRONMENT: # environment to add hosts to
    RANCHER_SECRET_KEY: # Rancher API Secret Key
    VMDEPLOY_PASS: # vmdeploy password
    VMDEPLOY_USER: # vmdeploy user
```
Example docker-compose:
```yaml
version: '2'
services:
  custom-provisioning:
    image: dockerhub.cisco.com/crate-docker/provisioning-automation:latest
    environment:
      DEBUG: 'True'
      NEW_HOST_CPU: '6'
      NEW_HOST_HDD: '25'
      NEW_HOST_RAM: '8'
      NEW_HOST_REGION: SJC
      NUMBER_OF_NEW_HOSTS: '3'
      RANCHER_ACCESS_KEY: # Rancher API Access Key
      RANCHER_ENVIRONMENT: # environment to add hosts to
      RANCHER_SECRET_KEY: # Rancher API Secret Key
      VMDEPLOY_PASS: # vmdeploy password
      VMDEPLOY_USER: # vmdeploy user
    volumes:
    - bootroot:/app/assets/config/hostname/
    - /var/run/docker.sock:/var/run/docker.sock
    tty: true
    labels:
      io.rancher.scheduler.affinity:host_label: crate.host.name=trusting_newton
      io.rancher.container.start_once: 'true'
      io.rancher.container.pull_image: always
```