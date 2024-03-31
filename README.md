# YOUTUBE批量下载爬虫

## 安装

* 虚拟环境安装

```python
python -m venv venv
.\venv\Scripts\activate 
pip install -r requirements.txt
```

* 下载器安装

[motrix](https://motrix.app/)

魔改了youtube-dl库，请在安装虚拟环境之后，进入 venv\Lib\site-packages\youtube_dl\extractor\youtube.py 文件

将1794行的

```python
'uploader_id': self._search_regex(r'/(?:channel|user)/([^/?&#]+)', owner_profile_url, 'uploader id') if owner_profile_url else None
```

替换为
```python
'uploader_id': self._search_regex(r'/(?:channel|user)/([^/?&#]+)', owner_profile_url, 'uploader id', fatal=False) if owner_profile_url else None
```

否则程序将无法正常运行