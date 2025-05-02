function [freq,var] = FFT_func(S,Fs)
% Single-sided Energy Spectrum 
% input S - signal (1-D array)
% FS - frequency sample

L = length(S);        % Length of signal

S2 = S - mean(S);     % remove offset 
S = S2;

Y = fft(S);
P2 = abs(Y/L).^2;
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);

freq = Fs*(0:(L/2))/L;
var = P1;
