// DLL proxying template made from a dnsapi.dll proxy
// Runs the conjure executable when called by a process
// dllmain.cpp : Defines the entry point for the DLL application.
#include "pch.h"
#include <windows.h>
#include <iostream>

#pragma comment (lib, "User32.lib")

//declare mutex name. This is used to make sure only one instance of Conjure is running on machine
const wchar_t* MUTEX_NAME = L"DNSAPIMUTEX";


int Main() {

    static HANDLE nMutex = NULL;

    while(TRUE){

         Sleep(5000); 

         //try to create mutex
        nMutex = CreateMutexW(NULL, TRUE, MUTEX_NAME);

        ///if mutex already exists, close handle and repeat while loop
        if (nMutex == NULL || GetLastError() == ERROR_ALREADY_EXISTS) {
            CloseHandle(nMutex);
        }
        else {
            //start executable and wait for process to finish.
            system("start /wait C:\\Users\\vboxuser\\source\\repos\\CSCode\\CSCode\\bin\\Debug\\net6.0\\CSCode.exe");
            CloseHandle(nMutex);
        }
    }
    return 1;
}

BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    //declare hMutex so it can be used across switch statement
    static HANDLE hMutex = NULL;

    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:

        //Start Main() in a new thread
        CreateThread(NULL, NULL, (LPTHREAD_START_ROUTINE)Main, NULL, NULL, NULL);

        break;

    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
        break;
    case DLL_PROCESS_DETACH:

        //Release Mutex before DLL detaches
        if (hMutex != NULL) {
            ReleaseMutex(hMutex);
            CloseHandle(hMutex);
            hMutex = NULL;
        }

        break;

    }

    return TRUE;
}

/*Insert export functions from getExports.py

ex:
#pragma comment(linker,"/export:DnsGetDomainName=C:\\Windows\\System32\\utilitycore.DnsGetDomainName,@1")
...
#pragma comment(linker,"/export:WriteDnsNrptRulesToRegistry=C:\\Windows\\System32\\utilitycore.WriteDnsNrptRulesToRegistry,@289")
*/