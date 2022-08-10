import sys
import requests
import json
import re
import ffmpeg
import os
from tqdm import tqdm

USER_AGENT_HEADER = {"User-agent": "Mozilla/5.0"}


def download(reddit_post_url: str) -> None:
    res = make_request(reddit_post_url + ".json")
    json_data = json.loads(res.text)

    if not is_video(json_data):
        print("Post does not contains video")
        sys.exit()

    print("\nDownloading video file...")
    video_url = get_video_url(json_data)
    video_title = get_post_name(json_data) + "_video.mp4"
    download_file(video_url, video_title)

    print("\nDownloading audio file...")
    audio_url = get_audio_url(json_data)
    audio_title = get_post_name(json_data) + "_audio.mp4"
    download_file(audio_url, audio_title)

    print("\nMerging video and audio...")
    input_video = ffmpeg.input(video_title)
    input_audio = ffmpeg.input(audio_title)
    output_title = get_post_name(json_data) + ".mp4"
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(output_title, loglevel="quiet").run()

    os.remove(video_title)
    os.remove(audio_title)


def make_request(url: str) -> requests.Response:
    res = requests.get(url, headers=USER_AGENT_HEADER)

    if res.status_code == 200:
        return res

    print(f"Failed to download video. Http status code: {res.status_code}")
    sys.exit()


def download_file(url: str, out_file_name: str) -> None:
    res = requests.get(url, headers=USER_AGENT_HEADER, stream=True)
    with open(out_file_name, 'wb') as f:
        pbar = tqdm(unit="B", total=int(res.headers['Content-Length']))
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                pbar.update(len(chunk))
                f.write(chunk)


def is_video(json_data) -> bool:
    return get_post_data(json_data)["is_video"]


def get_post_data(json_data):
    return json_data[0]["data"]["children"][0]["data"]


def get_video_url(json_data) -> str:
    return get_post_data(json_data)["media"]["reddit_video"]["fallback_url"]


def get_audio_url(json_data) -> str:
    video_url = get_video_url(json_data)
    return re.sub("DASH_.*?(?=\\.)", "DASH_audio", video_url)


def get_post_name(json_data) -> str:
    return get_post_data(json_data)["name"]


def main() -> None:
    if len(sys.argv) == 1:
        print("Please enter url to reddit post")
    else:
        download(sys.argv[1])


if __name__ == '__main__':
    main()
