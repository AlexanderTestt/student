from otree.api import *

class Calcu:

    def eoq(s, ss, Q, H, D, C):
        total_cost = s * (D / Q) + H * (Q / 2) -C*D
        Avg_Inv = Q / 2
        Avg_Reorder = Q / D
        total_cost_supplier = ss*(D/Q)+C*D
        total_supply_chain_cost = total_cost_supplier+total_cost
        results = {
            "TC": total_cost,
            "AI": Avg_Inv,
            "AR": Avg_Reorder,
            "TCS": total_cost_supplier,
            "TCSC": total_supply_chain_cost
        }
        return results

class C(BaseConstants):
    NAME_IN_URL = 'PureEOQ'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3
    INSTRUCTIONS_TEMPLATE = 'PureEOQ/instructions.html'
    # Initial amount allocated to each player
    ENDOWMENT = cu(100)
    MULTIPLIER = 3
    REORDERCOSTB = [200, 220, 380, 160]
    REORDERCOSTS =[300, 300, 300, 300]
    HOLDINGCOST = [5, 7, 1, 2]
    DEMAND = [100, 200, 150, 100]
    PROFIT = 10
    OPTIMALSOLUTION = [10, 112, 338, 127]

class Subsession(BaseSubsession):
    pass


class Player(BasePlayer):

    quantity = models.IntegerField(initial=0, label="Please input how many units you want to order")
    ordering_cost = models.IntegerField()
    buysell = models.StringField()
    profit = models.IntegerField()
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
    def vars_for_template(player: Player):
        DEMAND = C.DEMAND[player.round_number]
        holding = C.HOLDINGCOST[player.round_number]
        return dict(Dem=DEMAND,
                    holding=holding,)


class Introduction(Page):
    def vars_for_template(player: Player):
        player.ordering_cost = C.REORDERCOSTB[player.round_number]
        player.buysell = "Buyer"
        DEMAND = C.DEMAND[player.round_number]
        holding = C.HOLDINGCOST[player.round_number]
        return dict(Dem=DEMAND,
                    holding=holding,)

class order(Page):

    form_model = 'player'
    form_fields = ['quantity']

    def vars_for_template(player: Player):
        DEMAND = C.DEMAND[player.round_number]
        holding = C.HOLDINGCOST[player.round_number]
        return dict(Dem=DEMAND,
                    holding=holding, )

class Results(Page):
    """This page displays the earnings of each player"""
    @staticmethod

    def vars_for_template(player: Player):
        total_costs = Calcu.eoq(s=C.REORDERCOSTB[player.round_number], ss=C.REORDERCOSTS[player.round_number], Q=player.quantity, H=C.HOLDINGCOST[player.round_number], D=C.DEMAND[player.round_number], C=0)
        tcb = int(total_costs['TC'])
        player.profit = C.PROFIT * C.DEMAND[player.round_number] - tcb
        DEMAND = C.DEMAND[player.round_number]
        holding = C.HOLDINGCOST[player.round_number]
        opti = C.OPTIMALSOLUTION[player.round_number]
        return dict(
                    TC=tcb,
                    Dem=DEMAND,
                    holding=holding,
                    optimal=opti,
                    )


page_sequence = [
    Introduction,
    order,
    Results,
]
