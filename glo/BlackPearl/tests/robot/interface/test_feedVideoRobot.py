from unittest import TestCase
from robot.interface.FeedVideoRobot import FeedVideoRobot

class TestFeedVideoRobot(TestCase):
    def test_aucune_capture_apres_initialisation(self):
        feedVideo = FeedVideoRobot()
        self.assertFalse(feedVideo.capturer)

    def test_demarrerCapture_demarre_capture(self):
        feedVideo = FeedVideoRobot()
        feedVideo.demarrerCapture()
        self.assertTrue(feedVideo.capturer)

    def test_suspendreCapture_suspend_capture(self):
        feedVideo = FeedVideoRobot()
        feedVideo.demarrerCapture()
        self.assertTrue(feedVideo.capturer)
        feedVideo.suspendreCapture()
        self.assertFalse(feedVideo.capturer)
