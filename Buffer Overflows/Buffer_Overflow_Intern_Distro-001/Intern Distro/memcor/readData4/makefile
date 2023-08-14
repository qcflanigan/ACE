# Compile program with GCC
# -g: GDB Debug flag enabled
# -z execstack: Disables DEP
# -fno-stack-protector: Disables stack smashing protection (canaries)
# -Wno-implicit-function-declaration disable function warnings
# -Wno-format (-Wno-format-security) disable data format warnings
# -mpreferred-stack-boundary=4 (default is 4) removes alignment bytes optimization
#
# chown and chmod add SETUID permissions to program

readData4: readData4.c
	gcc \
		-g \
        -no-pie \
        -m32 \
		-fno-stack-protector \
		-Wno-implicit-function-declaration \
		-Wno-format \
		-mpreferred-stack-boundary=4 \
		-o readData4 \
		readData4.c 

	sudo chown root ./readData4
	sudo chmod u+s ./readData4
