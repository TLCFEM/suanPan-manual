reset
set term svg size 750,300
set output "RESULT.svg"
unset key
set xrange [*:*]
set yrange [*:*]
set xlabel "input"
set ylabel "output"
set grid
plot "RESULT.txt" u 1:2 w l lw 2
set output
