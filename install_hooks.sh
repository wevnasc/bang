#!/bin/sh
BLUE='\033[0;34m'

cp ./hooks/pre-push .git/hooks/pre-push

echo "${BLUE}All hooks was installed" >&2