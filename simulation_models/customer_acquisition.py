
#      _                   _ _
#  _____| |__ ___ _ __  _ __(_| |___ _ _
# (_-/ _` / _/ _ | '  \| '_ | | / -_| '_|
# /__\__,_\__\___|_|_|_| .__|_|_\___|_|
#                      |_|
# Copyright (c) 2013-2016 transentis management & consulting. All rights reserved.
#
try:
    from sdmodel import LERP, SDModel
except:
    from BPTK_Py.sdcompiler.sdmodel import LERP, SDModel
    
import numpy as np
from scipy.interpolate import interp1d
from scipy.special import gammaln
import math, statistics
import random, logging


def random_with_seed(seed):
    random.seed(seed)
    return random.random()

def beta_with_seed(a,b,seed):
    np.random.seed(seed)
    return np.random.beta(a,b)
    
def binomial_with_seed(n,p,seed):
    np.random.seed(seed)
    return np.random.binomial(n,p)
    
def gamma_with_seed(shape,scale,seed):
    np.random.seed(seed)
    return np.random.gamma(shape,scale)
    
def exprnd_with_seed(plambda,seed):
    np.random.seed(seed)
    return np.random.exponential(plambda)
    
def geometric_with_seed(p,seed):
    np.random.seed(seed)
    return np.random.geometric(p)
    


class simulation_model(SDModel):
    import logging
    def rank(self, lis, rank):
        rank = int(rank)
        sorted_list = sorted(lis)
        try:
            rankth_elem = sorted_list[rank-1]
        except IndexError as e:
            logging.error("RANK: Rank {} too high for array of size {}".format(rank,len(lis)))
        return lis.index(rankth_elem)+1
        
    def __init__(self):
        # Simulation Buildins
        self.dt = 1.0
        self.starttime = 0
        self.stoptime = 60
        self.units = 'Months'
        self.method = 'Euler'
        self.equations = {

        # Stocks
        
    
        'advertisingCustomers'          : lambda t: ( (0.0) if ( t  <=  self.starttime ) else (self.memoize('advertisingCustomers',t-self.dt) + self.dt * ( self.memoize('advCustIn',t-self.dt) )) ),
        'customers'          : lambda t: ( (self.memoize('initialCustomers', t)) if ( t  <=  self.starttime ) else (self.memoize('customers',t-self.dt) + self.dt * ( self.memoize('customerAcquisition',t-self.dt) )) ),
        'profit'          : lambda t: ( ( - self.memoize('initialInvestmentInService', t)) if ( t  <=  self.starttime ) else (self.memoize('profit',t-self.dt) + self.dt * ( self.memoize('earnings',t-self.dt) - ( self.memoize('spending',t-self.dt) ) )) ),
        'referralCustomers'          : lambda t: ( (0.0) if ( t  <=  self.starttime ) else (self.memoize('referralCustomers',t-self.dt) + self.dt * ( self.memoize('referralCustIn',t-self.dt) )) ),
        
    
        # Flows
        'advCustIn'             : lambda t: max([0 , self.memoize('acquisitionThroughAdvertising', t)]),
        'customerAcquisition'             : lambda t: max([0 , self.memoize('acquisitionThroughAdvertising', t) + self.memoize('acquisitionThroughReferrals', t)]),
        'earnings'             : lambda t: max([0 , self.memoize('serviceMargin', t) * self.memoize('serviceFee', t) * self.memoize('customers', t)]),
        'referralCustIn'             : lambda t: max([0 , self.memoize('acquisitionThroughReferrals', t)]),
        'spending'             : lambda t: max([0 , ( (self.memoize('acquisitionThroughReferrals', t) * ( self.memoize('referralFreeMonths', t) * self.memoize('serviceFee', t) / self.memoize('referrals', t) ) + self.memoize('referralAdvertisingCost', t) + self.memoize('classicalAdvertisingCost', t)) if (self.memoize('referrals', t) > 0.0) else (self.memoize('classicalAdvertisingCost', t)) )]),
        
    
        # converters
        'acquisitionThroughAdvertising'      : lambda t: self.memoize('potentialCustomersReachedThroughAdvertising', t) * self.memoize('advertisingSuccessPct', t) / 100.0,
        'acquisitionThroughReferrals'      : lambda t: self.memoize('referrals', t) * self.memoize('customers', t) * ( 1.0 - self.memoize('marketSaturationPct', t) / 100.0 ) * self.memoize('referralProgramAdoptionPct', t) / 100.0,
        'advertisingSuccessPct'      : lambda t: 0.1,
        'classicalAdvertisingCost'      : lambda t: 10000.0,
        'initialCustomers'      : lambda t: 0.0,
        'initialInvestmentInService'      : lambda t: 1000000.0,
        'marketSaturationPct'      : lambda t: 100.0 * self.memoize('customers', t) / self.memoize('targetMarket', t),
        'personsReachedPerEuro'      : lambda t: 100.0,
        'potentialCustomersReachedThroughAdvertising'      : lambda t: self.memoize('personsReachedPerEuro', t) * self.memoize('classicalAdvertisingCost', t) * self.memoize('targetCustomerDilutionPct', t) / 100.0 * ( 1.0 - self.memoize('marketSaturationPct', t) / 100.0 ),
        'referralAdvertisingCost'      : lambda t: 10000.0,
        'referralFreeMonths'      : lambda t: 3.0,
        'referralProgramAdoptionPct'      : lambda t: 30.0,
        'referrals'      : lambda t: 0.0,
        'serviceFee'      : lambda t: 10.0,
        'serviceMargin'      : lambda t: 0.5,
        'targetCustomerDilutionPct'      : lambda t: 80.0,
        'targetMarket'      : lambda t: 6000000.0,
        
    
        # gf
        
    
        #constants
        
    
    
        }
    
        self.points = {
            
        }
    
    
        self.dimensions = {
        	'': {
                'labels': [  ],
                'variables': [  ],
            },
        }
                
        self.dimensions_order = {}     
    
        self.stocks = ['advertisingCustomers',   'customers',   'profit',   'referralCustomers'  ]
        self.flows = ['advCustIn',   'customerAcquisition',   'earnings',   'referralCustIn',   'spending'  ]
        self.converters = ['acquisitionThroughAdvertising',   'acquisitionThroughReferrals',   'advertisingSuccessPct',   'classicalAdvertisingCost',   'initialCustomers',   'initialInvestmentInService',   'marketSaturationPct',   'personsReachedPerEuro',   'potentialCustomersReachedThroughAdvertising',   'referralAdvertisingCost',   'referralFreeMonths',   'referralProgramAdoptionPct',   'referrals',   'serviceFee',   'serviceMargin',   'targetCustomerDilutionPct',   'targetMarket'  ]
        self.gf = []
        self.constants= []
        self.events = [
            ]
    
        self.memo = {}
        for key in list(self.equations.keys()):
          self.memo[key] = {}  # DICT OF DICTS!
    
    def specs(self):
        return self.starttime, self.stoptime, self.dt, 'Months', 'Euler'
    