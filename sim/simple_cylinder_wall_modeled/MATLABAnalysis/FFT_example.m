clear all
close all
clc

%% FFT Example with controlled signal as input 
Fs = 20000;            % Sampling frequency                    
T = 1/Fs;             % Sampling period       
L = 10*Fs;             % Length of signal
t = (0:L-1)*T;        % Time vector

S = 1*sin(2*pi*50*t) + 0.5*sin(2*pi*120*t) + rand(1,L);

figure(1)
plot(t(1:200),S(1:200))
title('Test Signal')
xlabel('t (s)')
ylabel('X(t)')

Y = fft(S);
P2 = abs(Y/L).^2;
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

f = Fs*(0:(L/2))/L;

figure(2)
semilogx(f,P1,'Color',[1,0,0,0.5])
title('Single-Sided Amplitude Spectrum of S(t)')
xlabel('f (Hz)')
ylabel('Energy [Variance]')