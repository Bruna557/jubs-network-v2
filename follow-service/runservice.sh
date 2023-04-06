#! /bin/bash

python3 -m app.app &

python3 -m event-subscriber.subscribers
