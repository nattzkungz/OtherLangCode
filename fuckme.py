# from scipy.optimize import fsolve
# import numpy as np
# import math

# # Define the function representing the right side of the equation
# def equation_to_solve(x):
#     return (1/324000) * (math.atan(x/90000) + math.atan(x/30000) - math.atan(1173/90000) - math.atan(1173/30000)) + (2.0484 * 10**-5) / 107583

# # Use fsolve to find the root (value of x)
# initial_guess = 600  # You can adjust the initial guess
# result = fsolve(equation_to_solve, initial_guess)

# print("Approximate value of x:", result[0])


from scipy.integrate import quad

# Define the integrand
integrand = lambda x: 1 / (x**4 - 81 * 10**8)

# Set the integration bounds
lower_limit = 1173
upper_limit = -1.904 * 10**-10

# Use the quad function to approximate the definite integral
result, error = quad(integrand, lower_limit, upper_limit)

print("Approximate value of the integral:", result)
