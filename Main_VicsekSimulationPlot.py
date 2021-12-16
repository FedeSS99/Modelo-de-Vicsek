import numpy as np
from numpy.random import uniform, rand
from matplotlib.pyplot import figure, show
from matplotlib.gridspec import GridSpec

n_particles = 500 #Number of particles
l =  20.0 #Dimensions of the box
r = 2.5 #neighbourhood radius
dt = 0.1 #time interval
t = 0.0 #time
time_steps = 500 #Number of time steps
v0 = 0.5 #Velocity magnitude
number_noises = 16 #Number of noise samples

x, y = uniform(0.0, l, (n_particles, 1)), uniform(0.0, l, (n_particles, 1))
theta = uniform(-np.pi, np.pi, (n_particles, 1))
vx, vy = v0*np.cos(theta), v0*np.sin(theta)

noise = np.linspace(0.0, 5.0, number_noises, dtype=np.float64, endpoint=True)
average_velocities = np.zeros(number_noises, dtype=np.float64)

#Creating the main figure within its subplots
main_figure = figure(1, (8, 6))
gs = GridSpec(3, 3, main_figure)

subplot1, subplot2 = main_figure.add_subplot(gs[:-1,:]), main_figure.add_subplot(gs[2,:])

subplot1.set_xlabel("X")
subplot1.set_ylabel("Y")
subplot1.set_aspect("equal", "box")
subplot1.set_xlim(0.0, l)
subplot1.set_ylim(0.0, l)
subplot1.get_xaxis().set_visible(False)
subplot1.get_yaxis().set_visible(False)

subplot2.set_xlabel(r"Noise $\eta$")
subplot2.set_ylabel(r"Average normalize velocity $v_{a}$")
subplot2.set_xlim(-0.1, max(noise)+0.1)
subplot2.set_ylim(0.0, 1.1)
subplot2.spines["top"].set_visible(False)
subplot2.spines["right"].set_visible(False)

#Declaring the plots for each subplot
particles, = subplot1.plot([], [], "ok", markersize=1.0)
noise_velocity_plot, = subplot2.plot([], [], "--ob", markersize=3)

show(block=False)

#Function with the algoritm proposed by Vicsek (1995)
def Update_Flocking(noise_val, x_pos, y_pos, vx_particle, vy_particle, theta_particle):
   global dt, l, n_particles

   x_pos += vx_particle*dt
   y_pos += vy_particle*dt

   x_pos = x_pos % l
   y_pos = y_pos % l

   mean_angle = np.copy(theta_particle)
     
   for j in range(n_particles):
      near_particles = (x_pos-x_pos[j])**2.0 + (y_pos-y_pos[j])**2.0 < r**2.0
      sum_cos = np.sum(np.cos( theta_particle[near_particles] ))/near_particles.size
      sum_sin = np.sum(np.sin( theta_particle[near_particles] ))/near_particles.size

      mean_angle[j] = np.arctan2(sum_sin, sum_cos)
        
   theta_particle = mean_angle + noise_val*(rand(n_particles,1)-0.5)

   vx_particle = v0*np.cos(theta_particle)
   vy_particle = v0*np.sin(theta_particle)

   return x_pos, y_pos, vx_particle, vy_particle, theta_particle

#Start using every noise value in the array "noise" to simulate the system with this
#different setting
for k in range(noise.size):
   string_constant_data = r"N={0}, $\eta$={1:.2f}, $v_{{0}}$={2:.2f}, dt={3:.2f}".format(n_particles, noise[k], v0, dt)
   title = main_figure.suptitle(string_constant_data+f"\nt={t:.2f}")

   t = 0.0
   
   for time_step in range(time_steps):
      t += dt
      x, y, vx, vy, theta = Update_Flocking(noise[k], x, y, vx, vy, theta)
      average_velocities[k] = np.sqrt( np.sum(vx)**2.0 + np.sum(vy)**2.0 )/(n_particles*v0)
      
      particles.set_data(x,y)
      noise_velocity_plot.set_data(noise[:(k+1)], average_velocities[:(k+1)])
      title.set_text(string_constant_data+f"\nt={t:.2f}")

      main_figure.canvas.draw()
      main_figure.canvas.flush_events()
