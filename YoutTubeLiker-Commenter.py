import os
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


videos_list = get_channel_videos("UCxambigWU3QMK9UJXU2mwPg")
print(len(videos_list))

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
    # print(response)


def update_comment_videos(comment, text):
    comment["snippet"]["topLevelComment"]["snippet"]["textOriginal"] = text
    update_result = youtube.commentThreads().update(part="snippet", body=comment)
    # request = youtube.commentThreads().update(
    #         part="snippet",
    #         body={
    #             "id":commentId,
    #             "snippet" :{
    #                 "videoId": videoId,
    #                 "channelId": channelId,
    #                 "topLevelComment": {
    #                     "snippet": {
    #                         "textOriginal": comment,
    #                     }
    #                 }
    #             }
    #         }
    #     )

    response = update_result.execute()
    # print(response)


def get_comments(video_Id, channel_Id):
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_Id,
    )
    response = request.execute()
    return response
    # print(response)


# comment_we_want_to_update=get_comments(videos_list[1]["snippet"]["resourceId"]["videoId"], videos_list[0]["snippet"]["channelId"])["items"][0]
video_id_comment_check = videos_list[0]["snippet"]["resourceId"]["videoId"]
channel_id_comment_check = videos_list[0]["snippet"]["channelId"]
for index in range(47):
    comment_on_videos(video_id_comment_check, channel_id_comment_check, str(index))
    print(index)


# print(comment_we_want_to_update["snippet"]["topLevelComment"]["snippet"]["textOriginal"])


# comment_on_videos(
#     videoId=videos_list[0]["snippet"]["resourceId"]["videoId"],
#     channelId=videos_list[0]["snippet"]["channelId"],
#     comment="testing response code"
# )

# for index, video in enumerate(videos_list):
#     #youtube.videos().rate(id=video["snippet"]["resourceId"]["videoId"], rating="like").execute()
#     #print(videos_list[index % len(videos_list)])
#     # print(video["snippet"]["resourceId"]["videoId"])
#     # print(video["snippet"]["channelId"])
#     # print(comment_list[index % len(comment_list)])
#     print(index)
#     comment_on_videos(
#         videoId=video["snippet"]["resourceId"]["videoId"],
#         channelId=video["snippet"]["channelId"],
#         comment=comment_list[index % len(comment_list)])

# for index in range(0, 47):
#     print(index)
#     update_comment_videos(
#         commentId="UgyyPq19Gf9T6-xlYFJ4AaABAg",
#         videoId=videos_list[0]["snippet"]["resourceId"]["videoId"],
#         channelId=videos_list[0]["snippet"]["channelId"],
#         comment="")

# youtube.videos().rate(id=videos_list[0]["snippet"]["resourceId"]["videoId"], rating="like").execute()


# videos_list[0]["snippet"]["resourceId"]["videoId"]
# videos_list[0]["snippet"]["channelId"]

# "nJ384wg3g5A" videos_list[0]["id"]
# request = youtube.playlistItems().list(
#     part="snippet", playlistId="UUxambigWU3QMK9UJXU2mwPg"
# )

# response = request.execute()

# print(response)
