FROM ethcore/parity:v1.6.5

# install all dependencies
RUN apt-get update \
	&& apt-get install --yes --no-install-recommends curl python python-pip pkg-config python-dev autoconf automake libtool libssl-dev make g++ jq \
	&& rm -rf /var/lib/apt/lists/*

# create the master account
RUN /parity/parity daemon /parity/parity.pid --chain dev --no-ui --no-dapps --no-discovery --jsonrpc-apis web3,eth,net,personal,parity,parity_set,traces,rpc,parity_accounts \
	&& while ! curl --silent --show-error -H "Content-Type: application/json" -X POST --data '{"jsonrpc":"2.0","method":"parity_newAccountFromPhrase","params":["",""],"id": 1}' localhost:8545; do sleep 0.1; done \
	&& kill -s TERM `cat /parity/parity.pid` \
	&& while kill -0 `cat /parity/parity.pid`; do sleep 0.01; done \
	&& rm /parity/parity.pid \
	&& echo "" > /parity/password

# install pip dependencies
RUN mkdir /temp \
	&& curl --location --silent --show-error --output /temp/requirements-load.txt https://raw.githubusercontent.com/AugurProject/augur-core/master/load_contracts/requirements-load.txt \
	&& pip install -r /temp/requirements-load.txt \
	&& pip install https://github.com/ethereum/serpent/tarball/master \
	&& rm -rf /temp

WORKDIR /
COPY generate-contracts-json.py /temp/load_contracts/generate-contracts-json.py
RUN mkdir augur-core \
	&& cd augur-core \
	# download the contracts
	&& curl -L https://api.github.com/repos/AugurProject/augur-core/tarball/master | tar xz --strip=1 \
	&& rm load_contracts/build.json \
	&& mv /temp/load_contracts/generate-contracts-json.py /augur-core/load_contracts/generate-contracts-json.py \
	&& rm -rf /temp \
	# launch parity with the master account unlocked
	&& /parity/parity daemon /parity/parity.pid --chain dev --no-ui --no-dapps --no-discovery --jsonrpc-apis web3,eth,net,personal,parity,parity_set,traces,rpc,parity_accounts --unlock 0x00a329c0648769a73afac7f9381e08fb43dbea72 --password /parity/password \
	&& while ! curl --silent --show-error -H "Content-Type: application/json" -X POST --data '{"jsonrpc":"2.0","method":"net_version","id": 1}' localhost:8545; do sleep 0.1; done \
	# send a transaction with gasPrice of 1 so contracts are submitted with gas price set which will result in eth_gasPrice returning that value
	&& while ! curl --silent --show-error -H "Content-Type: application/json" -X POST --data '{"jsonrpc":"2.0","method":"eth_sendTransaction","params": [{"from":"0x00a329c0648769a73afac7f9381e08fb43dbea72","to":"0x00a329c0648769a73afac7f9381e08fb43dbea72","gasPrice":"0x1","value":"0x0"}],"id": 1}' localhost:8545; do sleep 0.1; done \
	# load the contracts and generate contracts/api json files
	&& python load_contracts/load_contracts.py --verbosity 1 --blocktime 0.1 \
	&& python /augur-core/load_contracts/generate-contracts-json.py \
	&& python /augur-core/load_contracts/make_api.py -o /api.json \
	# set the default augur branch
	&& curl --silent --show-error localhost:8545 -H "Content-Type: application/json" -X POST --data '{"id":2,"jsonrpc":"2.0","method":"eth_call","params":[{"to":'`jq '.Branches' /contracts.json`',"data":"0x29cef8a2","gas":"0x2fd618"},"latest"]}' \
	&& kill -s TERM `cat /parity/parity.pid` \
	&& while kill -0 `cat /parity/parity.pid`; do sleep 0.01; done \
	&& rm /parity/parity.pid \
	&& cd .. \
	&& rm -rf augur-core

COPY start.sh /start.sh
RUN chmod +x /start.sh
ENTRYPOINT ["/start.sh"]

# docker build --tag ethereum-node .
# docker run --rm -it -p 8000:8000 -p 8001:8001 -p 8545:8545 -p 8180:8180 ethereum-node
