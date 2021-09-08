% A 2-machine 5-bus system from Stagg-El-Abiad
% datastag.m
% incluye upfc entre nodos 3 - 4 (nodo 6 es ficticio)

% bus data format
% bus: number, voltage(pu), angle(degree), p_gen(pu), q_gen(pu),
%      p_load(pu), q_load(pu), bus_type
%      bus_type - 1, swing bus
%               - 2, generator bus (PV bus)
%               - 3, load bus (PQ bus)

bus = [  1 1.06    0.00   0.00   0.00  0.00  0.00  0.00  0.00 1;
	     2 1.00    0.00   0.40   0.00  0.20  0.10  0.00  0.00 2;
	     3 1.00    0.00   0.00   0.00  0.45  0.15  0.00  0.00 3; %shunt del upfc
	     4 1.00    0.00   0.00   0.00  0.40  0.05  0.00  0.00 3;
	     5 1.00    0.00   0.00   0.00  0.60  0.10  0.00  0.00 3];

% line data format
% line: from bus, to bus, resistance(pu), reactance(pu),
%       line charging(pu), tap ratio, phase shifter angle (degrees)

line = [ 1 2 0.02   0.06   0.06   1. 0. ;
         1 3 0.08   0.24   0.05   1. 0. ;
      	 2 3 0.06   0.18   0.04   1. 0. ;
		 2 4 0.06   0.18   0.04   1. 0. ;
		 2 5 0.04   0.12   0.03   1. 0. ;
		 3 4 0.01   0.03   0.02   1. 0. ;
		 4 5 0.08   0.24   0.05   1. 0. ];

 save('datastag.mat','bus','line');

% Machine data format
% machine: base mva, base kv, base field voltage
%          leakage reactance x_1(pu), resistance r_a(pu),
%          d-axis sychronous reactance x_d(pu), d-axis transient
%          reactance x'_d(pu), d-axis subtransient reactance x"_d(pu),
%          d-axis open-circuit time constant T'_do(sec), d-axis open-
%          circuit subtransient time constant T"_do(sec),
%          q-axis open-circuit time constant T'_qo(sec), q-axis open
%          circuit subtransient time constant T"_qo(sec),
%          inertia constant H(sec), damping coefficient d_o(pu),
%          damping coefficient d_1(pu), bus number
% note: all the following machines use electro-mechanical model
mac_con = [ ...
1 1 100 0.000  0.000  0.8958  0.1198  0 6.00  0 0.8645 0.0969 0 0.535 0  6.4  0.0 0 1 0 0 1 1;
2 2 100 0.000  0.000  1.3125  0.1813  0 5.89  0 1.2578 0.1500 0 0.600 0  3.01 0.0 0 2 0 0 1 1];

% conversion de parametros a una base 100 MVA
%Xd = 100*mac_con(:,6)./mac_con(:,3);
% X1d = 100*mac_con(:,7)./mac_con(:,3);
%  Xq = 100*mac_con(:,11)./mac_con(:,3);
%   X1q = 100*mac_con(:,12)./mac_con(:,3);
%    H = mac_con(:,16).*mac_con(:,3)/100;
%     D = zeros(2,1);
% D = mac_con(:,17).*mac_con(:,3)/100;
%      T1d0 = mac_con(:,9);
%        T1q0 = mac_con(:,14);


% load_con = [ ...
% 5 1.0 1.0 0.0 0.0;
% 7 1.0 1.0 0.0 0.0;
% 8 1.0 1.0 0.0 0.0;
% 9 1.0 1.0 0.0 0.0];




%writematrix(bus, 'datastag.xlsx', 'Sheet','bus');
%writematrix(line, 'datastag.xlsx', 'Sheet','line');
writematrix(mac_con, 'datastag.xlsx', 'Sheet','mac_con');