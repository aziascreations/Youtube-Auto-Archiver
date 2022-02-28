# Youtube Auto Archiver - Config


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
    <tr>
        <td>auto_shutdown_after_ms</td>
        <td>Integer</td>
        <td>
            Delay in milliseconds after which the application should automatically exit with a return code of <code>0</code>.<br>
            This can be used to restart containers and clean potential memory leaks.<br>
            Will disable the functionality if set to <code>-1</code>.
        </td>
        <td><code>-1</code></td>
    </tr>
    <tr>
        <td>auto_shutdown_do_wait_for_workers</td>
        <td>Boolean</td>
        <td>
            Indicates whether or not the application should wait for all worker's thread to finish without sending
            a <i>SIGINT</i> or <i>SIGTERM</i> signal back to them after the countdown was reached.<br>
            If set to <code>False</code>, the application will forcefully kill these threads which could lead to a loss
            or corruption of data.<br>
            No new threads will be launched while the main loop waits for all threads to be finished with there work.
        </td>
        <td><code>True</code></td>
    </tr>
    <tr>
        <td>auto_shutdown_number_to_send</td>
        <td>Integer</td>
        <td>
            Indicates which signal should be send to threads if <code>auto_shutdown_do_wait_for_workers</code> is set to
            <code>False</code>.<br>
            Allowed values are <code>-1</code>, <code>SIGINT (2)</code> and <code>SIGTERM (15)</code>.<br>
            If it is set to an incorrect value, or to <code>-1</code>, it will automatically be set to
            <code>SIGTERM (15)</code> and will be said in the debug-level logs.
        </td>
        <td><code>-1</code></td>
    </tr>
    <tr>
        <td>signal_shutdown_do_wait_for_workers</td>
        <td>Boolean</td>
        <td>
            Indicates whether or not the application should wait for all worker's thread to finish without sending
            a <i>SIGINT</i> or <i>SIGTERM</i> signal back to them after receiving a shutdown signal.<br>
            If set to <code>False</code>, the application will forcefully kill these threads which could lead to a loss
            or corruption of data.<br>
            No new threads will be launched while the main loop waits for all threads to be finished with there work.
        </td>
        <td><code>False</code></td>
    </tr>
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
        <td><code>{internal_id}</code><br><b>Broken in 0.7.0, now required</b></td>
    </tr>
    <tr>
        <td>output_subdir</td>
        <td>String</td>
        <td>
            Directory in which all the files for this channel are downloaded into.<br>
            Appended to <code>application.root_output_dir</code> and <code>youtube.output_subdir</code>.
        </td>
        <td><code>./{internal_id}</code><br><b>Broken in 0.7.0, now required</b></td>
    </tr>
    <tr>
        <td>live_subdir</td>
        <td>String</td>
        <td>
            Directory in which all the livestream files for this channel are downloaded into.
            <code>Appended to application.root_output_dir</code>, <code>youtube.output_subdir</code> and <code>youtube.{channel}.output_subdir</code>.
        </td>
        <td><code>./livestreams</code></b></td>
    </tr>
    <tr>
        <td>upload_subdir</td>
        <td>String</td>
        <td>
            Directory in which all the upload files for this channel are downloaded into.
            <code>Appended to application.root_output_dir</code>, <code>youtube.output_subdir</code> and <code>youtube.{channel}.output_subdir</code>.
        </td>
        <td><code>./uploads</code></b></td>
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
