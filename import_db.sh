#!/bin/bash

mysql -u $1 -h $2 -p$3 $4 < $5
