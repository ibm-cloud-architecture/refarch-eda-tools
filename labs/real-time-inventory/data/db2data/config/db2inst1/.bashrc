# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions

# The following three lines have been added by UDB DB2.
if [ -f /database/config/db2inst1/sqllib/db2profile ]; then
    . /database/config/db2inst1/sqllib/db2profile
fi


