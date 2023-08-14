#!/bin/bash

# This script will compile all exercises in this folder
find . -type d -exec make -C {} \;
