data = edfread("r01.edf");
electrode = data.Abdomen_2;
processedElectrode = transform(electrode);
sampling_frequency = 1E3;
time = 0: 1E-3 : 300-1E-3;
plot(time, processedElectrode)
title("Registro ECG - Abdomen - 1")
xlabel("Tiempo [s]")
ylabel("Voltaje [mV]")


function y = transform(x)
    y = zeros(1, length(x)*5000);
    for k = 1:length(x)
        values = x(k);
        y(1,5000*(k-1)+1:5000*k) = values{1};
    end
end