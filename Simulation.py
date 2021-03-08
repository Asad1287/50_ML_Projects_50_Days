import numpy as np
import simpy
import matplotlib.pyplot as plt
np.random.seed(0)
from math import ceil
class inventory_simulation:

  def __init__(self,env:simpy.Environment,reorder_level:int,reorder_qty:int,purchase_cost:float,selling_price:float) -> None:
    self.reorder_level = reorder_level
    self.reorder_qty = reorder_qty
    self.balance = 0
    self.num_ordered = 0
    self.inventory = self.reorder_qty
    self.env = env
    self.obs_time = []
    self.inventory_level = []
    self.demand =0
    self.purchase_cost = purchase_cost
    self.selling_price = selling_price
    self.costslevel = []
  def handle_order(self) -> None:
  
    #print(f'at {round(self.env.now)} placed order for {self.num_ordered}')
    
   
    self.num_ordered = self.reorder_level + 1 -self.inventory
    self.num_ordered = ceil(self.num_ordered/self.reorder_qty)*self.reorder_qty

    self.balance -= self.purchase_cost*self.num_ordered
    yield self.env.timeout(2.0)
    self.inventory += self.num_ordered
    self.num_ordered = 0
    #print(f'at {round(self.env.now)} recieved order for {self.num_ordered}')
  
  def generate_interarrival(self) -> np.array:
    return np.random.exponential(1./5)

  def generate_demand(self) -> np.array:
    return np.random.randint(1,5)


  def observe(self):
    
    while True:
      self.obs_time.append(self.env.now)
      self.inventory_level.append(self.inventory)
      self.costslevel.append(self.balance)
      yield self.env.timeout(0.1) 

  def runner_setup(self):
    while True:
      interarrival = self.generate_interarrival()
      yield self.env.timeout(interarrival)
      self.balance -= self.inventory*2*interarrival
      self.demand = self.generate_demand()
      if self.demand < self.inventory:
        self.balance += self.selling_price*self.demand
        self.inventory -= self.demand
        #print(f'customer comes I sold {self.demand} at time {round(self.env.now,2)}')
      else:
        self.balance += self.selling_price*self.inventory
        self.inventory = 0 
        #print(f'{self.inventory} is out of stock at {round(self.env.now,2)}')
      if self.inventory < self.reorder_level and self.num_ordered ==0:
        self.env.process(self.handle_order())
  def plot_inventory(self):
    plt.figure()
    plt.step(self.obs_time,self.inventory_level)
    plt.xlabel('Time')
    plt.ylabel('SKU level')
  
  def plot_balance(self):
    plt.figure()
    plt.step(self.obs_time,self.costslevel)
    plt.xlabel('Time')
    plt.ylabel('SKU balance USD')

  def service_level(self):
    __temp_level= np.array(self.inventory_level)
    __temp_level1 = __temp_level[__temp_level==0]
    if len(__temp_level1)==0:
      return 1
    else:
      return (1 - len(__temp_level1)/len(__temp_level))

  def avg_cost_of_inventory(self):
    __temp_level = np.array(self.inventory_level)*self.purchase_cost
    return (__temp_level.mean())
