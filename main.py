from utils.driver import webDriver
from youtube_dl import YoutubeDL
import requests

import requests
import json
import time


def start_download(save_folder: str, file_title: str, download_url: str):
    url = "http://127.0.0.1:16800/jsonrpc"
    payload = json.dumps(
        {
            "jsonrpc": "2.0",
            "method": "aria2.addUri",
            "id": "1",
            "params": [
                [download_url],
                {"dir": "C:/Users/11963/Downloads/Not Safe", "out": f"{title}.mp4"},
            ],
        }
    )
    headers = {"Content-Type": "application/json"}
    requests.request("POST", url, headers=headers, data=payload)
    time.sleep(1)


def get_download_link(video_url):
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "proxy": "socks5://127.0.0.1:10808",
    }
    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(video_url, download=False)
        if "formats" in result:
            download_formats = result["formats"][-1]
            return result["title"], download_formats["url"]


with webDriver() as driver:
    save_folder = "C:/Users/11963/Downloads/Not Safe"  # 要保存的文件夹
    youtube_url = "https://www.youtube.com/@NotSafe/videos"  # 下载内容的网址

    driver.get(youtube_url)
    if ele_btn_cookies := driver.wait_element_by_xpath(
        '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/form[2]/div/div/button/span',
        wait_time=10,
    ):
        ele_btn_cookies.click()
    if not driver.wait_element_by_xpath(
        '//*[@id="buttons"]/ytd-button-renderer/yt-button-shape/a/yt-touch-feedback-shape/div/div[2]',
        wait_time=15,
    ):
        raise Exception("网页加载失败，请重试")

    # 加载到最下方
    prev_video_length = 0
    while prev_video_length != driver.get_video_length():
        prev_video_length = driver.get_video_length()
        driver.execute_script("window.scrollBy(0, 99999)")
        time.sleep(10)  # 等待加载

    ele_video_url_list = driver.page_source_selector().xpath(
        '//ytd-rich-item-renderer[@class="style-scope ytd-rich-grid-row"]/div/ytd-rich-grid-media/div/div/ytd-thumbnail[1]//a[@id="thumbnail"]'
    )
    for ele_video_url in ele_video_url_list:
        video_url = f'https://www.youtube.com/{ele_video_url.xpath("@href").get()}'
        title, url = get_download_link(video_url)
        title = (
            title.replace(":", " ")
            .replace('"', "")
            .replace("*", "")
            .replace("<", "")
            .replace(">", "")
            .replace("/", "")
            .replace("\\", "")
            .replace("|", "")
        )  # 整理文件名
        print(f"开始下载 {title} {url}")
        start_download(save_folder, title, url)
