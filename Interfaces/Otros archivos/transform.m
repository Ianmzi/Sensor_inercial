function y = transform(x)
    y = zeros(1, length(x)*5000);
    for k = 1:length(x)
        values = x(k);
        y(1,5000*(k-1)+1:5000*k) = values{1};
    end
end