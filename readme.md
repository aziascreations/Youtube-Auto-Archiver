# Youtube Auto Archiver

A simple python application that automatically checks if a Youtuber is streaming, and downloads said streams.

Is it still under development, and a Dockerfile will be made public soon.

## Warning

Due to the way some commands are executed, it is possible to have a
[command injection](https://owasp.org/www-community/attacks/Command_Injection)
if you mess up or leave the config file editable by everyone.<br>
This might be fixed in the future, but don't count on it as this project is a personal project.

The code might not be pretty and enjoyable to look at, but it works, is reliable and decently structured,
so I'm fine with it.

## Features

* General
  * Can run on Windows and Linux (*x64 or armv8*)
* YouTube
  * Automatic livestream download through "*youtube.com/c/.../live*"
  * Automatic livestream thumbnail and description download
  * Configurable delays per channel
  * Toggleable actions
* Planned
  * Logging levels in the config file
  * Cookies support for *yt-dlp* and maybe *streamlink*

## Installation

**▸ Clone the repository and enter the directory:**<br>
`git clone https://github.com/aziascreations/Youtube-Auto-Archiver.git`
<br>
`cd Youtube-Auto-Archiver`

**▸ Install the required Python modules:**<br>
Run one of the following commands:<br>
`pip install -r requirements.txt`<br>
`pip install --upgrade streamlink yt-dlp`<br>
`python -m pip install -r requirements.txt`<br>
`python -m pip install --upgrade streamlink yt-dlp`

Please note that *streamlink* may need to be compiled when installed via *pip*.<br>
You can ignore it as long as the executable is accessible in the *PATH* environment variable.

**▸ Configure the application**<br>
Check the [Config section](#config).


**▸ Run the application**<br>
Simply run [app.py](app.py).

## Config
The config is stored in [config.json](config.json) and has to be in the same folder as [app.py](app.py).

<table>
    <tr>
        <td colspan="3"><b><u>{ application {</u></b></td>
    </tr>
    <tr>
        <td><b>Field</b></td>
        <td><b>Type</b></td>
        <td><b>Remark</b></td>
    </tr>
    <tr>
        <td>base_output_dir</td>
        <td>String</td>
        <td>Root directory where the downloaded data should be stored in.</td>
    </tr>
</table>

<table>
    <tr>
        <td colspan="3"><b><u>{ youtube {</u></b></td>
    </tr>
    <tr>
        <td><b>Field</b></td>
        <td><b>Type</b></td>
        <td><b>Remark</b></td>
    </tr>
    <tr>
        <td>output_subdir</td>
        <td>String</td>
        <td>
            Directory in which all YouTube related downloads are stored.<br>
            Appended to "<i>application.base_output_dir</i>".
        </td>
    </tr>
    <tr>
        <td>general_prefix</td>
        <td>String</td>
        <td>Prefix added to every downloaded file related to YouTube.</td>
    </tr>
    <tr>
        <td>delay_ms_before_metadata_download</td>
        <td>Integer</td>
        <td>Delay in ms between the start of a live downloader thread and the moment it attempts to download its thumbnail
and description.<br>Can be disabled if set to "-1".</td>
    </tr>
    <tr>
        <td>channels</td>
        <td>Array of Channel</td>
        <td>See below for more info on these objects.</td>
    </tr>
</table>

<table>
    <tr>
        <td colspan="3"><b><u>Channel => { youtube { channels [ {</u></b></td>
    </tr>
    <tr>
        <td><b>Field</b></td>
        <td><b>Type</b></td>
        <td><b>Remark</b></td>
    </tr>
    <tr>
        <td>internal_id</td>
        <td>String</td>
        <td>Arbitrary string used in downloaded files and loggers' names.</td>
    </tr>
    <tr>
        <td>channel_id</td>
        <td>String</td>
        <td>Id of the relevant YouTube channel.</td>
    </tr>
    <tr>
        <td>name</td>
        <td>String</td>
        <td>Friendly name used in logging only.</td>
    </tr>
    <tr>
        <td>output_subdir</td>
        <td>String</td>
        <td>
            Directory in which all the files for this channel are downloaded into.<br>
            Appended to "<i>application.base_output_dir</i>" and "<i>youtube.output_subdir</i>".
        </td>
    </tr>
    <tr>
        <td>check_live</td>
        <td>Boolean</td>
        <td>Toggles the live downloading worker and threads.</td>
    </tr>
    <tr>
        <td>check_upload</td>
        <td>Boolean</td>
        <td>Toggles the video downloading worker and threads. (NOT IMPLEMENTED)</td>
    </tr>
    <tr>
        <td>interval_ms_live</td>
        <td>Integer</td>
        <td>
            Delay in ms between each verification of the channel to see if it is livestreaming.<br>
            Will disable the functionality if set to "<i>-1</i>".<br>
            (NOT IMPLEMENTED)
        </td>
    </tr>
    <tr>
        <td>interval_ms_upload</td>
        <td>Integer</td>
        <td>
            Delay in ms between each verification of the channel to see if it is livestreaming.<br>
            Will disable the functionality if set to "<i>-1</i>".
        </td>
    </tr>
    <tr>
        <td>quality_live</td>
        <td>String</td>
        <td>Quality setting used in streamlink when downloading a live.</td>
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

This license does not apply to the required Python modules.
