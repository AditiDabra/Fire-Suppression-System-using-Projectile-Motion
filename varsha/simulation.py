# simulation.py
import numpy as np
import math
from scipy.optimize import minimize

g = 9.8
h0 = 10
m = 1.5 
k = 2000

def simulate_projectile(x_input, y_input):
    z_target = 0
    x_target = abs(x_input)
    y_target = abs(y_input)

    def objective(params):
        v0, theta, phi = params
        theta_rad = np.radians(theta)
        phi_rad = np.radians(phi)
        a = -0.5 * g
        b = v0 * np.sin(theta_rad)
        c = h0 - z_target
        discriminant = b**2 - 4 * a * c  # z = h + sin0t -1/2gt^2
        if discriminant < 0:
            return 1e6
        t1 = (-b + np.sqrt(discriminant)) / (2 * a)
        t2 = (-b - np.sqrt(discriminant)) / (2 * a)
        t = max(t1, t2) if max(t1, t2) > 0 else 1e6 
        x = v0 * np.cos(theta_rad) * np.cos(phi_rad) * t
        y = abs(v0 * np.cos(theta_rad) * np.sin(phi_rad) * t)
        return (x - x_target)**2 + (y - y_target)**2

    result = minimize(objective, [10, 45, 45], bounds=[(0, 15), (-90, 0), (0, 360)])
    if not result.success:
        return None

    v0, theta, phi = result.x
    theta_rad = np.radians(theta)
    phi_rad = np.radians(phi)
    a = -0.5 * g
    b = v0 * np.sin(theta_rad)
    c = h0 - z_target
    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return None

    t1 = (-b + np.sqrt(discriminant)) / (2 * a)
    t2 = (-b - np.sqrt(discriminant)) / (2 * a)
    t_final = max(t1, t2)
    t_vals = np.linspace(0, t_final, 500)
    x_vals = v0 * np.cos(theta_rad) * np.cos(phi_rad) * t_vals
    y_vals = v0 * np.cos(theta_rad) * np.sin(phi_rad) * t_vals
    z_vals = h0 + v0 * np.sin(theta_rad) * t_vals - 0.5 * g * t_vals ** 2
    disp=math.sqrt((m*v0**2)/k)
    
    if x_input < 0: x_vals = -x_vals
    if y_input < 0: y_vals = -y_vals

    return {

        'x_vals': x_vals.tolist(),
        'y_vals': y_vals.tolist(),
        'z_vals': z_vals.tolist(),
        'target': [x_input, y_input],
        'x_input':x_input,
        'y_input':y_input,
        'v0': v0,
        'theta': theta,
        'phi': phi,
        't_final': t_final,
        'disp':disp
    }
