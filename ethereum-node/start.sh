#!/bin/bash

# launch worlds smallest webserver serving `contracts.json` in the background
while true; do { echo -ne "HTTP/1.0 200 OK\r\n\r\n"; cat /contracts.json; } | nc -l -p 8000; done &

# launch worlds smallest webserver serving `api.json` in the background
while true; do { echo -ne "HTTP/1.0 200 OK\r\n\r\n"; cat /api.json; } | nc -l -p 8001; done &

# launch parity in the foreground
/parity/parity \
	--chain dev \
	--gasprice 2 \
	--no-discovery \
	--force-ui --ui-no-validation --ui-interface 0.0.0.0 \
	--jsonrpc-interface all --jsonrpc-cors "*" --jsonrpc-hosts all --jsonrpc-apis web3,eth,net,personal,parity,parity_set,traces,rpc,parity_accounts \
	--unlock 0x00a329c0648769a73afac7f9381e08fb43dbea72 --password /parity/password
