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
    NAME_IN_URL = 'EOQ'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 3
    INSTRUCTIONS_TEMPLATE = 'EOQ/instructions.html'
    # Initial amount allocated to each player
    ENDOWMENT = cu(100)
    MULTIPLIER = 3
    REORDERCOSTB = [200, 220, 380, 160]
    REORDERCOSTS =[300, 340, 200, 400]
    HOLDINGCOST = [5, 7, 1, 2]
    DEMAND = [100, 200, 150, 100]
    PROFIT = 10
    OPTIMALSOLUTION = [10, 179, 417, 237]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    min_quantity = models.IntegerField(initial=0,
                                    label="Please enter the minimum amount for the price reduction")
    price_reduction = models.FloatField(initial=0,
         label="Please input the price reduction if the buyer orders more than the quantity given above")
    quantity = models.IntegerField(initial=0, label="Please input how many units you want to order")
    reduction = models.FloatField(initial=0)



class Player(BasePlayer):
    ordering_cost = models.IntegerField()
    buysell = models.StringField()
    ordering_cost_oppose = models.IntegerField()
    profit = models.IntegerField()
# FUNCTIONS



def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    total_costs = Calcu.eoq(s=C.REORDERCOSTB[group.round_number], ss=C.REORDERCOSTS[group.round_number], Q=group.quantity, H=C.HOLDINGCOST[group.round_number], D=C.DEMAND[group.round_number],
                            C=group.reduction)
    tcb = total_costs['TC']
    tcs = total_costs['TCS']
    p1.profit = int(C.PROFIT*C.DEMAND[group.round_number] * 0.25 - tcs)
    p2.profit = int(C.PROFIT*C.DEMAND[group.round_number] * 0.75 - tcb)


# PAGES
class instructions(Page):
    def vars_for_template(player: Player):
        DEMAND = C.DEMAND[player.round_number]
        holding = C.HOLDINGCOST[player.round_number]
        return dict(Dem=DEMAND,
                    holding=holding, )

class Introduction(Page):
    def vars_for_template(player: Player):
        if player.id_in_group == 1:
            player.ordering_cost = C.REORDERCOSTS[player.round_number]
            player.buysell = "Supplier"
            player.ordering_cost_oppose = C.REORDERCOSTB[player.round_number]
        else:
            player.ordering_cost = C.REORDERCOSTB[player.round_number]
            player.buysell = "Buyer"
            player.ordering_cost_oppose = C.REORDERCOSTS[player.round_number]
        DEMAND = C.DEMAND[player.round_number]
        holding = C.HOLDINGCOST[player.round_number]
        return dict(Dem=DEMAND,
                    holding=holding,)

class Send(Page):
    """This page is only for P1
    P1 sends amount (all, some, or none) to P2
    This amount is tripled by experimenter,
    i.e if sent amount by P1 is 5, amount received by P2 is 15"""

    form_model = 'group'
    form_fields = ['min_quantity', 'price_reduction']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1
    def vars_for_template(player: Player):
        DEMAND = C.DEMAND[player.round_number]
        holding = C.HOLDINGCOST[player.round_number]
        return dict(Dem=DEMAND,
                    holding=holding, )

class SendBackWaitPage(WaitPage):
    pass


class SendBack(Page):
    """This page is only for P2
    P2 sends back some amount (of the tripled amount received) to P1"""

    form_model = 'group'
    form_fields = [ 'quantity']
    def error_message(group:Group, values):
        if values['quantity'] < 1:
            return 'The number must be higher than 0.'
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

    def vars_for_template(player: Player):
        DEMAND = C.DEMAND[player.round_number]
        holding = C.HOLDINGCOST[player.round_number]
        return dict(Dem=DEMAND,
                    holding=holding, )


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    """This page displays the earnings of each player"""

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        if group.quantity >= group.min_quantity:
            group.reduction = group.price_reduction
        else:
            group.reduction = 0


        total_costs = Calcu.eoq(s=C.REORDERCOSTB[group.round_number], ss=C.REORDERCOSTS[group.round_number], Q=group.quantity, H=C.HOLDINGCOST[group.round_number], D=C.DEMAND[group.round_number], C=group.reduction)
        tcb = total_costs['TC']
        tcs = total_costs['TCS']
        tcsc = total_costs['TCSC']
        DEMAND = C.DEMAND[group.round_number]
        holding = C.HOLDINGCOST[group.round_number]
        Opti = C.OPTIMALSOLUTION[group.round_number]
        return dict(
                    TC=int(tcb),
                    TCS=int(tcs),
                    TCSC=int(tcsc),
                    Dem=DEMAND,
                    holding=holding,
                    Optimal=Opti,)



page_sequence = [
    Introduction,
    Send,
    SendBackWaitPage,
    SendBack,
    ResultsWaitPage,
    Results,
]
