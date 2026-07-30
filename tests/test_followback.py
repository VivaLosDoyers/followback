import unittest

from followback import find_not_following_back


class FindNotFollowingBackTests(unittest.TestCase):
    def test_returns_following_users_missing_from_followers(self) -> None:
        followers = {"alice", "bob"}
        following = {"alice", "bob", "carol", "dave"}

        self.assertEqual(find_not_following_back(followers, following), ["carol", "dave"])

    def test_deduplicates_and_sorts_results(self) -> None:
        followers = ["alice", "bob"]
        following = ["dave", "carol", "dave", "bob"]

        self.assertEqual(find_not_following_back(followers, following), ["carol", "dave"])


if __name__ == "__main__":
    unittest.main()
