import os
import time
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

credentials = None

# token.pickle stores the user's credentials from previously successful logins
if os.path.exists("token.pickle"):
    print("Loading Credentials From File...")
    with open("token.pickle", "rb") as token:
        credentials = pickle.load(token)

# If there are no valid credentials available, then either refresh the token or log in.
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print("Refreshing Access Token...")
        credentials.refresh(Request())
    else:
        print("Fetching New Tokens...")
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secrets.json",
            scopes=["https://www.googleapis.com/auth/youtube.force-ssl"],
        )

        flow.run_local_server(
            port=8080, prompt="consent", authorization_prompt_message=""
        )
        credentials = flow.credentials

        # Save the credentials for the next run
        with open("token.pickle", "wb") as f:
            print("Saving Credentials for Future Use...")
            pickle.dump(credentials, f)

youtube = build("youtube", "v3", credentials=credentials)

# gets a list of all the videos of a channel usings it's channel id
def get_channel_videos(channel_id):
    resource = youtube.channels().list(id=channel_id, part="contentDetails").execute()

    playlist_id = resource["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    videos = []

    next_page_token = None
    while 1:
        res = (
            youtube.playlistItems()
            .list(
                playlistId=playlist_id,
                part="snippet",
                maxResults=50,
                pageToken=next_page_token,
            )
            .execute()
        )

        videos += res["items"]
        next_page_token = res.get("nextPageToken")

        if next_page_token is None:
            break

    return videos


# Update the string with desired youtube channel id
videos_list = get_channel_videos("Desired-YouTube-Id")

# comments on the particular video
def comment_on_videos(videoId, channelId, comment):
    request = youtube.commentThreads().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": videoId,
                "channelId": channelId,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": comment,
                    }
                },
            }
        },
    )

    response = request.execute()


# List of generic comments to comment on videos
comment_list = [
    "I love the content keep it up!!",
    "Very informational thank you!",
    "Amazing work!",
    "I love this!!",
    "Thank you clear explanation",
    "Awesome content keep it up!!",
    "Absolutely love the 5 minute length!",
    "This is very insightful, thanks for sharing",
    "Great job keep it up.",
    "I really enjoy these videos.",
]

for index, video in enumerate(videos_list):
    # this is to like the videos
    youtube.videos().rate(
        id=video["snippet"]["resourceId"]["videoId"], rating="like"
    ).execute()

    # this is to comment on the 15 videos using the created comment_list
    # note this only works for the most recent 15 videos
    if index < 15:
        comment_on_videos(
            videoId=video["snippet"]["resourceId"]["videoId"],
            channelId=video["snippet"]["channelId"],
            comment=comment_list[index % len(comment_list)],
        )

# not used in this program but
# Takes a comment and updates it's to become text
def update_comment_videos(comment, text):
    comment["snippet"]["topLevelComment"]["snippet"]["textOriginal"] = text
    update_result = youtube.commentThreads().update(part="snippet", body=comment)
    response = update_result.execute()


# not used in this program but
# gets a list of comments on a particular YouTube video
def get_comments(video_Id, channel_Id):
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_Id,
    )
    response = request.execute()
    return response