#!/bin/bash
#
# zenodo_upload.sh — upload one or more files into an existing
# Zenodo draft deposition.
#
# usage: ZENODO_TOKEN=xxx ./zenodo_upload.sh DEPOSITION_ID FILE [FILE...]
#        ./zenodo_upload.sh 21276988 data.zip.part.* data.zip.md5
#

set -eu

ZENODO_ENDPOINT=${ZENODO_ENDPOINT:-https://zenodo.org}
: "${ZENODO_TOKEN:?Set ZENODO_TOKEN env var}"
[ $# -ge 2 ] || { echo "usage: $0 DEPOSITION_ID FILE [FILE...]" >&2; exit 1; }

DEPOSITION=$(echo "$1" | sed 's+^http[s]*://zenodo.org/deposit/++g')
shift   # remaining args are the files to upload

AUTH="Authorization: Bearer ${ZENODO_TOKEN}"
MAX_RETRIES=10

# ── 1. fetch bucket of existing deposition ────────────────────────────
BUCKET=$(curl -sS -f -H "$AUTH" \
    "${ZENODO_ENDPOINT}/api/deposit/depositions/${DEPOSITION}" \
    | jq --raw-output .links.bucket)

echo "Deposition ID : $DEPOSITION"
echo "Bucket URL    : $BUCKET"
echo

# ── 2. upload each file with retry ────────────────────────────────────
upload_one() {
    local filepath="$1"
    local filename
    filename=$(basename "$filepath")
    filename=${filename// /%20}

    local n=0
    until [ "$n" -ge "$MAX_RETRIES" ]; do
        echo "Uploading ${filename} (attempt $((n+1))/${MAX_RETRIES})..."
        if curl -f -sS --progress-bar \
                -H "$AUTH" \
                -H "Content-Type: application/octet-stream" \
                --upload-file "$filepath" \
                "${BUCKET}/${filename}" > /tmp/zenodo_upload_resp.json; then
            echo "  OK  md5(zenodo)=$(jq -r .checksum /tmp/zenodo_upload_resp.json)"
            echo "      md5(local) =md5:$(md5sum "$filepath" | cut -d' ' -f1)"
            return 0
        fi
        n=$((n+1))
        echo "  failed; retrying in 15s..."
        sleep 15
    done
    echo "ERROR: ${filename} failed after ${MAX_RETRIES} attempts." >&2
    return 1
}

FAILED=0
for f in "$@"; do
    upload_one "$f" || FAILED=1
done

# ── 3. summary ────────────────────────────────────────────────────────
echo
echo "Files now in deposition ${DEPOSITION}:"
curl -sS -H "$AUTH" \
    "${ZENODO_ENDPOINT}/api/deposit/depositions/${DEPOSITION}/files" \
    | jq '.[] | {filename, filesize, checksum}'

if [ "$FAILED" -ne 0 ]; then
    echo "One or more uploads FAILED — do not publish yet." >&2
    exit 1
fi
echo "All uploads complete."
