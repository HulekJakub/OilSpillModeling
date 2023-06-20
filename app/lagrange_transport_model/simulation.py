import numpy as np
import cv2
OCEAN_BLUE = np.array([0, 157, 196], np.uint8)

def lagrangian_transport_model(initial_positions, fluid_velocity_field, turbulent_diffusivity, time_step, num_steps):
    num_particles = len(initial_positions)
    particle_positions = np.zeros((num_steps+1, num_particles, 2))
    particle_positions[0] = initial_positions
    base_image = np.zeros((200, 200, 3), np.uint8)
    base_image[:, :, :] = OCEAN_BLUE


    for step in range(num_steps):
        I = base_image.copy()
        I = cv2.cvtColor(I, cv2.COLOR_RGB2BGRA)
        for point in particle_positions[step]:
            cv2.circle(I, (int(point[1]) + 100, int(point[0]) + 100), 1, (0, 0, 0, 50))
        cv2.putText(I, str(step), (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255, 255), 2)
        I = cv2.resize(I, (600, 600), interpolation = cv2.INTER_NEAREST)

        cv2.imshow('Lagrange', I)

        if cv2.waitKey(50) & 0xFF == ord('q'): # break the loop when the ’q’ key is pressed
            break 

        for i in range(num_particles):
            current_position = particle_positions[step, i]
            
            # Get fluid velocity at current position
            velocity = fluid_velocity_field(*current_position)
            
            # Calculate deterministic displacement due to advection
            advection_displacement = velocity * time_step
            
            # Calculate stochastic displacement due to turbulence
            turbulence_displacement = np.sqrt(2 * turbulent_diffusivity * time_step) * np.random.randn(2)
            
            # Update particle position with advection and turbulence displacements
            new_position = current_position + advection_displacement + turbulence_displacement
            particle_positions[step+1, i] = new_position


    
    return particle_positions

# Example usage
def fluid_velocity_field(x, y):
    # Define your fluid velocity field here
    # This is just a simple example
    u = 0.5 * y
    v = -0.5 * x
    return np.array([u, v])

initial_positions = np.array([[0.0, 0.0] for _ in range(100)])  # Example initial positions of particles
turbulent_diffusivity = 0.5  # Turbulent diffusivity coefficient
time_step = 0.1  # Time step size
num_steps = 1000  # Number of time steps

particle_positions = lagrangian_transport_model(initial_positions, fluid_velocity_field, turbulent_diffusivity, time_step, num_steps)

# Print the final positions of particles
print("Final positions:")
for i, positions in enumerate(particle_positions[-1]):
    print(f"Particle {i+1}: ({positions[0]}, {positions[1]})")