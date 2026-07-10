#!/bin/bash
#
# zenodo_new_deposit_upload.sh — create a new Zenodo draft deposition
# and upload one or more files into it.
#
# usage: ZENODO_TOKEN=xxx ./zenodo_new_deposit_upload.sh data.zip [more files...]
#        ./zenodo_new_deposit_upload.sh data.zip.part.* data.zip.md5
#

set -eu

ZENODO_ENDPOINT=${ZENODO_ENDPOINT:-https://zenodo.org}
: "${ZENODO_TOKEN:?Set ZENODO_TOKEN env var}"
[ $# -ge 1 ] || { echo "usage: $0 FILE [FILE...]" >&2; exit 1; }

AUTH="Authorization: Bearer ${ZENODO_TOKEN}"
MAX_RETRIES=10

# ── 1. create empty draft ─────────────────────────────────────────────
RESPONSE=$(curl -sS -f -X POST \
    -H "$AUTH" \
    -H "Content-Type: application/json" \
    -d '{}' \
    "${ZENODO_ENDPOINT}/api/deposit/depositions")

DEPOSITION_ID=$(echo "$RESPONSE" | jq -r .id)
BUCKET=$(echo "$RESPONSE" | jq -r .links.bucket)

echo "Deposition ID : $DEPOSITION_ID"
echo "Bucket URL    : $BUCKET"
echo "Reserved DOI  : $(echo "$RESPONSE" | jq -r .metadata.prereserve_doi.doi)"
echo "Edit in UI    : $(echo "$RESPONSE" | jq -r .links.html)"
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
echo "Files now in deposition ${DEPOSITION_ID}:"
curl -sS -H "$AUTH" \
    "${ZENODO_ENDPOINT}/api/deposit/depositions/${DEPOSITION_ID}/files" \
    | jq '.[] | {filename, filesize, checksum}'

if [ "$FAILED" -ne 0 ]; then
    echo "One or more uploads FAILED — do not publish yet." >&2
    exit 1
fi
echo "All uploads complete."
