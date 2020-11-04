#!/bin/bash

exec /usr/bin/R -e "library(nzrserver); nzrserver:::dispatcher()"

exit

