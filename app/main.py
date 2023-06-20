from cellular_autmata.simulation import CellularAutomata

if __name__ == '__main__':
    sim = CellularAutomata(200, 200, (100, 100), 10000)
    sim.run_simulation(2000)
