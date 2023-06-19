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
    NAME_IN_URL = 'Jels'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 3
    INSTRUCTIONS_TEMPLATE = 'Jels/instructions.html'
    # Initial amount allocated to each player
    ENDOWMENT = cu(100)
    MULTIPLIER = 3
    REORDERCOSTB = 200
    REORDERCOSTS =300
    HOLDINGCOST = 5
    DEMAND = 100
    PROFIT = 20


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    min_quantity = models.IntegerField(initial=0,
                                    label="Please enter the minimum amount for the price reduction")
    price_reduction = models.IntegerField(initial=0,
         label="Please input the price reduction if the buyer orders more than the quantity given above")
    quantity = models.IntegerField(initial=0, label="Please input how many units you want to order")
    reduction = models.IntegerField(initial=0)



class Player(BasePlayer):
    ordering_cost = models.IntegerField()
    buysell = models.StringField()


# FUNCTIONS



def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    total_costs = Calcu.eoq(s=C.REORDERCOSTB, ss=C.REORDERCOSTS, Q=group.quantity, H=C.HOLDINGCOST, D=C.DEMAND,
                            C=group.reduction)
    tcb = total_costs['TC']
    tcs = total_costs['TCS']
    p1.payoff = C.PROFIT*C.DEMAND * 0.25 - tcs
    p2.payoff = C.PROFIT*C.DEMAND * 0.75 - tcb


# PAGES
class instructions(Page):
    def vars_for_template(player: Player):
        DEMAND = C.DEMAND

class Introduction(Page):
    def vars_for_template(player: Player):
        if player.id_in_group == 1:
            player.ordering_cost = C.REORDERCOSTS
            player.buysell = "Supplier"
        else:
            player.ordering_cost = C.REORDERCOSTB
            player.buysell = "Buyer"

class Send(Page):
    """This page is only for P1
    P1 sends amount (all, some, or none) to P2
    This amount is tripled by experimenter,
    i.e if sent amount by P1 is 5, amount received by P2 is 15"""

    form_model = 'group'
    form_fields = [ 'min_quantity', 'price_reduction']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class SendBackWaitPage(WaitPage):
    pass


class SendBack(Page):
    """This page is only for P2
    P2 sends back some amount (of the tripled amount received) to P1"""

    form_model = 'group'
    form_fields = [ 'quantity']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group




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


        total_costs = Calcu.eoq(s=C.REORDERCOSTB, ss=C.REORDERCOSTS, Q=group.quantity, H=C.HOLDINGCOST, D=C.DEMAND, C=group.reduction)
        tcb = total_costs['TC']
        tcs = total_costs['TCS']
        tcsc = total_costs['TCSC']
        return dict(
                    TC=tcb,
                    TCS=tcs,
                    TCSC=tcsc)

page_sequence = [
    Introduction,
    Send,
    SendBackWaitPage,
    SendBack,
    ResultsWaitPage,
    Results,
]
