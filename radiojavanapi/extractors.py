from radiojavanapi.helper import to_int
from radiojavanapi.models import (
    Account, Album, Artist, MyPlaylists, NotificationsStatus,
    ShortUser, Song, MusicPlaylist, Story, User, Video,
    ShortData, Podcast, SearchResults, VideoPlaylist
)
import re
from urllib.parse import urlparse, urlunparse
from typing import Optional, Dict, Any

def clean_url(url):
    if not url:
        return url
    
    url = url.replace('\xa0', '').strip()
    
    parsed_url = urlparse(url)
    clean_path = re.sub(r'\s*\(.*?\)/.*$', '', parsed_url.path)
    return urlunparse(parsed_url._replace(path=clean_path))

def ensure_required_fields(data: Dict[str, Any], model_class, context: str = "") -> Dict[str, Any]:
    """Ensure all required fields for a model are present with default values"""
    
    required_fields_map = {
        'Song': ['id', 'name', 'artist', 'plays', 'likes', 'dislikes', 'downloads', 'item'],
        'MusicPlaylist': ['id', 'title', 'count', 'created_at', 'created_by', 'last_updated_at', 
                         'share_link', 'followers', 'is_public', 'is_my_playlist', 'photo', 
                         'has_custom_photo', 'thumbnail'],
        'Album': ['id', 'name', 'artist', 'share_link'],
        'Video': ['id', 'name', 'artist', 'views', 'likes', 'dislikes'],
        'Podcast': ['id', 'title', 'artist', 'plays', 'likes', 'dislikes'],
        'Artist': ['id', 'name', 'followers_count', 'following', 'plays'],
        'User': ['id', 'username', 'default_thumbnail', 'has_custom_photo', 
                'has_subscription', 'is_verified'],
        'Account': ['id', 'username', 'default_thumbnail', 'has_subscription', 
                   'has_custom_photo', 'is_verified'],
        'Story': ['id', 'is_verified', 'lq_link', 'song_id', 'user'],
        'ShortData': ['id', 'title', 'permlink', 'photo'],
        'ShortUser': ['id', 'username', 'thumbnail', 'share_link']  
    }
    
    model_name = model_class.__name__
    
    
    if 'id' in data and isinstance(data['id'], int):
        data['id'] = str(data['id'])
    
    if model_name in required_fields_map:
        for field in required_fields_map[model_name]:
            if field not in data:
                
                if field in ['plays', 'likes', 'dislikes', 'downloads', 'views', 'count', 'followers_count']:
                    data[field] = 0
                elif field in ['is_public', 'is_my_playlist', 'has_custom_photo', 'is_verified', 'following']:
                    data[field] = False
                elif field in ['item', 'lyric', 'credits', 'date', 'created_at', 'last_updated_at']:
                    data[field] = ''
                elif field == 'share_link':
                    username = data.get('username', 'unknown')
                    data[field] = f"https://www.radiojavan.com/profile/{username}"
                elif field == 'photo':
                    data[field] = 'https://www.radiojavan.com/default_photo.jpg'
                elif field == 'thumbnail':
                    data[field] = data.get('photo', 'https://www.radiojavan.com/default_thumb.jpg')
                elif field == 'id':
                    data[field] = 'unknown_id'
                elif field == 'username':
                    data[field] = 'unknown_user'
                else:
                    data[field] = f"unknown_{field}"
    
    return data

def extract_account(data) -> Account:
    data["default_thumbnail"] = data.pop('default_thumb', '')
    data["has_subscription"] = data.pop('subscription', False)
    data["has_custom_photo"] = data.pop('custom_photo', False)
    data["is_verified"] = data.pop('verify', False)
    data["artists_name"] = [artist["name"] for artist in data.pop('artists', [])]
    data["stories"] = [extract_story(story) for story in data.pop('selfies', [])]
    data = ensure_required_fields(data, Account)
    return Account(**data)

def extract_user(data) -> User:
    data["default_thumbnail"] = data.pop('default_thumb', '')
    data["has_custom_photo"] = data.pop('custom_photo', False)
    data["has_subscription"] = data.pop('subscription', False)
    data["is_verified"] = data.pop('verify', False)
    data["artists_name"] = [artist["name"] for artist in data.pop('artists', [])]
    data["stories"] = [extract_story(story) for story in data.pop('selfies', [])]
    data["music_playlists"] = [extract_short_data(playlist['playlist'], MusicPlaylist) 
                              for playlist in data.pop('playlists', []) if 'playlist' in playlist]
    data = ensure_required_fields(data, User)
    return User(**data)

