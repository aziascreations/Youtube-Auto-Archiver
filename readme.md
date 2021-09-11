# Youtube Auto Archiver

A simple python application that automatically checks if a Youtuber is streaming, and downloads said streams.

The application will be improved as I have time to do so, or if you raise an issue an I have time to look into it.

A Dockerized version of the app is also available in my "<i>[Docker - Youtube Auto Archiver](https://github.com/aziascreations/Docker-Youtube-Auto-Archiver)</i>" repository.<br>
It is still missing a few features such as configurable UIG and GID however.

## Warning

Due to the way some commands are executed, it is possible to have a
[command injection](https://owasp.org/www-community/attacks/Command_Injection)
if you mess up or leave the config file editable by everyone.<br>
This might be fixed in the future, but don't count on it as this project is a personal project.

The code might also not be pretty and enjoyable to look at, but it works, is reliable and decently structured,
so I'm fine with it.

## Features

* General
  * Can run on Windows and Linux (*x64 or armv8*)
* YouTube
  * Automatic livestream download through <code>https://youtube.com/c/.../live</code>
  * Automatic livestream thumbnail and description download
  * Configurable delays per channel
  * Toggleable actions
* Planned
  * Logging levels in the config file
  * Cookies support for *yt-dlp* and maybe *streamlink*
  * Support for incomplete config files with default values.

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
        <td colspan="3"><b><u>Root => {</u></b></td>
    </tr>
    <tr>
        <td><b>Field</b></td>
        <td><b>Type</b></td>
        <td><b>Remark</b></td>
    </tr>
    <tr>
        <td>application</td>
        <td>Application Object</td>
        <td>Contains the configs that are use globally by the application.</td>
    </tr>
    <tr>
        <td>youtube</td>
        <td>Youtube Object</td>
        <td>Contains the configs for the YouTube related part of the application.</td>
    </tr>
</table>

<table>
    <tr>
        <td colspan="3"><b><u>Application => { application {</u></b></td>
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
        <td colspan="3"><b><u>Youtube => { youtube {</u></b></td>
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
            Appended to <code>application.base_output_dir</code>.
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
and description.<br>Can be disabled if set to <code>-1</code>.</td>
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
            Appended to <code>application.base_output_dir</code> and <code>youtube.output_subdir</code>.
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
        <td>Toggles the video downloading worker and threads.</td>
    </tr>
    <tr>
        <td>interval_ms_live</td>
        <td>Integer</td>
        <td>
            Delay in ms between each verification of the channel to see if it is livestreaming.<br>
            Will disable the functionality if set to <code>-1</code>.
        </td>
    </tr>
    <tr>
        <td>interval_ms_upload</td>
        <td>Integer</td>
        <td>
            Delay in ms between each verification of the channel to see if it is livestreaming.<br>
            Will disable the functionality if set to <code>-1</code>.
        </td>
    </tr>
    <tr>
        <td>quality_live</td>
        <td>String</td>
        <td>Quality setting used in streamlink when downloading a live.</td>
    </tr>
    <tr>
        <td>quality_upload</td>
        <td>String</td>
        <td>Quality setting used in yt-dlp with the <code>-f</code> option.</td>
    </tr>
    <tr>
        <td>backlog_days_upload</td>
        <td>Integer</td>
        <td>
            Number of days to look back to for uploads<br>
            Added as-is in the <code>--dateafter now-Xdays</code> option where <code>X</code> is the number of days given here.
        </td>
    </tr>
    <tr>
        <td>break_on_existing</td>
        <td>Boolean</td>
        <td>Indicates if yt-dlp should stop downloading uploads when encountering an existing completed download.</td>
    </tr>
    <tr>
        <td>break_on_reject</td>
        <td>Boolean</td>
        <td>Indicates if yt-dlp should stop downloading uploads when encountering a filtered video.</td>
    </tr>
    <tr>
        <td>write_upload_thumbnail</td>
        <td>Boolean</td>
        <td>Indicates if yt-dlp should use the <code>--write-thumbnail</code> flag.</td>
    </tr>
    <tr>
        <td>yt_dlp_extra_args</td>
        <td>String</td>
        <td>Extra args added as-is to the yt-dlp command right before the channel URL.</td>
    </tr>
    <tr>
        <td>allow_upload_while_live</td>
        <td>Boolean</td>
        <td>Indicates whether yt-dlp can download videos while a <i>live worker</i> is running for the given channel.</td>
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
