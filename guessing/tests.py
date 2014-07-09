import ptree.test
import guessing.views as views
from guessing.utilities import ParticipantMixIn, ExperimenterMixIn


class ParticipantBot(ParticipantMixIn, ptree.test.ParticipantBot):

    def play(self):
        pass


class ExperimenterBot(ExperimenterMixIn, ptree.test.ExperimenterBot):

    def play(self):
        pass