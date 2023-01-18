from otree.api import *

class Calcu:

    def newsvendor(P, S, Q, D, C, BB, W):
        Rest = Q-D
        if Rest >= 0:
            Revenue = D*P + Rest*(S+BB)
            Buyback = (BB) * Rest
        else:
            Revenue = Q*P
            Buyback = 0
        Profit = Revenue - Q * W
        Profits = Q*(W-C)-Buyback

        results = {
            "PF": Profit,
            "PFS": Profits

        }
        return results

class C(BaseConstants):
    NAME_IN_URL = 'BuybackNewsvendor'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 6
    INSTRUCTIONS_TEMPLATE = 'BuybackNewsvendor/instructions.html'
    # Initial amount allocated to each player
    DEMAND = [148, 184, 83, 137, 215, 173, 97]
    MEAN = 140
    STANDARDDIV = 40
    PROFIT = 20
    SALVAGE = 2
    WHOLESALE = 10
    COST = 5
    OPTIMALSOLUTION = [10, 112, 239, 89]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    buyback_reduction = models.FloatField(initial=0,
         label="Please input the buyback price")
    quantity = models.IntegerField(initial=0, label="Please input how many units you want to order")
    buyback = models.FloatField(initial=0)



class Player(BasePlayer):

    buysell = models.StringField()
    profit = models.IntegerField()
# FUNCTIONS



def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    total_costs = Calcu.newsvendor(P=C.PROFIT, S=C.SALVAGE, Q=group.quantity, D=C.DEMAND[group.round_number], C=C.COST, BB=group.buyback_reduction, W=C.WHOLESALE)
    ProfitB = total_costs['PF']
    ProfitS = total_costs['PFS']
    p1.profit = int(ProfitS)
    p2.profit = int(ProfitB)


# PAGES
class instructions(Page):
    pass

class Introduction(Page):
    def vars_for_template(player: Player):
        if player.id_in_group == 1:

            player.buysell = "Supplier"

        else:

            player.buysell = "Buyer"


class Send(Page):
    """This page is only for P1
    P1 sends amount (all, some, or none) to P2
    This amount is tripled by experimenter,
    i.e if sent amount by P1 is 5, amount received by P2 is 15"""

    form_model = 'group'
    form_fields = ['buyback_reduction']
    def error_message(group:Group, values):
        if values['buyback_reduction'] < 0:
            return 'The number must be higher than 0, otherwise the buyer will not accept the offer.'
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class SendBackWaitPage(WaitPage):
    pass


class SendBack(Page):
    """This page is only for P2
    P2 sends back some amount (of the tripled amount received) to P1"""

    form_model = 'group'
    form_fields = ['quantity']
    def error_message(player:Player, values):
        if values['quantity'] < 1:
            return 'The number must be higher than 0.'
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


        total_costs = Calcu.newsvendor(P=C.PROFIT, S=C.SALVAGE, Q=group.quantity, D=C.DEMAND[group.round_number],
                                       C=C.COST, BB=group.buyback_reduction, W=C.WHOLESALE)
        ProfitB = total_costs['PF']
        ProfitS = total_costs['PFS']
        DEMAND = C.DEMAND[group.round_number]

        return dict(
                    PF=int(ProfitB),
                    PFS=int(ProfitS),
                    Dem=DEMAND,
                    PFSC=int(ProfitB)+int(ProfitS)
                    )

class Thanks(Page):
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

page_sequence = [
    Introduction,
    Send,
    SendBackWaitPage,
    SendBack,
    ResultsWaitPage,
    Results,
    Thanks
]
