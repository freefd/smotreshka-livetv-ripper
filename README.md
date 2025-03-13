# Smotreshka Live TV Ripper

A tool to build the top-level M3U playlist and EPG XMLTV listing file using the [Smotreshka](https://smotreshka.tv/) as a source.

## Functionality
* Generate M3U playlist for Live TV streams
* Generate EPG listing in XMLTV format

## Requirements:
* Python 3.10+
* Smotreshka account with purchased channels bundle

## How to run
1. Clone the Git repository:
```shell
~> git clone https://github.com/freefd/smotreshka-livetv-ripper
```

2. Navigate to the cloned repo directory:

```shell
~> cd smotreshka-livetv-ripper
```

3. Run `main.py` with `--help` as argument:

```shell
~> python3 main.py --help
usage: main.py [-h] -u USERNAME -p PASSWORD [-m3u M3U_OUTPUT] [-xmltv XMLTV_OUTPUT] [-l LIMIT] [-m {all,epg,m3u}] [-o] [--verbose]
Smotreshka Live TV Ripper
options:
  -h, --help            show this help message and exit
  -u, --username USERNAME
                        User name to login. Default: not set
  -p, --password PASSWORD
                        Password to login. Default: not set
  -m3u, --m3u-output M3U_OUTPUT
                        Generated M3U file path. Default: smotreshka.m3u
  -xmltv, --xmltv-output XMLTV_OUTPUT
                        Generated XMLTV file path. Default: smotreshka.xmltv.xml
  -l, --limit LIMIT     Limit the number of channels for processing. Default: 0
  -m, --mode {all,epg,m3u}
                        Generator mode. Default: all
  -o, --overwrite       Allow to overwrite existing output files. Default: false
  --verbose, -v         Enable verbose output. Default: 0
```

### Examples

Generate only the EPG XMLTV listing to the current directory

```shell
~> python3 main.py -u 'user@name' -p 'P4$$w0r6' -m epg
[2025-03-13 00:13:31,676] INFO smotreshka_module.py::Smotreshka::_login(): Login as user user@name
[2025-03-13 00:13:31,717] INFO smotreshka_module.py::Smotreshka::_login(): Authenticated as user user@name
[2025-03-13 00:13:31,717] INFO smotreshka_module.py::Smotreshka::_collect_channels(): Collect purchased LiveTV channels
[2025-03-13 00:13:31,814] INFO smotreshka_module.py::Smotreshka::_collect_channels(): Add channel `Первый канал`
[2025-03-13 00:13:31,814] INFO smotreshka_module.py::Smotreshka::_collect_channels(): Add channel `Россия 1`
[2025-03-13 00:13:31,814] INFO smotreshka_module.py::Smotreshka::_collect_channels(): Add channel `Матч ТВ`
... omitted for brevity ...
[2025-03-13 00:13:31,815] INFO smotreshka_module.py::Smotreshka::_collect_channels(): Add channel `ТНТ4`
[2025-03-13 00:13:31,815] INFO smotreshka_module.py::Smotreshka::_collect_channels(): Add channel `Ювелирочка`
[2025-03-13 00:13:31,815] INFO smotreshka_module.py::Smotreshka::_collect_channels(): Add channel `Leomax 24`
[2025-03-13 00:13:31,815] INFO smotreshka_module.py::Smotreshka::_collect_epg(): Collect EPG for channel `52d555c99109550984000004` (Первый канал)
[2025-03-13 00:13:31,850] INFO smotreshka_module.py::Smotreshka::_collect_epg(): Add EPG programs to channel 52d555c99109550984000004 (Первый канал)
[2025-03-13 00:13:31,854] INFO smotreshka_module.py::Smotreshka::_collect_epg(): Collect EPG for channel `52d555c9910955098400000d` (Россия 1)
[2025-03-13 00:13:31,902] INFO smotreshka_module.py::Smotreshka::_collect_epg(): Add EPG programs to channel 52d555c9910955098400000d (Россия 1)
[2025-03-13 00:13:31,905] INFO smotreshka_module.py::Smotreshka::_collect_epg(): Collect EPG for channel `535f5da5ebf8c403a1001bd9` (Матч ТВ)
[2025-03-13 00:13:31,953] INFO smotreshka_module.py::Smotreshka::_collect_epg(): Add EPG programs to channel 535f5da5ebf8c403a1001bd9 (Матч ТВ)
... omitted for brevity ...
[2025-03-13 00:13:33,592] INFO smotreshka_module.py::Smotreshka::_collect_epg(): Collect EPG for channel `535f5d7febf8c403a1001bd8` (ТНТ4)
[2025-03-13 00:13:33,638] INFO smotreshka_module.py::Smotreshka::_collect_epg(): Add EPG programs to channel 535f5d7febf8c403a1001bd8 (ТНТ4)
[2025-03-13 00:13:33,650] INFO smotreshka_module.py::Smotreshka::_collect_epg(): Collect EPG for channel `679ca5495786b391d3537fdd` (Ювелирочка)
[2025-03-13 00:13:33,663] WARNING smotreshka_module.py::Smotreshka::_collect_epg(): List of EPG programs is empty for channel `679ca5495786b391d3537fdd` (Ювелирочка)
[2025-03-13 00:13:33,679] INFO smotreshka_module.py::Smotreshka::_collect_epg(): Collect EPG for channel `67a5bb155c85486a7c40ecec` (Leomax 24)
[2025-03-13 00:13:33,706] INFO smotreshka_module.py::Smotreshka::_collect_epg(): Add EPG programs to channel 67a5bb155c85486a7c40ecec (Leomax 24)
[2025-03-13 00:13:33,711] INFO epg_module.py::EPGListing::append_epg_channel(): Add EPG channel `Первый канал`
[2025-03-13 00:13:33,716] INFO epg_module.py::EPGListing::append_epg_channel(): Add EPG channel `Россия 1`
[2025-03-13 00:13:33,721] INFO epg_module.py::EPGListing::append_epg_channel(): Add EPG channel `Матч ТВ`
... omitted for brevity ...
[2025-03-13 00:13:34,258] INFO epg_module.py::EPGListing::append_epg_channel(): Add EPG channel `ТНТ4`
[2025-03-13 00:13:34,293] INFO epg_module.py::EPGListing::append_epg_channel(): Add EPG channel `Ювелирочка`
[2025-03-13 00:13:34,293] INFO epg_module.py::EPGListing::append_epg_channel(): Add EPG channel `Leomax 24`
[2025-03-13 00:13:34,541] INFO main.py::__main__::<module>(): Please find generated EPG XMLTV listing
	- /home/username/path/to/smotreshka-livetv-ripper/smotreshka.xmltv.xml
```

Generate only the M3U playlist to file /tmp/m3ufilename.m3u, with debug enabled and overwriting the existing file

```shell
~> ./main.py -u 'user@name' -p 'P4$$w0r6' -vv -m m3u -o -m3u /tmp/m3ufilename.m3u
[2025-03-13 13:21:53,044] INFO smotreshka_module.py::Smotreshka::_login(): Login as user user@name
[2025-03-13 13:21:53,044] DEBUG smotreshka_module.py::Smotreshka::_http_request(): Request POST https://fe.smotreshka.tv/login Params={'email': 'user@name', 'password': '*****'}
[2025-03-13 13:21:53,078] INFO smotreshka_module.py::Smotreshka::_login(): Authenticated as user user@name
[2025-03-13 13:21:53,078] DEBUG smotreshka_module.py::Smotreshka::_login(): Collected cookies {'userId': '97f6f45481094209a80d1273', 'session': 'IMt1pFPg1crTNaL9eon3jQOoOqADpaARpNt48YzzzlKV420DYwHPm8hevSSY5jHwtIlYrOjqaTD034U4aoAZO88VI3gProb86d5gwslOBmajOuFv'}
[2025-03-13 13:21:53,078] INFO smotreshka_module.py::Smotreshka::_collect_channels(): Collect purchased LiveTV channels
[2025-03-13 13:21:53,078] DEBUG smotreshka_module.py::Smotreshka::_http_request(): Request GET https://fe.smotreshka.tv/channels Params=None
[2025-03-13 13:21:53,162] INFO smotreshka_module.py::Smotreshka::_collect_channels(): Add channel `Первый канал`
[2025-03-13 13:21:53,162] INFO smotreshka_module.py::Smotreshka::_collect_channels(): Add channel `Россия 1`
[2025-03-13 13:21:53,162] INFO smotreshka_module.py::Smotreshka::_collect_channels(): Add channel `Матч ТВ`
... omitted for brevity ...
[2025-03-13 13:21:53,170] INFO smotreshka_module.py::Smotreshka::_collect_channels(): Add channel `Самарское губернское телевидение (ГУБЕРНИЯ)`
[2025-03-13 13:21:53,170] INFO smotreshka_module.py::Smotreshka::_collect_channels(): Add channel `Башкортостан 24`
[2025-03-13 13:21:53,170] INFO smotreshka_module.py::Smotreshka::_collect_channels(): Add channel `Осетия Ирыстон`
[2025-03-13 13:21:53,170] INFO smotreshka_module.py::Smotreshka::_collect_streams(): Collect LiveTV stream `52d555c99109550984000004` (Первый канал)
[2025-03-13 13:21:53,170] DEBUG smotreshka_module.py::Smotreshka::_http_request(): Request GET https://fe.smotreshka.tv/playback-info/52d555c99109550984000004 Params=None
[2025-03-13 13:21:53,197] INFO smotreshka_module.py::Smotreshka::_collect_streams(): Add language ru_RU to channel `52d555c99109550984000004` (Первый канал)
[2025-03-13 13:21:53,198] INFO smotreshka_module.py::Smotreshka::_collect_streams(): Add LiveTV stream URL to channel `52d555c99109550984000004` (Первый канал)
[2025-03-13 13:21:53,198] INFO smotreshka_module.py::Smotreshka::_collect_streams(): Collect LiveTV stream `52d555c9910955098400000d` (Россия 1)
[2025-03-13 13:21:53,198] DEBUG smotreshka_module.py::Smotreshka::_http_request(): Request GET https://fe.smotreshka.tv/playback-info/52d555c9910955098400000d Params=None
[2025-03-13 13:21:53,685] INFO smotreshka_module.py::Smotreshka::_collect_streams(): Add language ru_RU to channel `52d555c9910955098400000d` (Россия 1)
[2025-03-13 13:21:53,685] INFO smotreshka_module.py::Smotreshka::_collect_streams(): Add LiveTV stream URL to channel `52d555c9910955098400000d` (Россия 1)
[2025-03-13 13:21:53,685] INFO smotreshka_module.py::Smotreshka::_collect_streams(): Collect LiveTV stream `535f5da5ebf8c403a1001bd9` (Матч ТВ)
[2025-03-13 13:21:53,686] DEBUG smotreshka_module.py::Smotreshka::_http_request(): Request GET https://fe.smotreshka.tv/playback-info/535f5da5ebf8c403a1001bd9 Params=None
[2025-03-13 13:21:54,249] INFO smotreshka_module.py::Smotreshka::_collect_streams(): Add language ru_RU to channel `535f5da5ebf8c403a1001bd9` (Матч ТВ)
[2025-03-13 13:21:54,249] INFO smotreshka_module.py::Smotreshka::_collect_streams(): Add LiveTV stream URL to channel `535f5da5ebf8c403a1001bd9` (Матч ТВ)
... omitted for brevity ...
[2025-03-13 13:22:23,785] INFO smotreshka_module.py::Smotreshka::_collect_streams(): Collect LiveTV stream `6336fcfc944a76551004809b` (CINEMA UHD)
[2025-03-13 13:22:23,785] DEBUG smotreshka_module.py::Smotreshka::_http_request(): Request GET https://fe.smotreshka.tv/playback-info/6336fcfc944a76551004809b Params=None
[2025-03-13 13:22:24,284] INFO smotreshka_module.py::Smotreshka::_collect_streams(): Add language ru_RU to channel `6336fcfc944a76551004809b` (CINEMA UHD)
[2025-03-13 13:22:24,284] WARNING smotreshka_module.py::Smotreshka::_collect_streams(): Cannot collect default LiveTV rendition for channel `6336fcfc944a76551004809b` (CINEMA UHD)
[2025-03-13 13:22:24,284] INFO smotreshka_module.py::Smotreshka::_collect_streams(): Add first found LiveTV stream URL to channel `6336fcfc944a76551004809b` (CINEMA UHD)
... omitted for brevity ...
[2025-03-13 13:23:20,984] INFO smotreshka_module.py::Smotreshka::_collect_streams(): Collect LiveTV stream `5e79c2b3cf1d9d5a91882efd` (Самарское губернское телевидение (ГУБЕРНИЯ))
[2025-03-13 13:23:20,984] DEBUG smotreshka_module.py::Smotreshka::_http_request(): Request GET https://fe.smotreshka.tv/playback-info/5e79c2b3cf1d9d5a91882efd Params=None
[2025-03-13 13:23:21,393] INFO smotreshka_module.py::Smotreshka::_collect_streams(): Add language ru_RU to channel `5e79c2b3cf1d9d5a91882efd` (Самарское губернское телевидение (ГУБЕРНИЯ))
[2025-03-13 13:23:21,393] INFO smotreshka_module.py::Smotreshka::_collect_streams(): Add LiveTV stream URL to channel `5e79c2b3cf1d9d5a91882efd` (Самарское губернское телевидение (ГУБЕРНИЯ))
[2025-03-13 13:23:21,393] INFO smotreshka_module.py::Smotreshka::_collect_streams(): Collect LiveTV stream `63777ebceefd6484267418b0` (Башкортостан 24)
[2025-03-13 13:23:21,393] DEBUG smotreshka_module.py::Smotreshka::_http_request(): Request GET https://fe.smotreshka.tv/playback-info/63777ebceefd6484267418b0 Params=None
[2025-03-13 13:23:22,008] INFO smotreshka_module.py::Smotreshka::_collect_streams(): Add language ru_RU to channel `63777ebceefd6484267418b0` (Башкортостан 24)
[2025-03-13 13:23:22,008] INFO smotreshka_module.py::Smotreshka::_collect_streams(): Add LiveTV stream URL to channel `63777ebceefd6484267418b0` (Башкортостан 24)
[2025-03-13 13:23:22,008] INFO smotreshka_module.py::Smotreshka::_collect_streams(): Collect LiveTV stream `63c6b1ce0e8f8ac35d437c4e` (Осетия Ирыстон)
[2025-03-13 13:23:22,008] DEBUG smotreshka_module.py::Smotreshka::_http_request(): Request GET https://fe.smotreshka.tv/playback-info/63c6b1ce0e8f8ac35d437c4e Params=None
[2025-03-13 13:23:22,417] INFO smotreshka_module.py::Smotreshka::_collect_streams(): Add language en_EN to channel `63c6b1ce0e8f8ac35d437c4e` (Осетия Ирыстон)
[2025-03-13 13:23:22,417] INFO smotreshka_module.py::Smotreshka::_collect_streams(): Add LiveTV stream URL to channel `63c6b1ce0e8f8ac35d437c4e` (Осетия Ирыстон)
[2025-03-13 13:23:22,417] INFO m3u_module.py::M3UPlaylist::append_m3u_channel(): Add M3U channel `Первый канал`
[2025-03-13 13:23:22,418] INFO m3u_module.py::M3UPlaylist::append_m3u_channel(): Add M3U channel `Россия 1`
[2025-03-13 13:23:22,418] INFO m3u_module.py::M3UPlaylist::append_m3u_channel(): Add M3U channel `Матч ТВ`
... omitted for brevity ...
[2025-03-13 13:23:22,430] INFO m3u_module.py::M3UPlaylist::append_m3u_channel(): Add M3U channel `Самарское губернское телевидение (ГУБЕРНИЯ)`
[2025-03-13 13:23:22,430] INFO m3u_module.py::M3UPlaylist::append_m3u_channel(): Add M3U channel `Башкортостан 24`
[2025-03-13 13:23:22,430] INFO m3u_module.py::M3UPlaylist::append_m3u_channel(): Add M3U channel `Осетия Ирыстон`
[2025-03-13 13:23:22,432] INFO main.py::__main__::<module>(): Please find generated M3U playlist
	- /tmp/m3ufilename.m3u
```
