#!/bin/bash
# SSD Performance Benchmark Script
# Tests sequential and random read/write performance

set -e

# Configuration
TEST_DIR="${1:-./ssd_benchmark_test}"
TEST_SIZE="${2:-1G}"
BLOCK_SIZE="${3:-4k}"
NUM_JOBS=4

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Results storage
RESULT_SEQ_WRITE="N/A"
RESULT_SEQ_READ="N/A"
RESULT_RAND_READ_IOPS="N/A"
RESULT_RAND_READ_BW="N/A"
RESULT_RAND_WRITE_IOPS="N/A"
RESULT_RAND_WRITE_BW="N/A"
RESULT_MIXED_READ_IOPS="N/A"
RESULT_MIXED_WRITE_IOPS="N/A"
RESULT_LATENCY="N/A"

# Helper function to format bytes to human readable
format_speed() {
    local bytes=$1
    if (( bytes >= 1073741824 )); then
        printf "%.2f GB/s" "$(echo "scale=2; $bytes / 1073741824" | bc)"
    elif (( bytes >= 1048576 )); then
        printf "%.2f MB/s" "$(echo "scale=2; $bytes / 1048576" | bc)"
    else
        printf "%.2f KB/s" "$(echo "scale=2; $bytes / 1024" | bc)"
    fi
}

# Rating function
get_rating() {
    local value=$1
    local type=$2

    case $type in
        seq_read)
            if (( value >= 5000 )); then echo "Excellent"
            elif (( value >= 3000 )); then echo "Very Good"
            elif (( value >= 1000 )); then echo "Good"
            elif (( value >= 500 )); then echo "Average"
            else echo "Below Average"
            fi
            ;;
        seq_write)
            if (( value >= 4000 )); then echo "Excellent"
            elif (( value >= 2000 )); then echo "Very Good"
            elif (( value >= 500 )); then echo "Good"
            elif (( value >= 200 )); then echo "Average"
            else echo "Below Average"
            fi
            ;;
        rand_iops)
            if (( value >= 100000 )); then echo "Excellent"
            elif (( value >= 50000 )); then echo "Very Good"
            elif (( value >= 10000 )); then echo "Good"
            elif (( value >= 1000 )); then echo "Average"
            else echo "Below Average"
            fi
            ;;
        latency)
            if (( value <= 100 )); then echo "Excellent"
            elif (( value <= 500 )); then echo "Very Good"
            elif (( value <= 1000 )); then echo "Good"
            elif (( value <= 5000 )); then echo "Average"
            else echo "Below Average"
            fi
            ;;
    esac
}

print_header() {
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}┃${NC}${BOLD}                        SSD PERFORMANCE BENCHMARK                          ${NC}${CYAN}┃${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_header
echo ""
echo -e "  ${BOLD}Test Directory:${NC} $TEST_DIR"
echo -e "  ${BOLD}Test Size:${NC}      $TEST_SIZE"
echo -e "  ${BOLD}Block Size:${NC}     $BLOCK_SIZE"
echo ""

# Create test directory
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# Check for required tools
check_tool() {
    if command -v "$1" &> /dev/null; then
        echo -e "  ${GREEN}✓${NC} $1"
        return 0
    else
        echo -e "  ${YELLOW}✗${NC} $1 (not installed)"
        return 1
    fi
}

echo -e "${BOLD}Checking tools:${NC}"
if command -v fio &> /dev/null; then
    HAS_FIO=1
    echo -e "  ${GREEN}✓${NC} fio"
else
    HAS_FIO=0
    echo -e "  ${YELLOW}✗${NC} fio (not installed)"
fi

if command -v ioping &> /dev/null; then
    HAS_IOPING=1
    echo -e "  ${GREEN}✓${NC} ioping"
else
    HAS_IOPING=0
    echo -e "  ${YELLOW}✗${NC} ioping (not installed)"
fi

echo -e "  ${GREEN}✓${NC} dd"
echo ""

# Function to clean up test files
cleanup() {
    rm -f testfile* latency_test *.fio 2>/dev/null || true
    rmdir "$TEST_DIR" 2>/dev/null || true
}
trap cleanup EXIT

# ============================================
# Test 1: Sequential Write (dd)
# ============================================
echo -e "${BLUE}[1/5]${NC} ${BOLD}Sequential Write Test${NC} (1GB file)"
echo -n "      Running... "

if [[ "$OSTYPE" == "darwin"* ]]; then
    output=$(dd if=/dev/zero of=testfile_seq bs=1m count=1024 2>&1)
    sync
else
    output=$(dd if=/dev/zero of=testfile_seq bs=1M count=1024 oflag=direct 2>&1)
    sync
fi

# Parse dd output for bytes/sec
bytes_per_sec=$(echo "$output" | grep -oE '[0-9]+ bytes/sec' | grep -oE '[0-9]+' || echo "0")
if [[ -z "$bytes_per_sec" || "$bytes_per_sec" == "0" ]]; then
    # Try macOS format: (1.2 GB/s)
    bytes_per_sec=$(echo "$output" | grep -oE '\([0-9.]+ [A-Z]+/s' | grep -oE '[0-9.]+' | head -1 || echo "")
    unit=$(echo "$output" | grep -oE '\([0-9.]+ [A-Z]+/s' | grep -oE '[A-Z]+/s' | head -1 || echo "")
    # Try Linux format: 1.2 GB/s (at end of line, no parentheses)
    if [[ -z "$bytes_per_sec" ]]; then
        bytes_per_sec=$(echo "$output" | grep -oE '[0-9.]+ [GMKT]B/s' | grep -oE '[0-9.]+' | head -1 || echo "")
        unit=$(echo "$output" | grep -oE '[0-9.]+ [GMKT]B/s' | grep -oE '[A-Z]+/s' | head -1 || echo "")
    fi
    if [[ -n "$bytes_per_sec" && -n "$unit" ]]; then
        case $unit in
            "GB/s") bytes_per_sec=$(echo "$bytes_per_sec * 1073741824" | bc | cut -d. -f1) ;;
            "MB/s") bytes_per_sec=$(echo "$bytes_per_sec * 1048576" | bc | cut -d. -f1) ;;
            "KB/s") bytes_per_sec=$(echo "$bytes_per_sec * 1024" | bc | cut -d. -f1) ;;
            *) bytes_per_sec="0" ;;
        esac
    else
        bytes_per_sec="0"
    fi
