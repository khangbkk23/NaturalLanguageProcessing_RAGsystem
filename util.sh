#!/bin/bash

STUDENT_ID="2311402"
IMAGE_NAME="kelvincook_nlp"
PROJ_P_LANG="python"

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
S_OUT="$BASE_DIR/output"
S_IN="$BASE_DIR/input"

function check_requirements {
    if [ ! -f "$BASE_DIR/$PROJ_P_LANG/requirements.txt" ]; then
        touch "$BASE_DIR/$PROJ_P_LANG/requirements.txt"
    fi
    mkdir -p "$S_OUT"
}

function run_interactive {
    echo "--- [MODE 1] INTERACTIVE MODE ---"
    check_requirements
    
    (
        cd "$BASE_DIR/$PROJ_P_LANG" || exit
        docker build -t $IMAGE_NAME .
        
        echo ">> Starting Container..."
        docker run -it --rm \
            -v "$S_OUT":/src/output \
            -v "$S_IN":/src/input \
            $IMAGE_NAME
    )
}

function run_batch {
    echo "--- [MODE 2] BATCH PROCESSING ---"
    check_requirements
    
    (
        cd "$BASE_DIR/$PROJ_P_LANG" || exit
        docker build -t $IMAGE_NAME .
        
        echo ">> Auto-running Batch Mode..."
        echo "2" | docker run -i --rm \
            -v "$S_OUT":/src/output \
            -v "$S_IN":/src/input \
            $IMAGE_NAME
    )
    echo ">> DONE. Result: $S_OUT"
}

function run_submit {
    echo "--- PREPARING SUBMISSION ---"
    
    if ! command -v zip &> /dev/null; then
        echo "Error: 'zip' is not installed."
        return
    fi

    run_batch
    
    echo ">> Zipping files..."
    rm -f "${STUDENT_ID}.zip"
    
    (
        cd "$BASE_DIR" || exit
        zip -r "${STUDENT_ID}.zip" \
            python/ \
            input/ \
            output/ \
            util.sh \
            README.md
    )
        
    echo ">> SUCCEEDED: ${STUDENT_ID}.zip created."
}

function show_help {
    echo "USAGE:"
    echo "  ./util.sh interactive"
    echo "  ./util.sh batch"
    echo "  ./util.sh submit"
}

if [[ "$1" == "interactive" ]]; then
    run_interactive
elif [[ "$1" == "batch" ]]; then
    run_batch
elif [[ "$1" == "submit" ]]; then
    run_submit
else
    show_help
fi