# ###
#!/bin/bash

# Updated script (detect granted vs pending vs new invite)

# This version:

# Loads config from .env

# Fetches open invitations once (fast)

# For each username:

      # If collaborator -> already approved/granted

      # Else if in open invitations -> already sent - pending

      # Else -> send invite -> new request sent (201)



# Zero-arg usage:
# $ chmod +x run.sh
# $ ./run.sh

#
# Expects a .env file next to this script with:
#   GITHUB_TOKEN=...
#   OWNER=...
#   REPO=...
#   USER_FILE=...   (path to file with one username per line)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"

if [ ! -f "$ENV_FILE" ]; then
  echo "Error: .env file not found at: $ENV_FILE"
  exit 1
fi

set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a

: "${GITHUB_TOKEN:?Error: GITHUB_TOKEN is missing in .env}"
: "${OWNER:?Error: OWNER is missing in .env}"
: "${REPO:?Error: REPO is missing in .env}"
: "${USER_FILE:?Error: USER_FILE is missing in .env}"

if [[ "$USER_FILE" != /* ]]; then
  USER_FILE="$SCRIPT_DIR/$USER_FILE"
fi
if [ ! -f "$USER_FILE" ]; then
  echo "Error: USER_FILE not found at: $USER_FILE"
  exit 1
fi

API="https://api.github.com"
HDR_A="Accept: application/vnd.github+json"
HDR_Z="Authorization: Bearer $GITHUB_TOKEN"

# 1) Build a set of OPEN (pending) invitations once.
# This endpoint lists all currently open repo invitations. :contentReference[oaicite:5]{index=5}
INVITED_LOGINS="$(
  curl -s -H "$HDR_A" -H "$HDR_Z" \
    "$API/repos/$OWNER/$REPO/invitations" \
  | grep -o '"login":[[:space:]]*"[^"]\+"' \
  | sed -E 's/.*"login":[[:space:]]*"([^"]+)".*/\1/' \
  | sort -u
)"

is_in_invites() {
  local u="$1"
  echo "$INVITED_LOGINS" | grep -qx "$u"
}

while IFS= read -r USERNAME || [ -n "$USERNAME" ]; do
  USERNAME="$(echo "$USERNAME" | xargs)"
  [[ -z "$USERNAME" || "$USERNAME" =~ ^# ]] && continue

  # 2) Check if user is already a collaborator. (204 = yes, 404 = no) :contentReference[oaicite:6]{index=6}
  COLLAB_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "$HDR_A" -H "$HDR_Z" \
    "$API/repos/$OWNER/$REPO/collaborators/$USERNAME")

  if [ "$COLLAB_STATUS" -eq 204 ]; then
    echo "already approved/granted: $USERNAME"
    continue
  fi

  # 3) If not collaborator, see if there is an OPEN invitation already.
  if is_in_invites "$USERNAME"; then
    echo "request already sent (pending): $USERNAME"
    continue
  fi

  # 4) Otherwise, send a new invitation with write access.
  # PUT returns 201 when a new invitation is created, 204 when already has access. :contentReference[oaicite:7]{index=7}
  PUT_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -X PUT \
    -H "$HDR_A" -H "$HDR_Z" \
    "$API/repos/$OWNER/$REPO/collaborators/$USERNAME" \
    -d '{"permission":"push"}')

  case "$PUT_STATUS" in
    201) echo "new request sent: $USERNAME" ;;
    204) echo "already approved/granted: $USERNAME" ;;
    403) echo "failed (403): insufficient permission/token scope -> $USERNAME" ;;
    404) echo "failed (404): user or repo not found (or no access to private repo) -> $USERNAME" ;;
    422) echo "failed (422): validation/spam/role restriction -> $USERNAME" ;;
    *)   echo "failed: unexpected response ($PUT_STATUS) -> $USERNAME" ;;
  esac

done < "$USER_FILE"
