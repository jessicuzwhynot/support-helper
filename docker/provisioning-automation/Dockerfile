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

FROM python:3.7-alpine

RUN apk --no-cache add docker
COPY app /app
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ENTRYPOINT ["python", "-u", "/app/app.py"]

TAG {{ $image }}:{{ $baseTag }}

######################################################################
# Test Layers
######################################################################

{{ if (eq $action "build" "test") }}
COPY requirements-test.txt /requirements-test.txt
RUN pip install -r requirements-test.txt

COPY tests /tests
RUN cd /tests && pytest unit_tests.py

TAG {{ $image }}:{{ $testResultsTag }}
{{ end }}

######################################################################
# Interactive Shell
######################################################################

{{ if (eq $action "interactive") }}
ATTACH /bin/sh
{{ end }}

######################################################################
# Release
######################################################################

##### Publish the image #####
{{ if (eq $action "publish") (ne $tag "local") }}
PUSH {{ $repo }}{{ $image }}:{{ $tag }}
{{ end }}