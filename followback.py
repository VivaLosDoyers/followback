from __future__ import annotations

import argparse
import os
from typing import Iterable

import requests


def _build_session(sessionid: str) -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0",
            "X-IG-App-ID": "936619743392459",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/",
        }
    )
    session.cookies.set("sessionid", sessionid)
    return session


def _fetch_user_id(session: requests.Session, username: str) -> str:
    response = session.get(
        "https://i.instagram.com/api/v1/users/web_profile_info/",
        params={"username": username},
        timeout=30,
    )
    response.raise_for_status()
    user = response.json().get("data", {}).get("user")
    if not user or "id" not in user:
        raise ValueError(f"Could not find user '{username}'")
    return str(user["id"])


def _fetch_friendship_usernames(
    session: requests.Session,
    user_id: str,
    endpoint: str,
) -> set[str]:
    usernames: set[str] = set()
    next_max_id: str | None = None

    while True:
        params = {"count": 200}
        if next_max_id:
            params["max_id"] = next_max_id

        response = session.get(
            f"https://i.instagram.com/api/v1/friendships/{user_id}/{endpoint}/",
            params=params,
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()

        for user in payload.get("users", []):
            username = user.get("username")
            if username:
                usernames.add(username)

        next_max_id = payload.get("next_max_id")
        if not payload.get("next_max_id"):
            break

    return usernames


def get_followers_and_following(username: str, sessionid: str) -> tuple[set[str], set[str]]:
    session = _build_session(sessionid)
    user_id = _fetch_user_id(session, username)
    followers = _fetch_friendship_usernames(session, user_id, "followers")
    following = _fetch_friendship_usernames(session, user_id, "following")
    return followers, following


def find_not_following_back(
    followers: Iterable[str],
    following: Iterable[str],
) -> list[str]:
    return sorted(set(following) - set(followers))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Show Instagram accounts a user follows that do not follow back",
    )
    parser.add_argument("username", help="Instagram username to inspect")
    parser.add_argument(
        "--sessionid",
        default=os.getenv("INSTAGRAM_SESSIONID"),
        help="Instagram sessionid cookie (or set INSTAGRAM_SESSIONID)",
    )
    args = parser.parse_args()

    if not args.sessionid:
        raise SystemExit("Missing sessionid. Pass --sessionid or set INSTAGRAM_SESSIONID.")

    followers, following = get_followers_and_following(args.username, args.sessionid)
    for user in find_not_following_back(followers, following):
        print(user)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
