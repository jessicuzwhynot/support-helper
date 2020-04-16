######################################################################
# This is a Rockerfile (https://github.com/grammarly/rocker)
######################################################################
#
# Variables that are parsed:
#
# {{ $action := (or .action "") }}
# {{ $tag := (or .tag "local") }}
# {{ $repo := (or .repo "dockerhub.cisco.com/crate-docker/") }}
# {{ $image := (or .image "<use --var to set image name>") }}
# {{ $baseTag := (print "build-" (or .Env.BUILD_NUM "latest")) }}
# {{ $testResultsTag := (print "test-results-" (or .Env.BUILD_NUM "latest")) }}
#
# Place at the end of any wget to get a filtered progress output
# {{ $wget_filter := "2>&1 | stdbuf -o0 awk '!/[0-9]+K/||$7~/[0-9]+0%/&&l!=$7{l=$7;print$0}'" }}

######################################################################
# Python App Layers
######################################################################

FROM python:3.6-alpine

RUN pip install requests
RUN mkdir /app
COPY app/app.py /app/app.py

ENTRYPOINT ["python3", "/app/app.py"]

TAG {{ $image }}:{{ $baseTag }}

######################################################################
# Release
######################################################################

##### Publish the image #####
{{ if (eq $action "publish") (ne $tag "local") }}
PUSH {{ $repo }}{{ $image }}:{{ $tag }}
{{ end }}