# Compile program with GCC
# -g: GDB Debug flag enabled
# -z: execstack: Disables DEP
# -fno-stack-protector: Disables stack smashing protection (canaries)
# -Wno-implicit-function-declaration disable function warnings
# -Wno-format (-Wno-format-security) disable data format warnings
# -mpreferred-stack-boundary=4 (default is 4) removes alignment bytes optimization
#
# chown and chmod add SETUID permissions to program

readBinaryData1: readBinaryData1.c
	gcc \
		-g \
        -m32 \
        -no-pie \
		-Wno-implicit-function-declaration \
		-Wno-format \
		-mpreferred-stack-boundary=4 \
		-o readBinaryData1 \
		readBinaryData1.c 

	sudo chown root ./readBinaryData1 
	sudo chmod u+s ./readBinaryData1
