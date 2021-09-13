# Youtube Auto Archiver <sub><sup>v0.5.0</sup></sub>
A simple and yet highly configurable Python application that automatically checks if a Youtuber is streaming,
and downloads said streams while also archiving its latest uploads.

The application will be improved as I have time to do so, or if you raise an issue when I have time to look into it.

A Dockerized version of the app is also available in my "<i>[Docker - Youtube Auto Archiver](https://github.com/aziascreations/Docker-Youtube-Auto-Archiver)</i>" repository.<br>
It is still missing a few features such as configurable UIG and GID however.

## Warning
Due to the way some commands are executed, it is possible to have a
[command injection](https://owasp.org/www-community/attacks/Command_Injection)
if you mess up or leave the config file editable by everyone.<br><!--This problem **can be mitigated** if you set up the appropriate [environment variables ](#environment-variables).-->
This might be fixed in the future, but don't count on it as this project is a personal project.

The code might also not be pretty and enjoyable to look at, but it works, is reliable and decently structured,
so I'm fine with it.

The application isn't designed to be used by another one as a module.

## Features
* General
  * Can run on Windows and Linux (*Tested on x64 and ARMv8*)
  * Relatively high level of configurability. (*More is incoming*)
* YouTube
  * Automatic livestream download through <code>https://youtube.com/c/.../live</code>
  * Automatic livestream thumbnail and description download.
  * Automatic download of uploads and their metadata.
  * Configurable delays, actions, locations per channel.
* Planned for v1.0.0
  * Native support for cookies for *yt-dlp* and maybe *streamlink*.
  * Propagated SIGINT and SIGTERM to child threads.
  * Complete command injection protection. (Unless explicitly disabled for some specific config fields)

## Requirements
* [Python](https://www.python.org/) v3.9 or newer
* [Streamlink](https://streamlink.github.io/) v2.3.0 or newer
* [yt-dlp](https://github.com/yt-dlp/yt-dlp) v2021.09.02 or newer

The application may work just fine with older versions of these pieces of software, but they will not be supported.<br>
All requirements, except for *Python*, can be installed via *pip* or manually.

## Installation

### Clone the repository and enter the directory
`git clone https://github.com/aziascreations/Youtube-Auto-Archiver.git`
<br>
`cd Youtube-Auto-Archiver`

### Install the required Python modules
Run one of the following commands:<br>
`pip install -r requirements.txt`<br>
`pip install --upgrade streamlink yt-dlp`<br>
`python -m pip install -r requirements.txt`<br>
`python -m pip install --upgrade streamlink yt-dlp`

Please note that *streamlink* may need to be compiled when installed via *pip*.<br>
You can ignore this step as long as the executable is accessible in the *PATH* environment variable.

### Configure the application
Check the [Config section](#config).

### Run the application
Simply run [app.py](app.py).

## Config
The config is stored in [config.json](config.json) and has to be in the same folder as [app.py](app.py), unless the
[environment variables](#environment-variables) tells the application to look elsewhere for it.

Any value that is set to `null` or is left `undefined` will be set to its default value.<br>
If said variable does not have a default value, the program will exit and print out the specific error in the logs.

<table style="width:100%;">
    <tr>
        <td colspan="4"><b><u>Root => {</u></b></td>
    </tr>
    <tr>
        <td><b>Field</b></td>
        <td><b>Type</b></td>
        <td><b>Remark</b></td>
        <td><b>Default</b></td>
    </tr>
    <tr>
        <td>application</td>
        <td>Application Object</td>
        <td>Contains the configs that are use globally by the application.</td>
        <td><code>None</code>/<code>null</code></td>
    </tr>
    <tr>
        <td>youtube</td>
        <td>Youtube Object</td>
        <td>Contains the configs for the YouTube related part of the application.</td>
        <td><code>None</code>/<code>null</code></td>
    </tr>
</table>

<table>
    <tr>
        <td colspan="4"><b><u>Application => { application {</u></b></td>
    </tr>
    <tr>
        <td><b>Field</b></td>
        <td><b>Type</b></td>
        <td><b>Remark</b></td>
        <td><b>Default</b></td>
    </tr>
    <tr>
        <td>root_output_dir</td>
        <td>String</td>
        <td>Root directory where the downloaded data should be stored in.</td>
        <td><code>./data</code></td>
    </tr>
    <tr>
        <td>logging_level_main</td>
        <td>Integer</td>
        <td>
            Logging level for the main app.<br>
            See <a href="https://docs.python.org/3/library/logging.html#logging-levels">Python's documentation</a>
            for more information
        </td>
        <td><code>10</code></td>
    </tr>
    <!-- max_working_worker_count -->
    <!-- auto_shutdown_after_ms -->
    <!-- auto_shutdown_do_wait_for_workers -->
    <!--<td><code></code></td>-->
</table>

<table>
    <tr>
        <td colspan="4"><b><u>Youtube => { youtube {</u></b></td>
    </tr>
    <tr>
        <td><b>Field</b></td>
        <td><b>Type</b></td>
        <td><b>Remark</b></td>
        <td><b>Default</b></td>
    </tr>
    <tr>
        <td>output_subdir</td>
        <td>String</td>
        <td>
            Directory in which all YouTube related downloads are stored.<br>
            Appended to <code>application.root_output_dir</code>.
        </td>
        <td><code>./youtube</code></td>
    </tr>
    <tr>
        <td>general_prefix</td>
        <td>String</td>
        <td>
            Prefix added to every downloaded file related to YouTube.<br>
            (WILL BE REMOVED IN THE NEXT VERSION)
        </td>
        <td><i>Required</i></td>
    </tr>
    <tr>
        <td>delay_ms_metadata_download</td>
        <td>Integer</td>
        <td>Delay in ms between the start of a live downloader thread and the moment it attempts to download its thumbnail
and description.<br>Can be disabled if set to <code>-1</code>.</td>
        <td><code>30000</code></td>
    </tr>
    <!-- allow_upload_while_live -->
    <!-- max_working_live_worker_count -->
    <!-- max_working_upload_worker_count -->
    <tr>
        <td>logging_level_worker</td>
        <td>Integer</td>
        <td>
            Logging level for all YouTube-related workers.<br>
            See <a href="https://docs.python.org/3/library/logging.html#logging-levels">Python's documentation</a>
            for more information
        </td>
        <td><code>10</code></td>
    </tr>
    <tr>
        <td>logging_level_thread</td>
        <td>Integer</td>
        <td>
            Logging level for all YouTube-related threads.<br>
            See <a href="https://docs.python.org/3/library/logging.html#logging-levels">Python's documentation</a>
            for more information
        </td>
        <td><code>10</code></td>
    </tr>
    <tr>
        <td>channels</td>
        <td>Array of Channel</td>
        <td>See below for more info on these objects.</td>
        <td><code>None</code>/<code>null</code></td>
    </tr>
</table>

<table>
    <tr>
        <td colspan="4"><b><u>Channel => { youtube { channels [ {</u></b></td>
    </tr>
    <tr>
        <td><b>Field</b></td>
        <td><b>Type</b></td>
        <td><b>Remark</b></td>
        <td><b>Default</b></td>
    </tr>
    <tr>
        <td>internal_id</td>
        <td>String</td>
        <td>Arbitrary string used in downloaded files and loggers' names.</td>
        <td><i>Required</i></td>
    </tr>
    <tr>
        <td>channel_id</td>
        <td>String</td>
        <td>Id of the relevant YouTube channel.</td>
        <td><i>Required</i></td>
    </tr>
    <tr>
        <td>name</td>
        <td>String</td>
        <td>Friendly name used in logging only.</td>
        <td><code>{internal_id}</code></td>
    </tr>
    <tr>
        <td>output_subdir</td>
        <td>String</td>
        <td>
            Directory in which all the files for this channel are downloaded into.<br>
            Appended to <code>application.root_output_dir</code> and <code>youtube.output_subdir</code>.
        </td>
        <td><code>./{internal_id}</code></td>
    </tr>
    <tr>
        <td>check_live</td>
        <td>Boolean</td>
        <td>Toggles the live downloading worker and threads.</td>
        <td><code>False</code></td>
    </tr>
    <tr>
        <td>check_upload</td>
        <td>Boolean</td>
        <td>Toggles the video downloading worker and threads.</td>
        <td><code>False</code></td>
    </tr>
    <tr>
        <td>interval_ms_live</td>
        <td>Integer</td>
        <td>
            Delay in ms between each verification of the channel to see if it is livestreaming.<br>
            Will disable the functionality if set to <code>-1</code>.
        </td>
        <td><code>-1</code></td>
    </tr>
    <tr>
        <td>interval_ms_upload</td>
        <td>Integer</td>
        <td>
            Delay in ms between each verification of the channel to see if it is livestreaming.<br>
            Will disable the functionality if set to <code>-1</code>.
        </td>
        <td><code>-1</code></td>
    </tr>
    <tr>
        <td>quality_live</td>
        <td>String</td>
        <td>Quality setting used in streamlink when downloading a live.</td>
        <td><code>"best"</code></td>
    </tr>
    <tr>
        <td>quality_upload</td>
        <td>String</td>
        <td>Quality setting used in yt-dlp with the <code>-f</code> option.</td>
        <td><code>"best"</code></td>
    </tr>
    <tr>
        <td>backlog_days_upload</td>
        <td>Integer</td>
        <td>
            Number of days to look back to for uploads<br>
            Added as-is in the <code>--dateafter now-Xdays</code> option where <code>X</code> is the number of days given here.
        </td>
        <td><code>7</code></td>
    </tr>
    <tr>
        <td>break_on_existing</td>
        <td>Boolean</td>
        <td>Indicates if yt-dlp should stop downloading uploads when encountering an existing completed download.</td>
        <td><code>True</code></td>
    </tr>
    <tr>
        <td>break_on_reject</td>
        <td>Boolean</td>
        <td>Indicates if yt-dlp should stop downloading uploads when encountering a filtered video.</td>
        <td><code>True</code></td>
    </tr>
    <!--<tr>
        <td>write_upload_thumbnail</td>
        <td>Boolean</td>
        <td>Indicates if yt-dlp should use the <code>--write-thumbnail</code> flag.</td>
        <td><code></code></td>
    </tr>-->
    <tr>
        <td>yt_dlp_extra_args</td>
        <td>String</td>
        <td>Extra args added as-is to the yt-dlp command right before the channel URL.</td>
        <td><code>""</code></td>
    </tr>
    <tr>
        <td>allow_upload_while_live</td>
        <td>Boolean</td>
        <td>Indicates whether yt-dlp can download videos while a <i>live worker</i> is running for the given channel.</td>
        <td><code>True</code></td>
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
