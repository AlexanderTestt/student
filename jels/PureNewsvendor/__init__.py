from otree.api import *

class Calcu:

    def newsvendor(P, S, Q, D, C):
        Rest = Q-D
        if Rest >= 0:
            Revenue = D*P + Rest*S
        else:
            Revenue = Q*P

        Profit = Revenue - Q * C


        results = {
            "PF": Profit,

        }
        return results

class C(BaseConstants):
    NAME_IN_URL = 'PureNewsvendor'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 6
    INSTRUCTIONS_TEMPLATE = 'PureNewsvendor/instructions.html'
    # Initial amount allocated to each player
    ENDOWMENT = cu(100)
    MULTIPLIER = 3

    DEMAND = [148, 184, 83, 137, 215, 173, 97]
    MEAN = 140
    STANDARDDIV = 40
    PROFIT = 20
    SALVAGE = 2
    COST = 5
    OPTIMALSOLUTION = [179]

class Subsession(BaseSubsession):
    pass


class Player(BasePlayer):

    quantity = models.IntegerField(initial=0, label="Please input how many units you want to order")
    ordering_cost = models.IntegerField()
    buysell = models.StringField()
    profit = models.IntegerField()
    fprofit = models.IntegerField()
# FUNCTIONS


class Group(BaseGroup):
    pass


#def set_payoffs(player:Player):

 #   total_costs = Calcu.eoq(s=C.REORDERCOSTB, ss=C.REORDERCOSTS, Q=player.quantity, H=C.HOLDINGCOST, D=C.DEMAND,
 #                           C=0)
  #  tcb = total_costs['TC']
 #   player.payoff = C.PROFIT*C.DEMAND - tcb

 #PAGES


class instructions(Page):
    pass


class Introduction(Page):
    def is_displayed(player: Player):
        return player.round_number == 1


class Thanks(Page):
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    def vars_for_template(player: Player):


        return dict(
            a=player.fprofit
        )


class order(Page):

    form_model = 'player'
    form_fields = ['quantity']



class Results(Page):
    """This page displays the earnings of each player"""
    @staticmethod

    def vars_for_template(player: Player):
        total_costs = Calcu.newsvendor(P=C.PROFIT, S=C.SALVAGE, Q=player.quantity, C=C.COST, D=C.DEMAND[player.round_number])
        Profit = int(total_costs['PF'])
        player.profit = Profit
        DEMAND = C.DEMAND[player.round_number]
        if player.round_number > 1:
            pay_player = player.in_round(player.round_number - 1)
            player.fprofit = pay_player.fprofit + player.profit
        else:
            player.fprofit = player.profit
        return dict(
                    TC=Profit,
                    Dem=DEMAND,

                    )


page_sequence = [
    Introduction,
    order,
    Results,
    Thanks
]
