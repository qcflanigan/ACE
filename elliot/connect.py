### Upload executables to client(sftp), execute(ssh), remove file, leave. ###

import paramiko
from paramiko import SSHClient
import yaml

#change the following to iterate though list and assign

# Consider changing to IPv6
IP =    "10.65.181.206"
PORT =  22
USER =  "futureleaders"
PASS =  "Conjure2023!"

rFile = "text.txt"
rpath = rf"C:\Users\futureleaders\elliot\{rFile}"
lFile = "script.py"

def runPyFile(IP, PORT, USER, PASS, file):

    rpath = rf"C:\Users\futureleaders\elliot\{file}"

    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(IP, port=PORT, username=USER, password=PASS)

    sftp = client.open_sftp()
    sftp.put(file, rpath)

    stdin, stdout, stderr = client.exec_command(f'more {rpath}')
    ###stdin, stdout, stderr = client.exec_command(rpath)

    output = stdout.read().decode()
    error = stderr.read().decode()

    if output:
        print("Output: ", output)

    if error:
        print("Error", error)

    client.exec_command(f'del {rpath}')

    sftp.close()
    client.close()


def runPyOneLiner(IP, PORT, USER, PASS, files, i):
    for file in files:
        if(file.split('.')[1] == "py"):
            with open(file, 'r') as code:
                command = code.read()
            command = command.replace('"',r'\"').replace("'", r"\'").replace('\n', ';').replace('testing',f'testing{i}')
            command = rf'''py -c "{command}"'''

            client = SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(IP, port=PORT, username=USER, password=PASS)

            #print(f"""sending command, {command}""")
            stdin, stdout, stderr = client.exec_command(command)

            output = stdout.read().decode()
            error = stderr.read().decode()

            if output:
                print("Output: ", output)

            if error:
                print("Error: ", error)

            client.close()
        else:
            client = SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(IP, port=PORT, username=USER, password=PASS)

            #print(f"""sending command, {command}""")
            stdin, stdout, stderr = client.exec_command(command)

            output = stdout.read().decode()
            error = stderr.read().decode()

            if output:
                print("Output: ", output)

            if error:
                print("Error: ", error)

            client.close()

#returns ip, port, username, and password
def readCreds(fileName):
    creds = yaml.safe_load(open(fileName))

    vmName=[]

    for entry in creds:
        #print(entry)
        #print(creds[entry])
        vmName.append(entry)
        #for item in creds[entry]:       
            #print(item)
            #print(creds[entry][item])
    
    #return ip, port, user, passw
    return vmName, creds

def runExe(IP, PORT, USER, PASS, ftpPath): #Not yer functional
    
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(IP, port=PORT, username=USER, password=PASS)

    sftp = client.open_sftp()
    sftp.put(file, rpath)

    stdin, stdout, stderr = client.exec_command(f'')
    ###stdin, stdout, stderr = client.exec_command(rpath)

    output = stdout.read().decode()
    error = stderr.read().decode()

    if output:
        print("Output: ", output)

    if error:
        print("Error", error)

    client.exec_command(f'del {rpath}')

    sftp.close()
    client.close()



#runPyFile(IP, PORT, USER, PASS, rFile)
#runPyOneLiner(IP, PORT, USER, PASS, lFile)

#print(readCreds("creds.yaml", "conjure-1"))