def extract_song(data) -> Song:
    album = data.pop('album', None)
    if type(album) == dict:
        album = album.pop('album', None)
    data["album"] = album if album else data.pop('album', '')
    data["plays"] = to_int(data.pop('plays', 0))
    data["name"] = data.pop('song', 'Unknown Song')
    data["likes"] = to_int(data.pop('likes', 0))
    data["dislikes"] = to_int(data.pop('dislikes', 0))
    data["downloads"] = to_int(data.pop('downloads', 0))
    data["related_songs"] = [extract_short_data(song, Song) for song in data.pop('related', [])]
    data["stories"] = [extract_story(story) for story in data.pop('selfies', [])]
    
    
    if 'item' in data and isinstance(data['item'], int):
        data['item'] = str(data['item'])
    data['date'] = data.get('date', '')
    data['credits'] = data.get('credits', '')
    data['lyric'] = data.get('lyric', '')
    
    data = ensure_required_fields(data, Song)
    return Song(**data)

def extract_video(data) -> Video:
    data["lq_hls"] = data.get('low_web', '')
    data["hq_hls"] = data.get('high_web', '')
    data["name"] = data.pop('song', 'Unknown Video')
    data["views"] = to_int(data.pop('views', 0))
    data["likes"] = to_int(data.pop('likes', 0))
    data["dislikes"] = to_int(data.pop('dislikes', 0))
    data["related_videos"] = [extract_short_data(video, Video) for video in data.pop('related', [])]
    data = ensure_required_fields(data, Video)
    return Video(**data)

def extract_podcast(data) -> Podcast:
    data["is_talk"] = data.pop('talk', False)
    data["plays"] = to_int(data.pop('plays', 0))
    data["likes"] = to_int(data.pop('likes', 0))
    data["dislikes"] = to_int(data.pop('dislikes', 0))
    data["related_podcasts"] = [extract_short_data(podcast, Podcast) for podcast in data.pop('related', [])]
    data = ensure_required_fields(data, Podcast)
    return Podcast(**data)

def extract_artist(data) -> Artist:
    data["photo_thumbnail"] = data.pop('photo_thumb', '')
    data["latest_song"] = extract_short_data(data.pop('latest', {}), Song) if data.get('latest') else None
    data['name'] = data.pop('query', 'Unknown Artist')
    followers = data.pop('followers', {'count': 0, 'following': False, 'plays': 0})
    data["followers_count"] = followers.get('count', 0)
    data["following"] = followers.get('following', False)
    data["plays"] = followers.get('plays', 0)
    data["songs"] = [extract_short_data(mp3, Song) for mp3 in data.pop('mp3s', [])]
    data["albums"] = [extract_short_data(album, Album) for album in data.pop('albums', [])]
    data["videos"] = [extract_short_data(video, Video) for video in data.pop('videos', [])]
    data["podcasts"] = [extract_short_data(podcast, Podcast) for podcast in data.pop('podcasts', [])]
    data["music_playlists"] = [extract_short_data(playlist['playlist'], MusicPlaylist)
                              for playlist in data.pop('playlists', []) if 'playlist' in playlist]
    data = ensure_required_fields(data, Artist)
    return Artist(**data)

def extract_short_data(data, data_type) -> ShortData:
    
    if 'id' in data and isinstance(data['id'], int):
        data['id'] = str(data['id'])
    
    if data_type == Song or data_type == Video:
        data["name"] = data.get("song", "Unknown")
        data["title"] = f"{data.get('artist', 'Unknown')} - {data['name']}"
    elif data_type == Album:
        data["artist"] = data.get("album_artist", "Unknown")
        data["name"] = data.get("album_album", "Unknown Album")
        data["title"] = f"{data['artist']} - {data['name']}"
    elif data_type == Podcast:
        data["artist"] = data.get("podcast_artist", "Unknown")
        data["name"] = data.get("title", "Unknown Podcast")  
        data["title"] = f"{data['artist']} - \"{data['name']}\""
    elif data_type == MusicPlaylist:
        data["name"] = data.get("title", "Unknown Playlist")
        data["title"] = f"{data['name']} - \"{data.get('created_by', 'Unknown')}\""
    elif data_type == VideoPlaylist:
        data["name"] = data.get("title", "Unknown Video Playlist")
    elif data_type == 'show':
        data["artist"] = data.get("date", "Unknown Date")
        data["name"] = data.get("show_title", "Unknown Show")
        data["title"] = f"{data['artist']} - \"{data['name']}\""
        data["permlink"] = data.get("show_permlink", "")
    
    
    for url_field in ['photo', 'photo_player', 'thumbnail']:
        if url_field in data:
            data[url_field] = clean_url(data[url_field])
    
    data = ensure_required_fields(data, ShortData)
    return ShortData(**data)

