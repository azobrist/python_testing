#!/bin/bash
#scp pi@10.70.56.20:~/data/$1 .
for i in $(seq $2 6);
do
	echo $i
	case $i in
		0) size="12mm";;
		1) size="15mm";;
		2) size="20mm";;
		3) size="26mm";;
		4) size="35mm";;
		5) size="40mm";;
		6) size="50mm";;
	esac
	file="s$1_"$size"_static_test"
	echo "running test for $file"
	read -p "Press enter to continue"
	sudo minicom -C $file
	./plottsv.py $file
	./xwriter.py $file
done

