# Compile program with GCC
# -g: GDB Debug flag enabled
# -z: execstack: Disables DEP
# -fno-stack-protector: Disables stack smashing protection (canaries)
# -Wno-implicit-function-declaration disable function warnings
# -Wno-format (-Wno-format-security) disable data format warnings
# -mpreferred-stack-boundary=4 (default is 4) removes alignment bytes optimization

authFlagAdmin: authFlagAdmin.c
	gcc \
		-g \
        -m32 \
        -no-pie \
		-z execstack \
		-fno-stack-protector \
		-Wno-implicit-function-declaration \
		-Wno-format \
		-mpreferred-stack-boundary=4 \
		-o authFlagAdmin \
		authFlagAdmin.c 
