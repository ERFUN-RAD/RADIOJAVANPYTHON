![RADIO JAVAN LOGO](https://www.radiojavan.com/images/rj-touch-icon-144.png)

[![PYPI VERSION](https://badge.fury.io/py/radiojavanpython.svg)](https://badge.fury.io/py/radiojavanpython)
[![LICENSE: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://github.com/ERFUN-RAD/RADIOJAVANPYTHON/blob/master/LICENSE)
[![DOWNLOADS](https://pepy.tech/badge/radiojavanpython)](https://pepy.tech/project/radiojavanpython)

# RADIOJAVANPYTHON

THIS BUG-FREE VERSION OF THE RADIO JAVAN API WRAPPER IS FAST AND RELIABLE, OFFERING SEAMLESS ACCESS TO RADIO JAVAN FEATURES WITH PYTHON 3.7+ SUPPORT.

SUPPORT PYTHON >= 3.7

RADIO JAVAN API VALID FOR 19 MARCH 2023 (LAST REVERSE-ENGINEERING CHECK)

## FEATURES
* GET FULL INFO OF A SONG, VIDEO, PODCAST, STORY, PLAYLIST, ARTIST, ALBUM, USER, AND YOUR ACCOUNT
* LOGIN BY EMAIL AND PASSWORD
* SIGN UP TO RADIO JAVAN
* LIKE AND UNLIKE A SONG, VIDEO, PODCAST, AND STORY
* FOLLOW AND UNFOLLOW AN ARTIST, USER, OR MUSIC PLAYLIST
* GET FOLLOWERS AND FOLLOWING OF A USER
* CREATE, RENAME, AND DELETE A PLAYLIST
* ADD SONG OR VIDEO TO PLAYLIST OR REMOVE FROM IT
* EDIT AND DEACTIVATE ACCOUNT
* UPLOAD AND REMOVE PROFILE PHOTO
* SEARCH AND GET TRENDING, POPULAR, AND MORE MEDIAS
AND MUCH MORE ELSE

## INSTALLATION
**FROM GITHUB**  
```bash
pip install git+https://github.com/ERFUN-RAD/RADIOJAVANPYTHON
```

## BASIC USAGE

```python
from radiojavanapi import Client

# Create a Client instance and get a song info. 
client = Client()
song = client.get_song_by_url(
            'https://www.radiojavan.com/mp3s/mp3/Sijal-Baz-Mirim-Baham-(Ft-Sami-Low)')

print(f"""
        Name: {song.name}
        Artist: {song.artist}
        HQ-Link: {song.hq_link}
""")
```

<details>
    <summary>SHOW OUTPUT</summary>

```
Name: Baz Mirim Baham (Ft Sami Low)
Artist: Sijal
HQ-Link: https://host2.mediacon-rj.app/media/mp3/aac-256/99926-cf9dd3814907dbb.m4a
```
</details>

## SUPPORT
* CREATE A [GITHUB ISSUE](https://github.com/ERFUN-RAD/RADIOJAVANPYTHON/issues) FOR BUG REPORTS, FEATURE REQUESTS, OR QUESTIONS
* CONTACT US ON TELEGRAM AT [@ASYNCERFAN](https://t.me/asyncErfan)
* ADD A ⭐️ [STAR ON GITHUB](https://github.com/ERFUN-RAD/RADIOJAVANPYTHON) TO SUPPORT THE PROJECT!

## CONTRIBUTING
PULL REQUESTS ARE WELCOME. FOR MAJOR CHANGES, PLEASE OPEN AN ISSUE FIRST TO DISCUSS WHAT YOU WOULD LIKE TO CHANGE. CHECK OUR [CONTRIBUTING GUIDELINES](https://github.com/ERFUN-RAD/RADIOJAVANPYTHON/blob/master/CONTRIBUTING.md) FOR MORE DETAILS.

## LICENSE
THIS PROJECT IS LICENSED UNDER THE [MIT LICENSE](https://github.com/ERFUN-RAD/RADIOJAVANPYTHON/blob/master/LICENSE).
