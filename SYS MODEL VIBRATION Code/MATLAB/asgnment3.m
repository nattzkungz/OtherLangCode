phi = 0.15;
R = 0:0.01:10;
Mag = R;

for i = 1:length(R)
    r = R(i); 
    Mag(i) = r^2 * sqrt((1 + (2 * phi * r)^2) / ((1-r^2)^2 + (2 * phi * r)^2));
end

semilogx(R, Mag, 'LineWidth', 2); grid on; hold on
xlabel('r = \\frac{\omega}{\omega_n}');
ylabel('Magnitude');
title('freq response');