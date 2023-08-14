---------------STEPS TO INSTALL PYTHON AND NECESSARY LIBRARIES-------------------------
1. Python - (sudo apt install python3)
2. Python modules (pip3 install <module name>)
-socket
-pyDH
-base64
-sys
-os
-hashlib
-binascii
-time
-cryptography 





-----------------------------STEPS TO EXECUTE CODE--------------------------------------
1. Create a text file named "mesage.txt" containing the message you want the code to encryt and send to the other program. The program will handle the rest
2. Open up two terminals, one for Alice and one for Bob.
3. Execute the Alice module first with the command "python3 fullCommsAlice.py"
4. Execute the Bob module next, using the command "python3 fullCommsBob.py"
5. We should see the initial greeting of Bob -> Alice, then Alice will send her message both signed and hashed with the MAC and digital signature and Bob
        will verify the authenticity of both.
