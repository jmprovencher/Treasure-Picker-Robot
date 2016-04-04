from unittest import TestCase
from stationbase.interface.FeedVideoStation import FeedVideoStation


class TestFeedVideoStation(TestCase):

    def test_aucune_capture_apres_initialisation(self):
        feedVideo = FeedVideoStation()

        self.assertIsNotNone(feedVideo.captureTable)
