% Matriz bus, columna
% 1. Numero de nodo
% 2. Voltaje del nodo p.u.
% 3. Angul del nodo
%4. Potencia activa generada en ese nodo.
%5. Potencia reactiva
%6. Carga activa en el nodo
%7. Carga reactiva //
%8. Conductancia conectada del nodo a tierra.
%9. Susceptancia conectada del nodo a tierra, (+)Capacitiva(-)Negativa.
%10. Tipo de bus. 1 - slack 2 - PV 3 - PQ 

% Matriz line, columnas
%1. Nodo de envio
%2.Nodo de recepcion
%3.Resistencia de la linea
%4. Reactancia de la linea
%5. Susceptacia capacitiva total de la linea
%6. Pocision del tap, 1-Nominal, 0-se trata de una linea
%7. Transformadores desfasadores
bus=[1	1.06	0	0	0	0       0       0	0       1
    2	1.045	0	40	0	21.7	12.7	0	0       2
    3	1.01	0	0	0	94.2	19      0	0       2
    4	1       0	0	0	47.8	-3.9	0	0       3
    5	1       0	0	0	7.6     1.6     0	0       3
    6	1.07	0	0	0	11.2	7.5     0	0       2
    7	1       0	0	0	0       0       0	0.12	3
    8	1.09	0	0	0	0       0       0	0       2
    9	1       0	0	0	29.5	16.6	0	0.19	3
    10	1       0	0	0	9       5.8     0	0       3
    11	1       0	0	0	3.5     1.8     0	0       3
    12	1       0	0	0	6.1     1.6     0	0       3
    13	1       0	0	0	13.5	5.8     0	0.12	3
    14	1       0	0	0	14.9	5       0	0.12	3];

line=[1	2	0.01938	0.05917	0.0264	0
    1	5	0.05403	0.22304	0.0246	0
    2	3	0.04699	0.19797	0.0219	0
    2	4	0.05811	0.17632	0.0187	0
    2	5	0.05695	0.17388	0.017	0
    3	4	0.06701	0.17103	0.0173	0
    4	5	0.01335	0.04211	0.0064	0
    4	7	0       0.20912	0       0.975
    4	9	0       0.55618	0       0.95
    5	6	0       0.25202	0       1.025
    6	11	0.09498	0.1989	0       0
    6	12	0.12291	0.25581	0       0
    6	13	0.06615	0.13027	0       0
    7	8	0       0.17615	0       0
    7	9	0       0.11001	0       0
    9	10	0.03181	0.0845	0       0
    9	14	0.12711	0.27038	0       0
    10	11	0.08205	0.19207	0       0
    12	13	0.22092	0.19988	0       0
    13	14	0.17093	0.34802	0       0];

save('data14n.mat','bus','line');
