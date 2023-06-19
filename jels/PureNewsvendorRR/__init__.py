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
    NAME_IN_URL = 'PureNewsvendorRR'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 6
    INSTRUCTIONS_TEMPLATE = 'PureNewsvendorRR/instructions.html'
    # Initial amount allocated to each player
    ENDOWMENT = cu(100)
    MULTIPLIER = 3

    DEMAND = [34, 32, 29, 23, 25, 17, 28, 14]
    MEAN = 22
    STANDARDDIV = 6
    PROFIT = 1.95
    SALVAGE = 0.1
    COST = 0.8
    OPTIMALSOLUTION = [24]

class Subsession(BaseSubsession):
    pass


class Player(BasePlayer):

    quantity = models.IntegerField(initial=0, label="Please input how many units you want to order")
    ordering_cost = models.IntegerField()
    buysell = models.StringField()
    profit = models.FloatField()
    fprofit = models.FloatField()

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
    pass

class order(Page):

    form_model = 'player'
    form_fields = ['quantity']

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