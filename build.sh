#!/usr/bin/env bash
shopt -s expand_aliases
set -o nounset
set -o errexit

# Build variables and constants
PROJECT_BASENAME="$(basename $(pwd))"
ROCKER_VERSION='dockerhub.cisco.com/docker.io/segfly/rocker:1.3.0b'
ALLOWED_COMMANDS="build deps test unit_tests integration_tests external_integration_tests bava_tests qa_deploy publish deploy interactive"

# Setup CI variables
[[ -z "${JENKINS_URL+x}" ]] || CI_SERVER=1
[[ -z "${JOB_NAME+x}" ]] || JENKINSCI_PROJECT="${JOB_NAME%/*}"
PROJECT_NAME="${JENKINSCI_PROJECT:-${PROJECT_BASENAME}}"
export BUILD_NUM="${BUILD_NUMBER:-latest}"

# Validate the action against allowed commands
ACTION="${1:-build}"
if ! [[ "${ALLOWED_COMMANDS}" =~ (^|[[:space:]])"${ACTION}"($|[[:space:]]) ]]; then
    echo "usage:   ./build.sh <action> <opts>"
    echo
    echo "Available actions:"
    echo "build                      - Builds, tests, packages, and tags/pushes the application"
    echo "deps                       - Builds the app but does not run tests, useful for populating build cache"
    echo "test                       - Runs only the application unit tests"
    echo "unit_tests                 - Runs only the application unit tests"
    echo "integration_tests          - Runs only the internal integration tests"
    echo "external_integration_tests - Runs only the external integration tests"
    echo "bava_tests                 - Runs only the BAVA scanning tests"
    echo "qa_deploy                  - Stages the application in a testing environment"
    echo "publish                    - Publishes the artifacts"
    echo "deploy                     - Stages the application in the production environment"
    echo "interactive                - Enters an interactive shell for testing/debug"
    echo
    echo "Image names and tags are calculated automatically. Local builds are tagged 'local'"
    echo "To use Rocker attach, use ./build.sh build --attach"
    exit 1
fi
shift || true

## disable tty when executing Jenkins build
tty_option=$([ -z "${CI_SERVER+x}" ] && echo "t" || echo "")
alias rocker='docker run --env-file <(printenv | grep -v HOME) -v /var/run/docker.sock:/var/run/docker.sock -v "${HOME}/.docker":/root/.docker -v "${HOME}/.rocker_cache":/root/.rocker_cache -v "$(pwd)":"$(pwd)" -e HPWD="$(pwd)" -i'"${tty_option}"' --rm ${ROCKER_VERSION}'
alias docker-compose='docker run -v "$(pwd)":"$(pwd)" -v /var/run/docker.sock:/var/run/docker.sock -e COMPOSE_PROJECT_NAME=${PROJECT_NAME} --workdir="$(pwd)" -i --rm docker/compose:1.17.1'


# Support for building multiple docker images from the same repository
for dir in $PWD/docker/*/; do
  # Assemble the build arguments
  dir=${dir%*/}
  ROCKER_ARGS=()
  ROCKER_TARGET_ARGS=(--var action="${ACTION}" --var image="${PROJECT_NAME}/$(basename ${dir})" "${@:-}")
  ROCKER_CI_ARGS=(--cmd build)
  # Do a simple and fast build when NOT in a CI environment
  if [ -z "${CI_SERVER+x}" ]; then
    ROCKER_ARGS+=(build ${ROCKER_TARGET_ARGS[@]})
  else
    ROCKER_ARGS+=(${ROCKER_CI_ARGS[@]} ${ROCKER_TARGET_ARGS[@]})
  fi
  cd ${dir}
  # Execute the Rocker build action
  echo "Executing build action: ${ACTION}"
  echo "CI_SERVER=${CI_SERVER:-0}"
  echo "ROCKER_ARGS=${ROCKER_ARGS[@]}"
  echo
  rocker ${ROCKER_ARGS[@]}
done