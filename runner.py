
def run(simulation:inventory_simulation,until:float):
  simulation.env.process(simulation.runner_setup())
  simulation.env.process(simulation.observe())

  simulation.env.run(until=until)

  

def eoq_sim_search(reorder_lvl_proposals:float,reorder_qty_proposals:np.array,purchase_cost:float,selling_price:float,run_time:int,target_service_level:float) -> float:
  service_levels = []
  costs = []

  eoq = []
  
  for q in reorder_qty_proposals:
      s = inventory_simulation(simpy.Environment(),reorder_lvl_proposals,q,purchase_cost,selling_price)
      run(s,run_time)
      service_levels.append(s.service_level())
      costs.append(s.avg_cost_of_inventory())
      
      eoq.append(q)
  service_levels = np.array(service_levels)
  costs = np.array(costs)
  eoq = np.array(eoq)
  if (len(service_levels)<1) or (len(costs)<1) or (len(eoq)<1) or len(np.where(service_levels>=target_service_level)) < 1:
    return False
  else:
    
    plt.plot(reorder_qty_proposals,service_levels)
    return eoq[np.where(costs==np.min(costs[service_levels>=target_service_level]))][0]
    plt.show()
  