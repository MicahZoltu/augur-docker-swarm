FROM node:6

# hack to workaround https://github.com/npm/npm/issues/13306
RUN cd $(npm root -g)/npm \
	&& npm install fs-extra \
	&& sed -i -e s/graceful-fs/fs-extra/ -e s/fs.rename/fs.move/ ./lib/utils/rename.js

# workaround for https://github.com/yarnpkg/yarn/issues/2266
RUN yarn global add node-gyp

# we need this so we can compile the TypeScript modules
RUN yarn global add typescript

WORKDIR /source

# download all repositories; allow user to specify a particular branch/sha with `docker build --build-arg augur_commit=my-branch`; defaults to master
ARG ethereumjs_blockstream_commit=master
RUN mkdir ethereumjs-blockstream \
	&& curl --silent --show-error -L https://api.github.com/repos/ethereumjs/ethereumjs-blockstream/tarball/$ethereumjs_blockstream_commit | tar xz --strip=1 -C ethereumjs-blockstream

ARG augur_abi_commit=master
RUN mkdir augur-abi \
	&& curl --silent --show-error -L https://api.github.com/repos/AugurProject/augur-abi/tarball/$augur_abi_commit | tar xz --strip=1 -C augur-abi

ARG augur_contracts_commit=master
RUN mkdir augur-contracts \
	&& curl --silent --show-error -L https://api.github.com/repos/AugurProject/augur-contracts/tarball/$augur_contracts_commit | tar xz --strip=1 -C augur-contracts

ARG ethereumjs_ledger_commit=master
RUN mkdir ethereumjs-ledger \
	&& curl --silent --show-error -L https://api.github.com/repos/ethereumjs/ethereumjs-ledger/tarball/$ethereumjs_ledger_commit | tar xz --strip=1 -C ethereumjs-ledger

ARG ethrpc_commit=master
RUN mkdir ethrpc \
	&& rm -rf dist \
	&& curl --silent --show-error -L https://api.github.com/repos/ethereumjs/ethrpc/tarball/$ethrpc_commit | tar xz --strip=1 -C ethrpc

ARG ethereumjs_connect_commit=master
RUN mkdir ethereumjs-connect \
	&& rm -rf dist \
	&& curl --silent --show-error -L https://api.github.com/repos/ethereumjs/ethereumjs-connect/tarball/$ethereumjs_connect_commit | tar xz --strip=1 -C ethereumjs-connect

ARG augur_js_commit=master
RUN mkdir augur.js \
	&& rm -rf dist \
	&& curl --silent --show-error -L https://api.github.com/repos/AugurProject/augur.js/tarball/$augur_js_commit | tar xz --strip=1 -C augur.js

ARG augur_commit=master
RUN mkdir augur \
	&& curl --silent --show-error -L https://api.github.com/repos/AugurProject/augur/tarball/$augur_commit | tar xz --strip=1 -C augur \
	&& cd augur \
	# remove shared-git-hooks NPM module from augur, as we don't have a .git directory so they won't work
	&& npm uninstall --save-dev shared-git-hooks \
	# remove augur yarn lock as it breaks yarn link
	&& rm yarn.lock \
	# remove augur build directory, we want to make sure this build is clean
	&& rm -rf build

# yarn link and install everything
RUN cd ethereumjs-ledger \
	&& yarn install \
	&& tsc \
	&& yarn link
RUN cd ethereumjs-blockstream \
	&& yarn install \
	&& tsc \
	&& yarn link
RUN cd augur-abi \
	&& yarn link
RUN cd augur-contracts \
	&& yarn link
RUN cd ethrpc \
	&& yarn link ethereumjs-blockstream \
	&& yarn link augur-abi \
	&& yarn link
RUN cd ethereumjs-connect \
	&& yarn link ethrpc \
	&& yarn link
RUN cd augur.js \
	&& yarn link augur-abi \
	&& yarn link augur-contracts \
	&& yarn link ethereumjs-ledger \
	&& yarn link ethrpc \
	&& yarn link ethereumjs-connect \
	&& yarn link
RUN cd augur \
	&& yarn install \
	&& yarn link augur.js \
	# workaround for https://github.com/yarnpkg/yarn/issues/3048
	&& yarn link ethereumjs-connect \
	&& yarn link ethrpc \
	&& yarn link augur-contracts \
	&& yarn link augur-abi \
	&& yarn link ethereumjs-blockstream \
	&& yarn link ethereumjs-ledger

# setup the environment to run in and build augur UI
COPY env.json /source/augur/src/env.json

WORKDIR /source/augur

RUN { echo -n 'debugger;\n'; cat /source/augur/src/main.jsx; } > /source/augur/src/main.jsx.new && mv /source/augur/src/main.jsx.new /source/augur/src/main.jsx
# RUN yarn run build

ENTRYPOINT while ! curl --silent --show-error ethereum-node:8545 -H "Content-Type: application/json" -X POST --data '{"jsonrpc":"2.0","method":"net_version","id": 1}'; do sleep 0.1; done \
	&& curl --silent --show-error -o /source/augur-contracts/contracts.json http://ethereum-node:8000 \
	&& curl --silent --show-error -o /source/augur-contracts/api.json http://ethereum-node:8001 \
	# unfortunately, we can't build until runtime because we need to get the contracts.json and api.json from another service
	# TODO: make it so augur can be configured to dynamically pull in contracts.json and api.json client-side rather than compiling them in
	&& yarn run build dev \
	&& yarn run start
