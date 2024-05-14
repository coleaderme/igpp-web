#!/usr/bin/env python
INTRO = """
==============================================
About: Instagram Profile Picture HD
Github: https://github.com/coleaderme/igpp
License: MIT
==============================================
"""
import httpx
from glob import glob

def cached(user: str)->bool:
    user = f'{user}.jpg'
    for f in glob('static/*.jpg'):
        f = f.split('/')[-1]
        if user == f:
            return True
    return False


def save(name_ext: str, content: bytes) -> None:
    try:
        with open(f"static/{name_ext}", "wb") as f:
            f.write(content)
    except Exception as save_err:
        print(f"[-] Failed to save to static/{name_ext}\n", save_err)


def web_profile_info_api(username: str, client: httpx.Client) -> dict:
    """user_id from username"""
    print("Getting user id..")
    params = {"username": username}
    r = client.get("https://www.instagram.com/api/v1/users/web_profile_info/", params=params)
    try:
        return r.json()
    except:  # noqa
        print(f"[-] web_profile_info_api({username}) Not Exist / Logged out")
        return {}


def user_api(user_id: str, username: str, client: httpx.Client) -> str:
    """
    Gets bunch of info {dict} about user.
    We need hq pp url only
    """
    print("Getting url..")
    try:
        return client.get(f"https://www.instagram.com/api/v1/users/{user_id}/info/").json()["user"]["hd_profile_pic_url_info"]["url"]
    except:  # noqa
        print(f"[-] user_api({user_id},{username})")
        return ""


def download(username: str, client: httpx.Client) -> bool:
    print(f"User: {username}")
    if cached(username):
        print(f'CACHE HIT: {username}')
        return True
    info = web_profile_info_api(username, client)
    if not info:
        return False  # exit
    if info["data"]["user"] is None:
        print(f"[+] User not exist: {username}")
        return False
    user_id = info["data"]["user"]["id"]
    # print(f"[+] {username:<20}::{user_id:>12}")
    url = user_api(user_id, username, client)
    if url:  # HQ pic
        save(f"{username}.jpg", client.get(url).content)
        return True
    else:  # fallback to 320px
        url = info["data"]["user"]["profile_pic_url_hd"]
        save(f"{username}.jpg", client.get(url).content)
        return True
