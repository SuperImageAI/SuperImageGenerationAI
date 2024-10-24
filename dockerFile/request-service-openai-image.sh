#!/bin/bash

# Function to display usage
usage() {
    echo "Usage: $0 <model>"
    echo "Options:"
    echo "-h, --help        Display this help message"
}

# Check if no arguments were passed
if [ $# -eq 0 ]; then
    echo "No arguments provided"
    usage
    exit 1
fi

# Parse command-line arguments
while (( "$#" )); do
    case "$1" in
        -h|--help)
            usage
            exit 0
            ;;
        --) # end argument parsing
            shift
            break
            ;;
        -*|--*=) # unsupported flags
            echo "Error: Unsupported flag $1" >&2
            usage
            exit 1
            ;;
        *) # preserve positional arguments
            MODEL="$1"
            shift
            ;;
    esac
done

curl http://127.0.0.1:1042/v1/images/generations \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A cat holding a sign that says hello world",
    "size": "1024x1024"
  }'
