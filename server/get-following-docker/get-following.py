import requests
import re
from supabase import create_client, Client


supabase: Client = create_client('https://ebwkprvicnnscxhesdez.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVid2twcnZpY25uc2N4aGVzZGV6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwNzc4NjQyNSwiZXhwIjoyMDIzMzYyNDI1fQ.FzEyOC8XsMnxRJNXZ6XAVn5POyyb55Vvcj5UwPFsKsY')

def get_next_account():
    response = supabase.table('account_queue').select("*").eq('seen', False).limit(1).execute()
    return response.data[0]["id"], response.data[0]["unique_id"]

def delete_account(id):
    data, count = supabase.table('account_queue').delete().eq('id', id).execute()

def get_following(user_id, max_followers, allow_verified):
    def is_artist(bio):
        points = {
            "pop": 3, "alt": 2, "rock": 3, "hip-hop/rap": 3, "country": 3, "r&b": 3, "soul": 3, "edm": 3, "all": 1,
            "jazz": 3, "punk": 3, "indie": 3, "classical": 3, "reggae": 3, "feat": 1, "go": 1, "youtube": 1, "check": 2, "out": 2,
            "spotify": 4, "singer": 3, "make": 2, "song": 3, "listen": 2, "songs": 3, "tunes": 2, "save": 3, "gmail": 2, "i": 1,
            "ep": 3, "stream": 4, "album": 3, "singing": 2, "new": 1, "rapper": 4, "presave": 4, "pre save": 4, "pre-save": 4,
            "artist": 3, "official": 1, "musician": 2, "link": 2, "tour": 3, "single": 2, "platforms": 3, "listen": 3, "to": 1,
            "streaming": 2, "my": 1, "click": 1, "everywhere": 2, "now": 2, "out": 2, "songwriter": 4, "song writer": 4, "song-writer": 4,
            "show": 1, "soundcloud": 4, "band": 4, "debut": 3, "music": 3, "independant": 2, "below": 2, "merch": 2, "⬇️": 1, "fan": -5, "fanbase": -5, 
            "author": -5, "writer": -1, "storyteller": -3, "producer": 1
        }
        words = re.findall(r'\w+|\W+', bio.lower())
        unique_words = list(set(words))
        score = 0
        for word in unique_words:
            if word in points:
                score += points[word]
        return score, score >= 4, unique_words

    url = "https://tiktok-scraper7.p.rapidapi.com/user/following"
    querystring = {"user_id":user_id,"count":"100","time":"0"}
    headers = {
        "X-RapidAPI-Key": "b87bdcb7demsh254452f23161a24p1b6651jsn0dc63627d18e",
        "X-RapidAPI-Host": "tiktok-scraper7.p.rapidapi.com"
    }
    data = requests.get(url, headers=headers, params=querystring).json()
    if data['code'] == -1: return -1

    accounts_to_save = []
    for account in data['data']['followings']:
        bio = account['signature'].lower()
        follower_count = account['follower_count']
        verified = account['verified']
        if is_artist(bio)[1] and follower_count < max_followers and (not verified or allow_verified):
            account_data = {
                'id': account['id'],
                'unique_id': account['unique_id'],
                # 'signature': account['signature'],
                # 'follower_count': account['follower_count'],
                # 'total_favorited': account['total_favorited']
            }
            accounts_to_save.append(account_data)

    return accounts_to_save




while(True):
    response = supabase.table('account_queue').select("*").eq('seen', False).limit(1).execute()
    if response.data:
        id, unique_id = response.data[0]["id"], response.data[0]["unique_id"]
        following = get_following(id, 100000, False)
        if following == -1:
            data, count = supabase.table('account_queue').update({'seen': True}).eq('id', id).execute()
        else:
            # print(following)
            data, error = supabase.rpc('add_artists', {'data': following}).execute()
            data, count = supabase.table('account_queue').update({'seen': True}).eq('id', id).execute()
            break
    else:
        print("No accounts left")
        break