fi

RESULT_SEQ_WRITE=$(format_speed "$bytes_per_sec")
RESULT_SEQ_WRITE_RAW=$((bytes_per_sec / 1048576))
echo -e "${GREEN}Done${NC} - $RESULT_SEQ_WRITE"

# ============================================
# Test 2: Sequential Read (dd)
# ============================================
echo -e "${BLUE}[2/5]${NC} ${BOLD}Sequential Read Test${NC} (1GB file)"
echo -n "      Running... "

# Clear cache if possible
if [[ "$OSTYPE" == "darwin"* ]]; then
    sudo purge 2>/dev/null || true
    output=$(dd if=testfile_seq of=/dev/null bs=1m 2>&1)
else
    echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null 2>&1 || true
    output=$(dd if=testfile_seq of=/dev/null bs=1M iflag=direct 2>&1)
fi

bytes_per_sec=$(echo "$output" | grep -oE '[0-9]+ bytes/sec' | grep -oE '[0-9]+' || echo "0")
if [[ -z "$bytes_per_sec" || "$bytes_per_sec" == "0" ]]; then
    # Try macOS format: (1.2 GB/s)
    bytes_per_sec=$(echo "$output" | grep -oE '\([0-9.]+ [A-Z]+/s' | grep -oE '[0-9.]+' | head -1 || echo "")
    unit=$(echo "$output" | grep -oE '\([0-9.]+ [A-Z]+/s' | grep -oE '[A-Z]+/s' | head -1 || echo "")
    # Try Linux format: 1.2 GB/s (at end of line, no parentheses)
    if [[ -z "$bytes_per_sec" ]]; then
        bytes_per_sec=$(echo "$output" | grep -oE '[0-9.]+ [GMKT]B/s' | grep -oE '[0-9.]+' | head -1 || echo "")
        unit=$(echo "$output" | grep -oE '[0-9.]+ [GMKT]B/s' | grep -oE '[A-Z]+/s' | head -1 || echo "")
    fi
    if [[ -n "$bytes_per_sec" && -n "$unit" ]]; then
        case $unit in
            "GB/s") bytes_per_sec=$(echo "$bytes_per_sec * 1073741824" | bc | cut -d. -f1) ;;
            "MB/s") bytes_per_sec=$(echo "$bytes_per_sec * 1048576" | bc | cut -d. -f1) ;;
            "KB/s") bytes_per_sec=$(echo "$bytes_per_sec * 1024" | bc | cut -d. -f1) ;;
            *) bytes_per_sec="0" ;;
        esac
    else
        bytes_per_sec="0"
    fi
fi

