clear all
close all
clc

% code to load and plot some wake profiles behind cylinder from paraview
% data

file_CFD = '../paraView/x0p3_y0p3.txt'
% this file is x=0.3m, and -0.3 < y < 0.3

%% load data
data_CFD = importdata(file_CFD)

x = data_CFD.data(:,25);
y = data_CFD.data(:,26);
U_avg = data_CFD.data(:,4:6)./26.8;
U_rms = data_CFD.data(:,7:12).^(0.5)/26.8; %3x diagonal and 3x off-diagonal 

for i=1:length(U_avg);
    U_mag(i) = sqrt(dot(U_avg(i,1:3),U_avg(i,1:3)));
end

%% plot the data 
figure
subplot(1,3,1)
plot(x,y,'.')
title('Data location','Interpreter','Latex')
xlabel('x [m]','Interpreter','Latex')
ylabel('y [m]','Interpreter','Latex')
legend('OpenFOAM')
axis equal
grid on

subplot(1,3,2)
plot(U_rms(:,1),y,'-r')
hold on
plot(U_rms(:,2),y,'-b')
plot(U_rms(:,3),y,'-k')
hold off
title('Resolved Turbulent intensity','Interpreter','Latex')
xlabel('$I$','Interpreter','Latex')
ylabel('$y$ [m]','Interpreter','Latex')
legend('$I_{xx}$','$I_{yy}$','$I_{zz}$')
grid on

subplot(1,3,3)
plot(U_avg(:,1),y,'-r')
hold on
plot(U_avg(:,2),y,'-b')
plot(U_avg(:,3),y,'-k')
plot(U_mag,y,'-g')
hold off
title('Avg. Velocity','Interpreter','Latex')
xlabel('$\overline{U}$','Interpreter','Latex')
ylabel('$y$ [m]','Interpreter','Latex')
legend('$u$','$v$','$w$','$|U|$')
grid on


