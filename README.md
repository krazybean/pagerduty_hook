pagerduty_hook
==============

Getting around internal endpoint for pagerduty hooks

Quick usage:

    curl -X POST -d '{"data": "test"}' http://hostname:port/pagerduty

 *sets data into the queue*


To pull data off the queue:

    curl -X GET http://hostname:port/heartbeat

dats it :/
