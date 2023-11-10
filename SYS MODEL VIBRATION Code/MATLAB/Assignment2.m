% RUN THIS CODE IN COMMAND WINDOWS
% Underdamped case
m = 150;
k = 15000;
c = 1000;
Wn = sqrt(k/m);
Zeta = c/(2*sqrt(k*m));
Wd = Wn*sqrt(1-Zeta^2);
x0 = -0.02;
v0 = 0;
ASinPhi = x0;
ACosPhi = (v0 + Zeta*Wn*x0)/Wd;
Phi = atan(ASinPhi/ACosPhi);
A = x0/sin(Phi);
t1 = 0:0.01:6;
X = t1;
for i=1:length(t1)
    X(i) = A*exp(-Zeta*Wn*t1(i))*sin(Wd*t1(i) + Phi);
end
plot(t1,X,'b'); grid on
legend('ODE45', 'Closed Form Solution')

% Critically damped case
m = 150;
k = 15000;
c = 3000;
Wn = sqrt(k/m);
A1 = -0.02;
A2 = -0.2
x0 = -0.02;
v0 = 0;
t1 = 0:0.01:6;
X = t1;
for i=1:length(t1)
    X(i) = (A1+(A2*t1(i)))*exp(-Wn*t1(i));
end
plot(t1,X,'b'); grid on
legend('ODE45', 'Closed Form Solution')

% Overdamped case
m = 150;
k = 15000;
c = 7000;
Wn = sqrt(k/m);
A1 = -0.03;
A2 = 0.01
x0 = -0.02;
v0 = 0;
t1 = 0:0.01:6;
Zeta = c/(2*sqrt(k*m));
X = t1;
for i=1:length(t1)
    X(i) = (exp(-Zeta*Wn*t1(i)))*(A1*exp(Wn*sqrt(Zeta^2-1)*t1(i))+A2*exp(-Wn*sqrt(Zeta^2-1)*t1(i)));
end
plot(t1,X,'b'); grid on
legend('ODE45', 'Closed Form Solution')