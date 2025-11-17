#!/bin/bash

STUDENT_ID="2311402"
IMAGE_NAME="nlp_assignment"
PROJ_P_LANG="python"

BASE_DIR=$(pwd)
S_OUT="$BASE_DIR/$STUDENT_ID/output"
S_IN="$BASE_DIR/input"

function run_ { 
    echo "Usage: ./util.sh [parse|generate|submit]" 
    echo "  parse    : Run Earley parser with Docker"
    echo "  generate : Generate sentences with Docker"
    echo "  submit   : Package the project for submission"
}

function run_parse {
    echo "--- RUNNING PARSER TASK (DOCKER) ---"
    mkdir -p "$S_OUT"
    
    cur=`pwd`
    
    cd $PROJ_P_LANG
    echo "Building Docker image..."
    docker build -t $IMAGE_NAME .
    docker run --rm -v "$S_OUT":/src/output -v "$S_IN":/src/input $IMAGE_NAME
    cd $cur
    echo "Done. Please check output in: $S_OUT"
}

function run_generate {
    echo "--- RUNNING GENERATOR TASK ---"
    mkdir -p "$S_OUT"
    
    cur=`pwd`
    
    cd $PROJ_P_LANG
    docker build -t $IMAGE_NAME .
    
    docker run --rm -v "$S_OUT":/src/output -v "$S_IN":/src/input $IMAGE_NAME python3 -m hcmut.iaslab.nlp.app.main generate
    
    cd $cur
    echo "Done. Please check output in: $S_OUT"
}

function run_submit {
    echo "--- MAKING SUBMISSION FILE ---"
    
    if ! command -v zip &> /dev/null; then
        echo "Error: 'zip' is not installed. Please install it (sudo apt install zip)."
        return
    fi

    run_generate
    run_test
    
    cp python/hcmut/iaslab/nlp/data/grammar.txt "$S_OUT/"
    
    zip -r "${STUDENT_ID}.zip" python/ input/ "$STUDENT_ID/output/" util.sh README.md
    
    echo "Created: ${STUDENT_ID}.zip"
}

run_$1 "${@:2}"