def extract_search_results(data) -> SearchResults:
    data["songs"] = [extract_short_data(mp3, Song) for mp3 in data.pop('mp3s', [])]
    data["albums"] = [extract_short_data(album, Album) for album in data.pop('albums', [])]
    data["videos"] = [extract_short_data(video, Video) for video in data.pop('videos', [])]
    data["podcasts"] = [extract_short_data(podcast, Podcast) for podcast in data.pop('podcasts', [])]
    data["shows"] = [extract_short_data(show, 'show') for show in data.pop('shows', [])]
    data["users"] = [extract_short_user(profile) for profile in data.pop('profiles', [])]
    data["artist_names"] = [artist.get("name", "") for artist in data.pop('artists', [])]
    data["music_playlists"] = [extract_short_data(playlist['playlist'], MusicPlaylist)
                              for playlist in data.pop('playlists', []) if 'playlist' in playlist]
    return SearchResults(**data)

def extract_video_playlist(data) -> VideoPlaylist:
    data['is_my_playlist'] = data.pop('myplaylist', False)
    data["videos"] = [extract_video(video) for video in data.pop('items', [])]
    return VideoPlaylist(**data)

def extract_music_playlist(data) -> MusicPlaylist:
    data['is_my_playlist'] = data.pop('myplaylist', False)
    data['is_public'] = data.pop('public', False)
    data['has_custom_photo'] = data.pop('custom_photo', False)
    data["sync"] = data.pop('sync', None)
    data["songs"] = [extract_song(song) for song in data.pop('items', [])]
    
    data = ensure_required_fields(data, MusicPlaylist)
    
    
    optional_fields = {'following': None, 'photo_player': None}
    for field, default_value in optional_fields.items():
        if field not in data:
            data[field] = default_value
    
    return MusicPlaylist(**data)

def extract_short_user(data) -> ShortUser:
    
    if 'share_link' not in data:
        username = data.get('username', 'unknown')
        data['share_link'] = f"https://www.radiojavan.com/profile/{username}"
    
    
    if 'id' in data and isinstance(data['id'], int):
        data['id'] = str(data['id'])
    
    
    required_fields = ['id', 'username', 'thumbnail', 'share_link']
    for field in required_fields:
        if field not in data:
            if field == 'id':
                data[field] = 'unknown_id'
            elif field == 'username':
                data[field] = 'unknown_user'
            elif field == 'thumbnail':
                data[field] = 'https://www.radiojavan.com/default_thumb.jpg'
            elif field == 'share_link':
                data[field] = 'https://www.radiojavan.com/profile/unknown'
    
    return ShortUser(**data)

def extract_story(data) -> Story:
    data['is_verified'] = data.pop('verified', False)
    data['lq_link'] = data.pop('hls', '')
    data["song_id"] = data.pop('mp3', '')
    data['is_my_story'] = data.pop('myselfie', False)
    
    user_data = data.pop('user', {})
    if not user_data or not isinstance(user_data, dict):
        user_data = {'username': 'unknown', 'id': 'unknown_id', 'thumbnail': ''}
    
    data['user'] = extract_short_user(user_data)
    data = ensure_required_fields(data, Story)
    return Story(**data)

def extract_album(data):
    if 'id' in data and isinstance(data['id'], int):
        data['id'] = str(data['id'])
    
    data["tracks"] = [extract_song(song) for song in data.pop('album_tracks', [])]
    data['name'] = data.pop('album_album', 'Unknown Album')
    data['artist'] = data.pop('album_artist', 'Unknown Artist')
    data['share_link'] = data.get('album_share_link', f"https://www.radiojavan.com/albums/{data.get('id', '')}")
    data = ensure_required_fields(data, Album)
    return Album(**data)

def extract_my_playlists(data):
    return MyPlaylists(**{
        "music_playlists": [extract_short_data(mpl, MusicPlaylist) 
                           for mpl in data.get('mp3s', {}).get('myplaylists', [])],
        "video_playlists": [extract_short_data(vpl, VideoPlaylist) 
                           for vpl in data.get('videos', {}).get('myplaylists', [])]
    })
    
def extract_notifications_status(data) -> NotificationsStatus:
    return NotificationsStatus(**data)
