#!/bin/bash

STUDENT_ID="2311402"
IMAGE_NAME="kelvincook_nlp"
PROJ_P_LANG="python"
BASE_DIR=$(pwd)
S_OUT="$BASE_DIR/output"
S_IN="$BASE_DIR/input"

if [ ! -f "$PROJ_P_LANG/requirements.txt" ]; then
    touch "$PROJ_P_LANG/requirements.txt"
fi

function run_ { 
    echo "HƯỚNG DẪN SỬ DỤNG:"
    echo "  ./util.sh interactive  : Chạy chế độ tương tác (Nhập tay)"
    echo "  ./util.sh batch        : Chạy chế độ tự động (Đọc file input)"
    echo "  ./util.sh submit       : Chạy Batch 1 lần rồi nén file nộp bài"
}

function run_interactive {
    echo "--- [MODE 1] INTERACTIVE MODE ---"
    mkdir -p "$S_OUT"
    
    cur=`pwd`
    cd $PROJ_P_LANG
    
    echo ">> 1. Building Docker image..."
    docker build -t $IMAGE_NAME .
    
    echo ">> 2. Starting Container..."
    echo "   (Vui lòng nhập '1' khi chương trình hỏi chọn chế độ)"
    docker run -it --rm \
        -v "$S_OUT":/src/output \
        -v "$S_IN":/src/input \
        $IMAGE_NAME
    
    cd $cur
}

function run_batch {
    echo "--- [MODE 2] BATCH PROCESSING ---"
    mkdir -p "$S_OUT"
    
    cur=`pwd`
    cd $PROJ_P_LANG
    
    echo ">> 1. Building Docker image..."
    docker build -t $IMAGE_NAME .
    echo ">> 2. Auto-running Batch Mode..."
    echo "2" | docker run -i --rm \
        -v "$S_OUT":/src/output \
        -v "$S_IN":/src/input \
        $IMAGE_NAME
    
    cd $cur
    echo ">> DONE. Kết quả đã được lưu tại: $S_OUT"
}

function run_submit {
    echo "--- PREPARING SUBMISSION ---"
    
    if ! command -v zip &> /dev/null; then
        echo "Error: 'zip' is not installed."
        return
    fi

    echo ">> STEP 1: Running Batch Mode to generate latest output..."
    run_batch
    echo ">> STEP 2: Zipping files..."
    rm -f "${STUDENT_ID}.zip"
    
    zip -r "${STUDENT_ID}.zip" \
        python/ \
        input/ \
        output/ \
        util.sh \
        README.md
        
    echo ">> SUCCEEDED: ${STUDENT_ID}.zip created."
}

if [[ "$1" == "interactive" || "$1" == "batch" || "$1" == "submit" ]]; then
    run_$1 "${@:2}"
else
    run_
fi