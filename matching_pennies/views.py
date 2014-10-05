# -*- coding: utf-8 -*-
from __future__ import division
import matching_pennies.models as models
from matching_pennies._builtin import Page, WaitPage
from otree.common import Money


def variables_for_all_templates(self):
    return {'point_value': self.subsession.point_value,
            'total_q': 1,
            'total_rounds': self.subsession.number_of_rounds,
            'round_number': self.subsession.round_number,
            'role': self.player.role()}


class Introduction(Page):

    template_name = 'matching_pennies/Introduction.html'

    def participate_condition(self):
        return self.subsession.round_number == 1


class QuestionOne(Page):

    template_name = 'matching_pennies/Question.html'

    def participate_condition(self):
        return self.subsession.round_number == 1

    form_model = models.Player
    form_fields = ['training_question_1']

    def variables_for_template(self):
        return {'num_q': 1}


class FeedbackOne(Page):

    template_name = 'matching_pennies/Feedback.html'

    def participate_condition(self):
        return self.subsession.round_number == 1

    def variables_for_template(self):
        return {'num_q': 1,
                'question': 'Suppose Player 1 picked "Heads" and Player 2 guessed "Tails". Which of the following will be the result of that round?',
                'answer': self.player.training_question_1,
                'correct': self.subsession.training_1_correct,
                'explanation': 'Player 1 gets 100 points, Player 2 gets 0 points',
                'is_correct': self.player.is_training_question_1_correct(),
                }


class Choice(Page):

    template_name = 'matching_pennies/Choice.html'

    form_model = models.Player
    form_fields = ['penny_side']


class ResultsWaitPage(WaitPage):

    group = models.Match

    def after_all_players_arrive(self):
        self.match.set_points()
        if self.subsession.round_number == self.subsession.number_of_rounds:
            self.match.set_payoffs()

    def body_text(self):
        return "We need to wait for your opponent."


class Results(Page):

    template_name = 'matching_pennies/Results.html'

    def variables_for_template(self):

        return {'my_choice': self.player.penny_side,
                'other_choice': self.player.other_player().penny_side,
                'my_points': self.player.points_earned,
                'other_points': self.player.other_player().points_earned,
                'my_payoff': self.player.payoff,
                'other_payoff': self.player.other_player().payoff,
                'me_in_previous_rounds': self.player.me_in_previous_rounds()}


class ResultsSummary(Page):

    template_name = 'matching_pennies/ResultsSummary.html'

    def participate_condition(self):
        return self.subsession.round_number == self.subsession.number_of_rounds

    def variables_for_template(self):

        return {'me_in_previous_rounds': self.player.me_in_previous_rounds(),
                'points_earned': self.player.points_earned,
                'is_winner': self.player.is_winner,
                'total_points_earned': sum(p.points_earned for p in self.player.me_in_previous_rounds() + [self.player]),
                'payoff': self.player.payoff}


def pages():

    return [Introduction,
            QuestionOne,
            FeedbackOne,
            Choice,
            ResultsWaitPage,
            Results,
            ResultsSummary]
