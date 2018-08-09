import random
import numpy as np

def self_AdvectionRK4(particle, fieldset, time, dt):
    """Advection of particles using fourth-order Runge-Kutta integration.
    Overload function from parcels.kernels.advection module.
    Randomly deploy the particles that run out of boundary."""
    
    u_max = 2*np.amax(fieldset.U.data)*dt
    u_min = 2*np.amin(fieldset.U.data)*dt
    v_max = 2*np.amax(fieldset.V.data)*dt
    v_min = 2*np.amin(fieldset.V.data)*dt
    if particle.lon > 1.0 or 1.0-particle.lon < u_max or particle.lon < np.abs(u_min) or particle.lon < 0.0:
        particle.lon = random.uniform(np.abs(u_min),1.0-u_max)
    if particle.lat > 1.0 or 1.0-particle.lat < v_max or particle.lat < np.abs(v_min) or particle.lat < 0.0:
        particle.lat = random.uniform(np.abs(v_min),1.0-v_max)
    (u1, v1) = fieldset.UV[time, particle.lon, particle.lat, particle.depth]
    lon1, lat1 = (particle.lon + u1*.5*dt, particle.lat + v1*.5*dt)
    (u2, v2) = fieldset.UV[time + .5 * dt, lon1, lat1, particle.depth]
    lon2, lat2 = (particle.lon + u2*.5*dt, particle.lat + v2*.5*dt)
    (u3, v3) = fieldset.UV[time + .5 * dt, lon2, lat2, particle.depth]
    lon3, lat3 = (particle.lon + u3*dt, particle.lat + v3*dt)
    (u4, v4) = fieldset.UV[time + dt, lon3, lat3, particle.depth]
    particle.lon += (u1 + 2*u2 + 2*u3 + u4) / 6. * dt
    particle.lat += (v1 + 2*v2 + 2*v3 + v4) / 6. * dt
