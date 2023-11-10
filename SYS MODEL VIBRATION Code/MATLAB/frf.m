Zeta = 1;
R = 0:0.01:10;
Mag = R;

for i=1:length(R)
    r = R(i);
    Mag(i) = (0.2/1.9843)*exp(-0.125*2*r)*sin(1.9843*r)+(0.1/1.9843)*exp(-0.125*2*r)*sin(1.9843*r);
end

subplot(2,1,1); semilogx(R,Mag); grid on; hold on
legend('Zeta=0.125');
ylabel('Magnitude (dB)'); xlabel('Frequency (rad/s)');
title('Frequency Response of a Second Order System');