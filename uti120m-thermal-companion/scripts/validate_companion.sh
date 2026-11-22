#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${1:?Usage: validate_companion.sh /path/to/companion/android}"
cd "$PROJECT_DIR"

./gradlew :app:assembleDebug

if [[ -f "$PROJECT_DIR/app/src/main/java/com/diabcare/thermal/Uti120Protocol.java" \
   && -f "$PROJECT_DIR/src/test/java/com/diabcare/thermal/Uti120ProtocolSmokeTest.java" ]]; then
  TEST_DIR="$(mktemp -d)"
  trap 'rm -rf "$TEST_DIR"' EXIT
  javac -d "$TEST_DIR" \
    "$PROJECT_DIR/app/src/main/java/com/diabcare/thermal/Uti120Protocol.java" \
    "$PROJECT_DIR/src/test/java/com/diabcare/thermal/Uti120ProtocolSmokeTest.java"
  java -cp "$TEST_DIR" com.diabcare.thermal.Uti120ProtocolSmokeTest
fi

git diff --check
printf 'Companion validation passed: %s\n' "$PROJECT_DIR"
