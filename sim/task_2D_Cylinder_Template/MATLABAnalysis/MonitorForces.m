clear all
close all
clc

%% Specify INPUTS 
file=["../postProcessing/forces/0/force.dat","../postProcessing/forces/0.1/force.dat"]

%force.dat file is a little more complex. Need to use some tricks to open
%it properly ...


%% Main Code 
ind = 0;
for li = 1:length(1)
    fid = fopen(char(file(1)));
    
for line=1:4                % first 4 lines are basic headlines
    line = fgetl(fid);      % do nothing with that data 
end

%ind = 0;
while ~feof(fid)                % read until End Of File (EOF)
    line = fgetl(fid);
    newStr = split(line,'(');   % split the line by '(' character
    
    ind = ind + 1;              % index update
    time(ind,1) = str2num(newStr{1});
    
    fStr = split(newStr{2},')');    % remove the ')' character
    ftot = split(fStr{1},' ');      % split into x,y,z components
    
    F_tot(ind,1) = str2num(ftot{1});
    F_tot(ind,2) = str2num(ftot{2});
    F_tot(ind,3) = str2num(ftot{3});    
end
fclose(fid)
end

%% Plot the Forces
set(groot, 'defaultAxesTickLabelInterpreter','latex'); set(groot, 'defaultLegendInterpreter','latex');
figure
s = 1;     % set to 1 to use all data, set to N to ignore first N points
e = 0;
subplot(2,1,1)
hold on
plot(time(s:end-e,1),F_tot(s:end-e,1),'-r')
xline([0.1],'k')
%xline([0.0660],'r')
hold off
title('$F_x$','Interpreter','latex')
xlabel('Iterations','Interpreter','latex')
ylabel('Force [N]','Interpreter','latex')
subplot(2,1,2)
hold on
plot(time(s:end-e,1),F_tot(s:end-e,2),'-g')
xline([0.1],'k')
%xline([0.0660],'r')
hold off
title('$F_y$','Interpreter','latex')
xlabel('Iterations','Interpreter','latex')
ylabel('Force [N]','Interpreter','latex')



%% Final results for UNSTEADY CASE
% simply take the latest results 
F = F_tot(s:end,1:3);
F_avg = mean(F)
F_rms = sqrt(var(F))
C_avg = F_avg./(0.5*1.225*5^2*0.15*0.075)
C_rms = F_rms./(0.5*1.225*5^2*0.15*0.075)


%% Frequency Analyis 
fprintf(' WARNING - TIME STEP MUST BE CONSTANT FOR FFT ANALYSIS!!! \n')
dt = time(2)-time(1);
index = 2;  %1=Fx, 2=Fy
[freq,var] = FFT_func(F(:,index),1/dt);

figure(2)
semilogx(freq,var,'Color',[1,0,0,0.9])
title('FFT Analysis of Forces')
ylabel('Variance [N]]')
xlabel('Frequency [Hz]')