RESULT_SEQ_READ=$(format_speed "$bytes_per_sec")
RESULT_SEQ_READ_RAW=$((bytes_per_sec / 1048576))
echo -e "${GREEN}Done${NC} - $RESULT_SEQ_READ"

rm -f testfile_seq

# ============================================
# FIO Tests (if available)
# ============================================
if [[ "$HAS_FIO" == "1" ]]; then

    # Test 3: Random Read (4K)
    echo -e "${BLUE}[3/5]${NC} ${BOLD}Random Read 4K Test${NC} (30 seconds)"
    echo -n "      Running... "

    fio_output=$(fio --name=rand_read \
        --ioengine=posixaio \
        --rw=randread \
        --bs=4k \
        --size=256M \
        --numjobs=$NUM_JOBS \
        --time_based \
        --runtime=30 \
        --group_reporting \
        --output-format=json \
        --filename=testfile_fio 2>/dev/null)

    RESULT_RAND_READ_IOPS=$(echo "$fio_output" | python3 -c "import sys,json; d=json.load(sys.stdin); print(int(d['jobs'][0]['read']['iops']))" 2>/dev/null || echo "0")
    RESULT_RAND_READ_BW=$(echo "$fio_output" | python3 -c "import sys,json; d=json.load(sys.stdin); print(round(d['jobs'][0]['read']['bw']/1024, 2))" 2>/dev/null || echo "0")

    echo -e "${GREEN}Done${NC} - ${RESULT_RAND_READ_IOPS} IOPS (${RESULT_RAND_READ_BW} MB/s)"
    rm -f testfile_fio

    # Test 4: Random Write (4K)
    echo -e "${BLUE}[4/5]${NC} ${BOLD}Random Write 4K Test${NC} (30 seconds)"
    echo -n "      Running... "

    fio_output=$(fio --name=rand_write \
        --ioengine=posixaio \
        --rw=randwrite \
        --bs=4k \
        --size=256M \
        --numjobs=$NUM_JOBS \
        --time_based \
        --runtime=30 \
        --group_reporting \
        --output-format=json \
        --filename=testfile_fio 2>/dev/null)

    RESULT_RAND_WRITE_IOPS=$(echo "$fio_output" | python3 -c "import sys,json; d=json.load(sys.stdin); print(int(d['jobs'][0]['write']['iops']))" 2>/dev/null || echo "0")
    RESULT_RAND_WRITE_BW=$(echo "$fio_output" | python3 -c "import sys,json; d=json.load(sys.stdin); print(round(d['jobs'][0]['write']['bw']/1024, 2))" 2>/dev/null || echo "0")

    echo -e "${GREEN}Done${NC} - ${RESULT_RAND_WRITE_IOPS} IOPS (${RESULT_RAND_WRITE_BW} MB/s)"
    rm -f testfile_fio

else
    echo -e "${BLUE}[3/5]${NC} ${YELLOW}Random Read 4K Test - SKIPPED (fio not installed)${NC}"
    echo -e "${BLUE}[4/5]${NC} ${YELLOW}Random Write 4K Test - SKIPPED (fio not installed)${NC}"
fi

# ============================================
# Latency Test
# ============================================
echo -e "${BLUE}[5/5]${NC} ${BOLD}I/O Latency Test${NC}"
echo -n "      Running... "

if [[ "$HAS_IOPING" == "1" ]]; then
    latency_output=$(ioping -c 20 . 2>&1)
    # Parse ioping output - format: "min/avg/max/mdev = 4 us / 8.75 us / 12 us / 3.11 us"
    avg_line=$(echo "$latency_output" | grep -E 'min/avg/max')
    RESULT_LATENCY=$(echo "$avg_line" | awk -F'/' '{print $6}' | sed 's/^ *//' | awk '{print $1 " " $2}' || echo "N/A")
    RESULT_LATENCY_RAW=$(echo "$avg_line" | awk -F'/' '{print $6}' | grep -oE '[0-9.]+' | head -1 || echo "0")
else
    total=0
    for i in {1..10}; do
        start=$(python3 -c "import time; print(int(time.time()*1000000))")
        dd if=/dev/zero of=latency_test bs=4k count=1 conv=fsync 2>/dev/null
        end=$(python3 -c "import time; print(int(time.time()*1000000))")
        latency=$((end - start))
        total=$((total + latency))
        rm -f latency_test
    done
    RESULT_LATENCY_RAW=$((total / 10))
    if (( RESULT_LATENCY_RAW >= 1000 )); then
        RESULT...