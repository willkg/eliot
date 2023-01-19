#!/usr/bin/env bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

set -eo pipefail

if [ "$1" = "--shell" ]
then
    bash
fi

# Run eliot-service tests
pushd eliot-service
pytest
popd
