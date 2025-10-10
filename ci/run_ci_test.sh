#!/bin/bash

#
# Copyright IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#

# Bash colors
NO_STYLE='\033[0m'
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'

# vars
PROFILE_FILE="${HOME}/.profile"

function print_logs() {
    local dir=$1

    find "$dir" -type f | while read -r file; do
        # Print the last part of the logs
        echo -e "📝 ${BLUE}$file${NO_STYLE}"
        tail -n 500 "$file"

        # Print only logs with `err` inside
        echo -e "🚨 ${RED}Error logs${NO_STYLE}"
        grep -i "err" "$file"
        echo
    done
}

# Collect deployment failure info
function collect_deployment_failure_info() {
    echo -e "🚩 ${BLUE}Retrieve status for service ports.${NO_STYLE}"

    make services ping
    make load-generators ping
    echo "✅ Done."

    echo -e "🚩 ${BLUE}List running docker containers.${NO_STYLE}"
    docker container ls
    echo "✅ Done."

    echo -e "🚩 ${BLUE}Retrieve the logs from the services.${NO_STYLE}"
    make services fetch-logs
    make load-generators fetch-logs
    echo "✅ Done."

    echo -e "🚩 ${BLUE}List the fetched log files.${NO_STYLE}"
    ls "$PROJECT_DIR/out/logs"
    echo "✅ Done."

    echo -e "🚩 ${BLUE}Show all the logs.${NO_STYLE}"
    print_logs "$PROJECT_DIR/out/logs"
    echo "✅ Done."
}

# Run a bash command.
function run_cmd() {
    local status

    echo -e "🕛 Running ${GREEN}$*${NO_STYLE}"
    "$@"
    status=$?

    # Show the logs only if the command fails
    if [[ $status -ne 0 ]]; then
        # collect general failure info
        echo -e "❌ ${RED}$*${NO_STYLE} failed with status: $status"
        collect_deployment_failure_info
        exit $status
    fi
}

set +e
set -o pipefail
trap exit 1 INT

# shellcheck source=/dev/null
source "${PROFILE_FILE}"

# run network and tests
run_cmd make setup
run_cmd make start
run_cmd sleep 10
run_cmd make load-generators get-metrics ASSERT_METRICS=true

# stop deployment
run_cmd make teardown
