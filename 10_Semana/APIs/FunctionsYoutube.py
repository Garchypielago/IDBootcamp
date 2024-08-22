from googleapiclient.discovery import build
from dateutil import parser
import pandas as pd
from IPython.display import JSON

# Data viz packages
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime


def get_channel_stats(youtube, channel_ids):
    
    """
    Get channel stats
    
    Params:
    ------
    youtube: build object of Youtube API
    channel_ids: list of channel IDs
    
    Returns:
    ------
    dataframe with all channel stats for each channel ID
    
    """
    
    all_data = []
    
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=','.join(channel_ids)
    )
    response = request.execute()

    # loop through items
    for item in response['items']:
        data = {'channelName': item['snippet']['title'],
                'subscribers': item['statistics']['subscriberCount'],
                'views': item['statistics']['viewCount'],
                'totalVideos': item['statistics']['videoCount'],
                'playlistId': item['contentDetails']['relatedPlaylists']['uploads']
        }
        
        all_data.append(data)
        
    return pd.DataFrame(all_data)

def get_video_ids(youtube, playlist_id):
    
    video_ids = []
    
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlist_id,
        maxResults = 50
    )
    response = request.execute()
    
    for item in response['items']:
        video_ids.append(item['contentDetails']['videoId'])
        
    next_page_token = response.get('nextPageToken')# metodo get (diccionarios), para que no me rompa el codigo
    while next_page_token is not None:
        request = youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId = playlist_id,
                    maxResults = 50,
                    pageToken = next_page_token)
        response = request.execute()

        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])

        next_page_token = response.get('nextPageToken')
        
    return video_ids
    
    
def get_video_details(youtube, video_ids):

    all_video_info = []
    
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute() 

        for video in response['items']:
            stats_to_keep = {'snippet': ['channelTitle', 'title', 'description', 'tags', 'publishedAt'],
                             'statistics': ['viewCount', 'likeCount', 'favouriteCount', 'commentCount'],
                             'contentDetails': ['duration', 'definition', 'caption']
                            }
            video_info = {}
            video_info['video_id'] = video['id']

            for k in stats_to_keep.keys():
                for v in stats_to_keep[k]:
                    try:
                        video_info[v] = video[k][v]
                    except:
                        video_info[v] = None

            all_video_info.append(video_info)
    df=pd.DataFrame(all_video_info)
    # df['publishedAt']=df['publishedAt'].apply(lambda x: datetime.fromisoformat(x[:-1]))
    return df

def get_comments_elements(youtube, channel_ids):
    request = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=channel_ids,
            maxResults = 50
            
        )
    response = request.execute()
    new_token = response.get("nextPageToken")
    
    all_data = []
    
    for _ in response["items"]:
        data={"User": _["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
             "Comment": _["snippet"]["topLevelComment"]["snippet"]["textOriginal"],
             "Date": _["snippet"]["topLevelComment"]["snippet"]["updatedAt"],
             "Video_Id": _["snippet"]["videoId"]}
        if "replies" in _:
            data["reply"] = _["replies"]["comments"][0]["snippet"]["textOriginal"]
        
        all_data.append(data)
        
    while new_token is not None:
        request = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=channel_ids,
            pageToken = new_token,
            maxResults = 50
        )
        response = request.execute()
        new_token = response.get("nextPageToken")

        for _ in response["items"]:
            data={"User": _["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                 "Comment": _["snippet"]["topLevelComment"]["snippet"]["textOriginal"],
                 "Date": _["snippet"]["topLevelComment"]["snippet"]["updatedAt"],
                 "Video_Id": _["snippet"]["videoId"]}
            if "replies" in _:
                data["reply"] = _["replies"]["comments"][0]["snippet"]["textOriginal"]

            all_data.append(data)
    
    df = pd.DataFrame(all_data)
    df["len_com"] = df["Comment"].map(lambda x: len(x))
    
    return df
