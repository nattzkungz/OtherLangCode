% Define the numerator and denominator of the transfer function
numerator = 2;
denominator = [1 8 12 0];  % Coefficients of s^3, s^2, s, and constant

% Create the transfer function system
sys = tf(numerator, denominator);

% Plot the step response
figure;
step(sys);
title('Step Response of the Spring-Mass-Damper System');

% Get step response characteristics
step_info = stepinfo(sys);

% Display the step information
disp('Step Response Information:');
disp(step_info);
