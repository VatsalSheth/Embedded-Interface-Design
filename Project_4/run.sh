#!/bin/bash

cd `dirname $0`
node AWS_Node.js &
python3 Server.py


