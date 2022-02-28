# Youtube Auto Archiver <sub><sup>v0.7.0</sup></sub>
A simple and yet highly configurable Python application that automatically checks if a Youtuber is streaming,
and downloads said streams while also archiving its latest uploads.

The application will be improved as I have time to do so, or if you raise an issue when I have time to look into it.

## Warning
Due to the way some commands are executed, it is possible to have a
[command injection vulnerability](https://owasp.org/www-community/attacks/Command_Injection)
if you mess up or leave the config file editable by everyone.<br><!--This problem **can be mitigated** if you set up the appropriate [environment variables ](#environment-variables).-->
This might be fixed in the future, but don't count on it as this project is a personal one.

The Python module named "*[lxml](https://lxml.de/)*" may fail to compile, but streamlink will work regardless since 
it is installed via the "*[py3-lxml](https://pkgs.alpinelinux.org/packages?name=py3-lxml)*" package.

The application isn't designed to be used by another one as a module.

## Features
* General
  * Can run on Windows and Linux (*Tested on x64 and ARMv8*)
  * Relatively high level of configurability.
* YouTube
  * Automatic livestream download through <code>https://youtube.com/c/.../live</code>
  * Automatic livestream thumbnail and description download.
  * Automatic download of uploads and their metadata.
  * Configurable delays, actions, locations per channel.
* Planned for v1.0.0
  * Native support for cookies for *yt-dlp* and maybe *streamlink*.
  * Better support to prevent command injection.  (Will block some features if used)
* Planned for later
  * Using TOML for the config file only Python 3.11 is released and stable.

## Requirements
* [Python](https://www.python.org/) >= v3.9, < v3.11 <sub><sup>(Preferably)</sup></sub>
* [Streamlink](https://streamlink.github.io/) >= v3.1.1, < v4.\*.\*
* [yt-dlp](https://github.com/yt-dlp/yt-dlp) >= v2022.02.04

The application may work just fine with older or newer versions of these pieces of software, but they will not be supported.<br>
All requirements, except for *Python*, can be installed via *pip* or manually.

## Installation

### Standalone
1. Clone the repository and enter it
```bash
git clone https://github.com/aziascreations/Youtube-Auto-Archiver.git
cd Youtube-Auto-Archiver
```

2. If desired, setup a Python virtual environment
```bash
pip install --upgrade virtualenv
python -m venv ./venv
```
* Linux:
```bash
source venv/bin/activate
```
* Windows:
```bash
venv\Scripts\activate
```

3. Install the required Python modules
```bash
pip install -r requirements.txt
```
<sup>Please note that *streamlink* may need to be compiled when installed via *pip*.<br>
You can ignore it as long as the executable is accessible in the *PATH* environment variable.</sup>

3. Configure the application's config file
4. Run the application

### Docker
1. Clone the repository and enter it
```bash
git clone https://github.com/aziascreations/Youtube-Auto-Archiver.git
cd Youtube-Auto-Archiver
```

2. Configure the [docker-compose.yml](docker-compose.yml) file.

<sup>If you are running Docker on Windows, or on a NTFS mount under Linux, you may need to run the application as
root since the output volume binding's permissions can't be properly configured.</sup>

3. Build the container via *docker-compose*
```bash
docker-compose up --build
```

## Configuration
For information on how to configure the app, check the relevant section on the project's readme.

For information regarding the configuration of this container, all you have to do is change the `/data` volume if you need it in a specific location.

Please note that the [docker-compose.yml](docker/docker-compose.yml) files already has its environment variables set, as well as an independent config file setup.

## Config
The config is stored in [config.json](config.json) and has to be in the same folder as [app.py](app.py), unless the
appropriate [environment variables](#environment-variables) tells the application to look elsewhere for it.

Please refer to [config.md](config.md) for more information on the config file and its fields.

## Build Arguments *(Docker)*
<table>
    <tr>
        <th style="width:25%">Variable</th>
        <th style="width:20%">Type</th>
        <th style="width:50%">Remark</th>
        <th style="width:5%">Default</th>
    </tr>
    <tr>
        <td>BUID</td>
        <td>Integer</td>
        <td>User ID under which the app runs and who owns the app's directory.<br>May not work on Windows and NTFS volumes !</td>
        <td><code>1000</code></td>
    </tr>
    <tr>
        <td>BGID</td>
        <td>Integer</td>
        <td>Group ID under which the app runs and who owns the app's directory.<br>May not work on Windows and NTFS volumes !</td>
        <td><code>1000</code></td>
    </tr>
</table>

## Environment Variables
Any environment variable that is not set will have the effect of its default value.

<table>
    <tr>
        <th style="width:25%">Variable</th>
        <th style="width:20%">Type</th>
        <th style="width:50%">Remark</th>
        <th style="width:5%">Default</th>
    </tr>
    <tr>
        <td>YAA_ALLOW_ROOT</td>
        <td>Boolean (<code>0</code>|<code>1</code>)</td>
        <td>Can be used to prevent the application from running as root on Linux-based systems. (UID==0)</td>
        <td><code>1</code></td>
    </tr>
    <!--<tr>
        <td>YAA_ALLOW_RAW_PARAMETERS</td>
        <td>Boolean (<code>0</code>|<code>1</code>)</td>
        <td>Can be used to prevent the command injection attacks.</td>
        <td><code>1</code></td>
    </tr>-->
    <tr>
        <td>YAA_CONFIG_PATH</td>
        <td>String</td>
        <td>
            Indicates where the config file can be found.<br>
            The path can be relative to app.py's location, or absolute.
        </td>
        <td><code>"./config.json"</code></td>
    </tr>
</table>

## Credits
● [Livestream achival guide](https://github.com/abayochocoball/hollow_memories/blob/master/archiving_livestreams.md)
by [abayochocoball](https://github.com/abayochocoball) <br>
&nbsp;&nbsp;&nbsp;&nbsp;Helped greatly with downloading the thumbnail and description of a stream.

● The [yt-dlp](https://github.com/yt-dlp/yt-dlp) contributors<br>
&nbsp;&nbsp;&nbsp;&nbsp;For actually giving a fuck about maintaining and improving *youtube-dl*.

## License
[Unlicense](LICENSE)

This license does not apply to the required Python modules or any other required piece of software.
