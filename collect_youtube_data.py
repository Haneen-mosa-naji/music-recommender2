from googleapiclient.discovery import build
import csv
import time

API_KEY = "AIzaSyCf4A7VwNKlbPxu3ieFzBUmqXiVsPC5Qes"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

search_queries = ["أغاني عربية", "أغاني رومانسية", "أغاني حزينة",
                  "Arabic music", "اغاني مصرية", "اغاني لبنانية"]

all_videos = []
seen_video_ids = set()

def get_videos_for_query(query, max_total=60):
    videos = []
    next_page_token = None
    while len(videos) < max_total:
        request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=20,
            videoCategoryId="10",
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response.get('items', []):
            video_id = item['id']['videoId']
            if video_id in seen_video_ids:
                continue
            seen_video_ids.add(video_id)

            video_data = {
                'Video_ID': video_id,
                'Title': item['snippet']['title'],
                'Artist': item['snippet']['channelTitle'],
                'Channel': item['snippet']['channelTitle'],
                'Published_At': item['snippet']['publishedAt'],
                'URL': f"https://www.youtube.com/watch?v={video_id}",
                'ImageURL': item['snippet']['thumbnails']['medium']['url']
            }
            videos.append(video_data)

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
        time.sleep(1)  # للتقليل من احتمال تجاوز حد الـ API

    return videos

# جمع النتائج لكل استعلام
for query in search_queries:
    all_videos.extend(get_videos_for_query(query))

# حفظ النتائج في ملف CSV
with open("arabic_music_data.csv", mode='w', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['Video_ID', 'Title', 'Artist', 'Channel',
                                              'Published_At', 'URL', 'ImageURL'])
    writer.writeheader()
    for video in all_videos:
        writer.writerow(video)

print(f"تم جمع {len(all_videos)} فيديو موسيقي وحفظها في ملف arabic_music_data.csv")