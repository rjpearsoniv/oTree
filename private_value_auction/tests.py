# -*- coding: utf-8 -*-
from __future__ import division
import private_value_auction.views as views
from private_value_auction._builtin import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # Introduction
        self.submit(views.Introduction)

        # bid
        self.submit(views.Bid, {"bid_amount": round(random.uniform(self.subsession.min_allowable_bid, self.subsession.max_allowable_bid), 1)})

        # results
        self.submit(views.Results)
