filename =  '/Users/thanakrittr/Downloads/vibrPrj.xlsx';

K = 1;
T = 0.1;

Data = xlsread(filename,'XL 2','G15:I30');
t = Data(:,1);

Step = Data(1,3);

Ref = [1:length(Data(:,1))];
for i=1:length(Ref)
    Ref(i) = Step;
end

Pos = Ref;
for i=1:length(Ref)
    Pos(i) = Step - Data(i,3);
end
plot(t,Pos)
title('Experiment (kd = 0.01, kp = 2)')
ylabel('Amplitude')
xlabel('Time (s) [Starts from G15]')

data = iddata(Pos',Ref',T);

sys = tfest(data,2,0)

J = K/sys.Denominator(3)
C = sys.Denominator(2)*J

figure, step(sys)