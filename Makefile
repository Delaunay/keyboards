


install:
	uv tool install zmk
	cd ergogen && npm i

v2:
	node src/cli.js v2/config.yaml -o v2/

v3:
	node ergogen/src/cli.js split/v3 -o split/v3 --svg
