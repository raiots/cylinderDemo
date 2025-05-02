clear all
close all
clc

% code to compare the CP curve from OpenFOAM (exported by Paraview) against
% xFOIL data 

file_CFD = '../Cp.csv'


%% load data
data_CFD = importdata(file_CFD)


x = data_CFD.data(:,2);
y = data_CFD.data(:,3);
pins = data_CFD.data(:,20);
pavg = data_CFD.data(:,21);
prms = sqrt(data_CFD.data(:,22));
yPlus = data_CFD.data(:,1);

cp_ins = pins./(0.5*26.8^2);
cp_avg = pavg./(0.5*26.8^2);
cp_rms = prms./(0.5*26.8^2);

theta = atan2(y,x)*180/pi; 

%% plot the data against each other
figure
subplot(1,4,1)
plot(x,y,'.')
title('Wall Surface','Interpreter','Latex')
xlabel('x [m]','Interpreter','Latex')
ylabel('y [m]','Interpreter','Latex')
legend('OpenFOAM')
axis equal
axis([-0.2 0.2 -0.2 0.2])
grid on

subplot(1,4,2)
plot(theta,cp_ins,'.')
hold on
plot(theta,cp_avg,'x')
hold off
title('Pressure Coefficient Distribution','Interpreter','Latex')
xlabel('$\theta$ [deg]','Interpreter','Latex')
ylabel('$C_p$','Interpreter','Latex')
legend('Instantaneous','Time Avg')
grid on
axis([-180 180 -3 3])


subplot(1,4,3)
plot(theta,cp_rms,'x')
title('Pressure Coefficient Distribution','Interpreter','Latex')
xlabel('$\theta$ [deg]','Interpreter','Latex')
ylabel('$C_p$','Interpreter','Latex')
legend('Instantaneous','Time Avg')
grid on
axis([-180 180 0 0.2])

subplot(1,4,4)
plot(theta,yPlus,'x')
title('Wall BL Resolution','Interpreter','Latex')
xlabel('$\theta$ [deg]','Interpreter','Latex')
ylabel('$y^+$','Interpreter','Latex')
legend('OpenFOAM')
grid on
axis([-180 180 -2 2])

