"""CSV normalization helpers for uploaded Twitter/X datasets."""

from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = ["user_id", "tweet", "followers", "following", "tweets_count"]

COLUMN_ALIASES = {
    "user_id": ("user_id", "author_id", "username", "screen_name", "user", "handle"),
    "tweet": ("tweet", "text", "full_text", "tweet_text", "content", "body"),
    "followers": ("followers", "followers_count", "follower_count"),
    "following": ("following", "following_count", "friends_count"),
    "tweets_count": ("tweets_count", "tweet_count", "statuses_count", "total_tweets"),
}


def _normalized_columns(frame: pd.DataFrame) -> dict[str, str]:
    return {column.strip().lower(): column for column in frame.columns}


def _first_existing_column(frame: pd.DataFrame, aliases: tuple[str, ...]) -> pd.Series | None:
    columns = _normalized_columns(frame)
    for alias in aliases:
        source_column = columns.get(alias)
        if source_column is not None:
            return frame[source_column]
    return None


def _text_series(frame: pd.DataFrame, aliases: tuple[str, ...]) -> pd.Series:
    series = _first_existing_column(frame, aliases)
    if series is None:
        raise ValueError("Uploaded CSV needs a tweet text column.")
    return series.fillna("").astype(str).str.strip()


def _numeric_series(frame: pd.DataFrame, aliases: tuple[str, ...]) -> pd.Series:
    series = _first_existing_column(frame, aliases)
    if series is None:
        return pd.Series([0] * len(frame), index=frame.index)
    return pd.to_numeric(series, errors="coerce").fillna(0).astype(int)


def normalize_tweet_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Return the dashboard schema from a native or Xquik export CSV."""
    normalized = pd.DataFrame(index=frame.index)
    normalized["user_id"] = _text_series(frame, COLUMN_ALIASES["user_id"])
    normalized["tweet"] = _text_series(frame, COLUMN_ALIASES["tweet"])
    normalized["followers"] = _numeric_series(frame, COLUMN_ALIASES["followers"])
    normalized["following"] = _numeric_series(frame, COLUMN_ALIASES["following"])
    normalized["tweets_count"] = _numeric_series(frame, COLUMN_ALIASES["tweets_count"])

    normalized = normalized[normalized["tweet"] != ""]
    return normalized[REQUIRED_COLUMNS]
