# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
# Created on Mon Jun 12 13:25:28 2017

# @author: nealcz @Aian_fund

# This program is personal trading platform desiged when employed in 
# Aihui Asset Management as a quantatitive analyst.
# 
# Contact: 
# Name: Chen Zhang (Neal)
# Mobile: (+86) 139-1706-0712
# E-mail: nealzc1991@gmail.com

###############################################################################

class Sector(object):
    
    def __init__(self):
        # Energy
        self.Coal_Pairs = ['J','JM']
        self.Coal_number = [1,2]
        # Metals
        self.Iron_Ore_Steel = ['I', 'RB']
        self.Iron_Ore_Steel_number = [1,2]
        self.Steel_Hot_Rolled = ['RB', 'HC']
        self.Steel_Hot_Rolled_number = [1,1]
        # Agriculture
        self.SoyBean_Meal = ['M']
        self.SoyBean_Oil = ['Y']
        self.Rapeseed_Oil = ['OI']
        # Financial Futures
        self.Index_Futures = ['IC', 'IF', 'IH']
        self.number = '0123456789'
    
    def pairs_trading(self, sector):
        '''
        Input:
            sector:
                1: Coal and Coking Coal
                2: Iron Ore and Steel
                3: Steel and Hot Rolled
        Output:
            return dict of underlying assets and normal pairs number
        '''
        
        pairs_Coal = dict(zip(self.Coal_Pairs, self.Coal_number))
        pairs_Metal = dict(zip(self.Iron_Ore_Steel, self.Iron_Ore_Steel_number))
        pairs_SteelRolled = dict(zip(self.Steel_Hot_Rolled, self.Steel_Hot_Rolled_number))
        
        if sector == 1:
            return pairs_Coal
        elif sector == 2:
            return pairs_Metal
        elif sector == 3:
            return pairs_SteelRolled