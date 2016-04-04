from unittest import TestCase
from stationbase.interface.StationBase import StationBase


class StationBase(TestCase):

    def setUp(self):
        self.stationBase = StationBase("routine complete", 2)
        self.stationBase.initialisationTrajectoire()

    def test_initTrajectoire(self):
        self.stationBase.initialisationTrajectoire()

        self.assertIsNotNone(self.stationBase.carte.trajectoire.grilleCellule)

    def test_attendreRobotPret(self):
        self.stationBase.attendreRobotPret()

        self.assertTrue(self.stationBase.threadCommunication.getRobotPret())

    def test_deplacer(self):
        self.stationBase.initialisationTrajectoire()
        l = len(self.stationBase.trajectoireReel)
        self.stationBase.deplacer()
        bool = self.stationBase.trajectoireReel == [] or len(self.stationBase.trajectoireReel) == l - 1

        self.assertTrue(bool)

    def test_orienter(self):
        self.stationBase.angleDesire = 90
        self.stationBase.orienter('deplacement')
        bool = 87 <= self.stationBase.getCarte().getRobot().getOrientation() <= 93

        self.assertTrue(bool)

    def test_trouverTrajectoirePrevu(self):
        self.stationBase.trouverTrajectoirePrevu((500, 500))

        self.assertIsNotNone(self.stationBase.trajectoirePrevue)
        self.assertIsNotNone(self.stationBase.trajectoireReel)

    def test_aligner(self):
        self.stationBase.aligner('alignement_ile')

        self.assertTrue(self.stationBase.threadCommunication.getAttenteDuRobot())

    def test_touverOrientationDesire(self):
        angle = self.stationBase.trouverOrientationDesire((0, 0), (5, 5))

        self.assertEqual(angle, 45)

    def test_trouverDeplacementOrientation(self):
        self.stationBase.angleDesire = 90
        dep = self.stationBase.trouverDeplacementOrientation()
        bool = 0 <= dep <180

        self.assertTrue(bool)





