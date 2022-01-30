import json

import requests

from comments import Comments

VIDEO_ID = "ACdh-yzENXM"

RAPID_API_TOKEN = "0f35b55f3amshba4c2b9f3590916p1b8d35jsn2efedc4c7c9a"


def simple_call(video_id: str) -> Comments:
    url = "https://youtube-search6.p.rapidapi.com/video/comments/"
    querystring = {"videoId": video_id}
    headers = {
        "x-rapidapi-host": "youtube-search6.p.rapidapi.com",
        "x-rapidapi-key": RAPID_API_TOKEN,
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return Comments(**response.json())


def continuation_call(video_id: str, continuation_token: str) -> Comments:
    url = "https://youtube-search6.p.rapidapi.com/video/comments/continuation/"

    payload = {"continuationToken": continuation_token, "videoId": video_id}
    headers = {
        "content-type": "application/json",
        "x-rapidapi-host": "youtube-search6.p.rapidapi.com",
        "x-rapidapi-key": RAPID_API_TOKEN,
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

    return Comments(**response.json())


def get_comments(video_id: str, continuation_token: str = None) -> Comments:
    if not continuation_token:
        return simple_call(video_id=video_id)
    return continuation_call(video_id=video_id, continuation_token=continuation_token)


list_of_comments = []

comments = get_comments(video_id=VIDEO_ID)
list_of_comments.extend(comments.comments)

while len(list_of_comments) < 2500:
    comments = get_comments(
        video_id=VIDEO_ID, continuation_token=comments.continuation_token
    )
    list_of_comments.extend(comments.comments)
    print(len(list_of_comments))

with open("comments.json", mode="w", encoding="utf-8") as file:
    file.write(json.dumps(list_of_comments))
