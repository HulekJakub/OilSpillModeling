from parcels import FieldSet, ParticleSet, Variable, JITParticle, AdvectionRK4, plotTrajectoriesFile, download_example_dataset
import numpy as np
import math
from datetime import timedelta
from operator import attrgetter

class ParcelSimulation:

    def simulation(self):
        try:
            example_dataset_folder = download_example_dataset("MovingEddies_data")

            fieldset = FieldSet.from_parcels(f"{example_dataset_folder}/moving_eddies")
            fieldset.U.show()
            pset = ParticleSet.from_list(fieldset=fieldset,   # the fields on which the particles are advected
                                    pclass=JITParticle,  # the type of particles (JITParticle or ScipyParticle)
                                    lon=[3.3e5,  3.3e5], # a vector of release longitudes
                                    lat=[1e5, 2.8e5])    # a vector of release latitudes
            pset.show(field=fieldset.U)
            output_file = pset.ParticleFile(name="EddyParticles.zarr", outputdt=timedelta(hours=1)) # the file name and the time step of the outputs
            pset.execute(AdvectionRK4,                 # the kernel (which defines how particles move)
                        runtime=timedelta(days=6),    # the total length of the run
                        dt=timedelta(minutes=5),      # the timestep of the kernel
                        output_file=output_file)

            pset.show(field=fieldset.U)
            # plotTrajectoriesFile('EddyParticles.zarr')
            plotTrajectoriesFile('EddyParticles.zarr', mode='movie2d')
        except Exception as e:
            print(e)
            print(e.__traceback__)

        

if __name__ == '__main__':

    sim = ParcelSimulation()
    sim.simulation()