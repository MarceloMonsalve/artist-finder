import requests
import datetime
from supabase import create_client, Client
from fake_useragent import UserAgent

supabase: Client = create_client('https://ebwkprvicnnscxhesdez.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVid2twcnZpY25uc2N4aGVzZGV6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwNzc4NjQyNSwiZXhwIjoyMDIzMzYyNDI1fQ.FzEyOC8XsMnxRJNXZ6XAVn5POyyb55Vvcj5UwPFsKsY')

# requests tiktok for a users liked videos
def request_likes(cursor, user_agent, count=30):
    url = 'https://www.tiktok.com/api/favorite/item_list/'
    params = {
        'WebIdLastTime': '1707766329',
        'aid': '1988',
        'app_language': 'en',
        'app_name': 'tiktok_web',
        'browser_language': 'en-US',
        'browser_name': 'Mozilla',
        'browser_online': 'true',
        # 'browser_platform': 'MacIntel',
        'browser_version': f'{user_agent}',
        'channel': 'tiktok_web',
        'cookie_enabled': 'true',
        'count': f'{count}',
        'coverFormat': '2',
        'cursor': f'{cursor}',
        'device_id': '7334800398581286442',
        'device_platform': 'web_pc',
        'focus_state': 'true',
        'from_page': 'user',
        'history_len': '6',
        'is_fullscreen': 'false',
        'is_page_visible': 'true',
        'language': 'en',
        'odinId': '7334800484082287658',
        'os': 'mac',
        'referer' : 'https://www.tiktok.com/@cecilpark123',
        'region': 'US',
        'root_referer': 'https://www.google.com/',
        'screen_height': '1117,',
        'screen_width': '1728',
        'secUid': 'MS4wLjABAAAAO0d5uALJNnBjdwXb8j-ZBv6cVXBP7_UpM46o-iJuWDSsJlGZuJjOP_n14qrys_1a',
        'tz_name': 'America/Los_Angeles',
        'webcast_language': 'en',
        'msToken': '6PARAlcj06A0t9qtXcREt0k6wqz0kgtxMIqwS_Kr40FL8FqHn93dRjFhJK-o4A_XDuyY9vflEeADPOE5ib6H59uVEi5zwqv0SBDPJHSwAESD-WGEPiQDYkrwNvvQy7BY15bGnoWb24PCjN1j',
        'X-Bogus': 'DFSzswVYsp0ANxChtqcC4t9WcBrc',
        '_signature': '_02B4Z6wo00001NYExJAAAIDA1gTEknZDJtzWBMAAAFBQ01',
    }
    return requests.get(url, params=params)

# gets users liked videos up until last liked video
def get_videos():
    last_video = get_last_video()
    user_agent = UserAgent().random
    videos = []
    has_more = True
    cursor = 0
    while has_more == True:
        response = request_likes(cursor, user_agent)
        if response.status_code == 200:
            data = response.json()
            if 'hasMore' not in data or 'itemList' not in data:
                print("Error: Data not found")
                exit()
            has_more = data['hasMore']
            for item in data['itemList']:
                if item['id'] == last_video:
                    has_more = False
                    break
                video_data = {
                    'video_id': item['id'],
                    'user_id': item['author']['id'],
                    'user_unique_id': item['author']['uniqueId'],
                }
                videos.append(video_data)
            cursor = data['cursor']
    if videos:
        data, _ = supabase.table('vars').update({'value': videos[0]['video_id']}).eq('name', 'last_video').execute()
    return videos

# takes a list of videos and returns unique usernames in it and adds date
def prepare_accounts(videos):
    unique_users = []
    for item in videos:
        user_id = item.get('user_id')
        if user_id and user_id not in [user.get('id') for user in unique_users]:
            unique_users.append({'id': user_id, 'unique_id': item.get('user_unique_id'), 'date': datetime.datetime.now().isoformat()})
    return unique_users


# gets the last video looked at from the previous time running the script (currently only demo functionality)
def get_last_video():
    response = supabase.table('vars').select("*").eq('name','last_video').execute()
    value = response.data[0]['value']
    return value

videos = get_videos()
unique_accounts = prepare_accounts(videos)
data, count = supabase.table('artists').upsert(unique_accounts).execute()


# DB_PASSWORD = '7Fx%%kmiQ/g#nd/'