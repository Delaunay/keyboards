


install:
	uv tool install zmk
	cd ergogen && npm i

v2:
	node src/cli.js v2/config.yaml -o v2/

v3:
	node src/cli.js v3/config.yaml -o v3/
