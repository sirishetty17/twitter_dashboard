import unittest

import pandas as pd

from twitter_dashboard.xquik_csv import REQUIRED_COLUMNS, normalize_tweet_frame


class XquikCsvTest(unittest.TestCase):
    def test_normalizes_xquik_export_columns(self):
        frame = pd.DataFrame(
            [
                {
                    "username": "analyst",
                    "full_text": "Useful dashboard signal",
                    "followers_count": "1200",
                    "following_count": "300",
                    "tweet_count": "75",
                }
            ]
        )

        normalized = normalize_tweet_frame(frame)

        self.assertEqual(list(normalized.columns), REQUIRED_COLUMNS)
        self.assertEqual(normalized.iloc[0]["user_id"], "analyst")
        self.assertEqual(normalized.iloc[0]["tweet"], "Useful dashboard signal")
        self.assertEqual(normalized.iloc[0]["followers"], 1200)
        self.assertEqual(normalized.iloc[0]["following"], 300)
        self.assertEqual(normalized.iloc[0]["tweets_count"], 75)

    def test_drops_blank_tweet_rows_and_defaults_missing_counts(self):
        frame = pd.DataFrame(
            [
                {"user": "empty", "text": ""},
                {"user": "known", "text": "Real row"},
            ]
        )

        normalized = normalize_tweet_frame(frame)

        self.assertEqual(len(normalized), 1)
        self.assertEqual(normalized.iloc[0]["user_id"], "known")
        self.assertEqual(normalized.iloc[0]["followers"], 0)


if __name__ == "__main__":
    unittest.main()
