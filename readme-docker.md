# Docker - Youtube Auto Archiver

Dockerized version of my [Youtube Auto Archiver](https://github.com/aziascreations/Youtube-Auto-Archiver) project.

## Warning

The container is running the application as root which may be dangerous if you improperly configure the app as it is vulnerable to 
[command injection attacks](https://owasp.org/www-community/attacks/Command_Injection) if its config file is messed with.<br>
This **will** be fixed once I know how to set that up properly in the Dockerfile.

The Python module named "*[lxml](https://lxml.de/)*" fails to compile, but streamlink will work regardless since it is installed via the
"*[py3-lxml](https://pkgs.alpinelinux.org/packages?name=py3-lxml)*" package.

## Installation

Simply clone this repository using the following command:<br>
`git clone --recurse-submodules https://github.com/aziascreations/Docker-Youtube-Auto-Archiver`

And run *docker compose* like so in the cloned directory:
`docker-compose up`

## Configuration

For information on how to configure the app, check the relevant section on the project's readme.

For information regarding the configuration of this container, all you have to do is change the `/data` volume if you need it in a specific location.

Please note that the [docker-compose.yml](docker/docker-compose.yml) files already has its environment variables set, as well as an independent config file setup.

## License

[Unlicense](LICENSE)
