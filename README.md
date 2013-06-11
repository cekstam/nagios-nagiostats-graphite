misc
====

Various tools and scripts

nagiosStats.py
=============

A script to pull metrics from nagiostats (shipped with Nagios) and send to Graphite.
The metrics are included in a dictionary within the script, and stored in Graphite using more readable names.

To use: put the script somewhere, chmod +x on it, change carbonServer within the script, verify the location of nagiostats, then add a cron job to call it (I use every 60s).

TODO: Frontend for viewing them in a pretty dashboard
