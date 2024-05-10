# QUARTER: QQ Music Playlist Report Generator

## 简介

QUARTER是一个QQ音乐歌单报告生成器，可以根据QQ音乐歌单生成歌单报告。

目前支持的功能有：

- 统计歌单中歌曲的歌手分布情况
- 统计歌单中歌曲的专辑分布情况
- （受API限制，web端仅能获取这些信息TAT）

考虑未来可能会增加的功能：

- 统计语种、流派等信息（似乎需要安卓客户端）
- 统计歌单中歌曲的播放次数排行（似乎需要安卓客户端）

## 依赖

- Python 3
- requests
- pyecharts
- bs4

## 使用方法

将希望分析的歌单通过客户端生成分享链接，其格式形如：

```url
https://c6.y.qq.com/base/fcgi-bin/u?__=xxxxxx
```

将链接中的`u?__=`后的部分复制到`config.py`中的`PLAYLIST_TOKEN`变量，然后运行`main.py`即可。

```shell
python3 main.py
```
