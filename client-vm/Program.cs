using System;
using System.Collections.Generic;
using System.Threading;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Edge;
using OpenQA.Selenium.Support;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;
using System.Security.AccessControl;
using System.IO;

//turn off warnings, make running code cleaner, will renable at the end of code
#pragma warning disable

//this powershell option should hide the terminal when the code is executed
//"powershell.integratedConsole.showOnStartup": false

public class ConjureLog
{
    public string user, ip, time, type, url, success, message = "none";
    public string dest = "none";
}

class ConjureProgram
{
    static IWebDriver driver;
    static Random random = new Random();
    static bool paused;
    public static List<ConjureLog> Logs = new List<ConjureLog>();

    static bool WebNav = true;

    static void Main(string[] args)
    {
        if (args.Length == 2)
        {
            string dest = args[0];
            string url = args[1];
            DownloadFromWeb(dest, url);
            foreach (var log in Logs)
            {
                Console.WriteLine(log.user + ' ' + log.time + ", " + log.type + ", " + log.success + ", " + log.url + ", " + log.dest + ", " + log.message);
            }
        }
        if (args.Length == 1)
        {
            string dest = args[0];
            OpenDownload(dest, "");
            foreach (var log in Logs)
            {
                Console.WriteLine(log.user + ' ' + log.time + ", " + log.type + ", " + log.success + ", " + log.dest + ", " + log.message);
            }
        }
        if (args.Length == 0)
        {
            while (WebNav)
            {
                WebNavigation();

                //use this time to continue web navigation until we receive an 'end' command from the server
                //can make this number random and much longer to simulate the user tendency to search for random periods of time
                //allows program to generate web traffic, quit/stop as normal, and continue on again in a new iteration without the server needing to start it up again
                Thread.Sleep(10000);
            }
            foreach (var log in Logs)
            {
                Console.WriteLine(log.user + ' ' + log.time + ", " + log.type + ", " + log.success + ", " + log.url + ", " + log.dest + ", " + log.message);
            }
        }
    }

    // DOWNLOAD
    static void DownloadFromWeb(string dest, string url)
    {
        ConjureLog log1 = new ConjureLog(); // One log per try/catch statement
        ConjureLog log2 = new ConjureLog();
        ConjureLog log3 = new ConjureLog();
        ConjureLog log4 = new ConjureLog();
        ConjureLog log5 = new ConjureLog();
        ConjureLog log6 = new ConjureLog();
        IPAddress ip = Dns.GetHostEntry(Dns.GetHostName()).AddressList[1];

        log1.ip = log2.ip = log3.ip = log4.ip = log5.ip = log6.ip = ip.ToString();
        log1.user = log2.user = log3.user = log4.user = log5.user = log6.user = Environment.UserName;
        log1.url = log2.url = log3.url = log4.url = log5.url = log6.url = url;
        log1.dest = log2.dest = log3.dest = log4.dest = log5.dest = log6.dest = dest;
        log1.type = log2.type = log3.type = log4.type = log5.type = log6.type = "download";
        string fileName = Path.GetFileName(url);

        // Attempt: HTTPClient
        log1.time = DateTime.UtcNow.ToString();
        try
        {
            using (var client = new HttpClient())
            {
                HttpResponseMessage response = client.GetAsync(url).Result;
                byte[] content = response.Content.ReadAsByteArrayAsync().Result;
                File.WriteAllBytes(destPath, content);
            }
            log1.success = "success";
            log1.message = "no error";
            Logs.Add(log1);
            OpenDownload(fileName, dest);
            return;
        }
        catch (Exception e)
        {
            log1.message = "HTTP Client: " + e.GetType().ToString().Split('.')[1];
            log1.success = "attempt failed";
            Logs.Add(log1);
        }


        // Attempt: WebClient DownloadData and WriteAllBytes
        log2.time = DateTime.UtcNow.ToString();
        try
        {
            using (WebClient client = new WebClient())
            {
                byte[] fileData = client.DownloadData(url);
                File.WriteAllBytes(destPath, fileData);
            }
            log2.success = "success";
            log2.message = "no error";
            Logs.Add(log2);
            OpenDownload(fileName, dest);
            return;
        }
        catch (Exception e)
        {
            log2.message = "Web Client with DownloadData: " + e.GetType().ToString().Split('.')[1];
            log2.success = "attempt failed";
            Logs.Add(log2);
        }

        // Attempt: WebClient and DownloadFile
        log3.time = DateTime.UtcNow.ToString();
        try
        {
            using (WebClient client = new WebClient())
            {
                client.DownloadFile(url, destPath);
            }
            log3.success = "success";
            log3.message = "no error";
            Logs.Add(log3);
            OpenDownload(fileName, dest);
            return;
        }
        catch (Exception e)
        {
            log3.message = "Web Client with DownloadFile: " + e.GetType().ToString().Split('.')[1];
            log3.success = "attempt failed";
            Logs.Add(log3);
        }

        // Attempt: HttpWebRequest
        log4.time = DateTime.UtcNow.ToString();
        try
        {
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
            HttpWebResponse response = (HttpWebResponse)request.GetResponse();

            using (Stream responseStream = response.GetResponseStream())
            using (FileStream fileStream = File.Create(destPath))
            {
                responseStream.CopyTo(fileStream);
            }
            log4.success = "success";
            log4.message = "no error";
            Logs.Add(log4);
            OpenDownload(fileName, dest);
            return;
        }
        catch (Exception e)
        {
            log4.message = "HTTPWebRequest: " + e.GetType().ToString().Split('.')[1];
            log4.success = "attempt failed";
            Logs.Add(log4);
        }

        // Attempt: WebRequest
        log5.time = DateTime.UtcNow.ToString();
        try
        {
            WebRequest request = WebRequest.Create(url);
            using (WebResponse response = request.GetResponse())
            {
                using (Stream responseStream = response.GetResponseStream())
                {
                    using (var fileStream = File.Create(destPath))
                    {
                        responseStream.CopyTo(fileStream);
                    }
                }
            }
            log5.success = "success";
            log5.message = "no error";
            Logs.Add(log5);
            OpenDownload(fileName, dest);
            return;
        }
        catch (Exception e)
        {
            log5.message = "WebRequest: " + e.GetType().ToString().Split('.')[1];
            log5.success = "attempt failed";
            Logs.Add(log5);
        }

        // Attempt: Curl Command
        log6.time = DateTime.UtcNow.ToString();
        try
        {
            Process.Start("curl -o " + destPath + " " + url);
            log6.success = "success";
            log6.message = "no error";
            Logs.Add(log6);
            OpenDownload(fileName, dest);
            return;
        }
        catch (Exception e)
        {
            log6.message = e.GetType().ToString().Split('.')[1] + " error running curl -o " + destPath + " " + url;
            log6.success = "download failure";
            Logs.Add(log6);
        }

    }

    static void OpenDownload(string fileName, string path)
    {
        
        ConjureLog log1 = new ConjureLog(); // One log per try/catch statement
        ConjureLog log2 = new ConjureLog(); // One log per try/catch statement

        IPAddress ip = Dns.GetHostEntry(Dns.GetHostName()).AddressList[1];
        log1.ip = log2.ip = ip.ToString();
        log1.user = log2.user = Environment.UserName;
        log1.url = log2.url = "none";
        log1.dest = log2.dest = fileName;
        log1.type = log2.type = "execute";
        log1.time = log2.time = DateTime.UtcNow.ToString();

        //try statement to execute/open the downloaded file
        //tried many different things but powershell worked the best for us
        //cd into directory of downloaded file, use powershell to execute/open it
        try
        {
            //System.Diagnostics.Process.Start("cmd.exe", "cd " + path + " & start /B " + fileName);
            System.Diagnostics.Process.Start("powershell.exe", "cd " + path + "; .\\" + fileName);
            log2.success = "success";
            log2.message = "none";
            Logs.Add(log2);
            return;
        }
        catch (Exception e)
        {
            log2.success = "failure";
            Console.WriteLine(e.Message);
            log2.message = "Process Start: " + e.GetType().ToString().Split('.')[1];
            Logs.Add(log2);
            return;
        }
    }

    // WEB NAGIVATION
    static void WebNavigation()
    {
        //list of possible websites the driver can search
        List<string> webList = new List<string>{
            "bing.com",
            "google.com",
            "facebook.com",
            "youtube.com",
            "yahoo.com",
            "ebay.com",
            "amazon.com",
            "dell.com",
            "ua.edu",
            "wikipedia.com",
            "python.org"
            };

        // string[] lines = System.IO.File.ReadAllLines("websites.txt");
        // webList.AddRange(lines);

        string randWeb = webList[random.Next(webList.Count)];
        string url = "https://www." + randWeb;


        //uncomment for to use an edge driver
        //will need to change the EdgeOptions to remove the automate software flag
        //EdgeOptions edgeOptions = new EdgeOptions();
        //Remove "Edge is being controlled by automated software"
        //edgeOptions.AddAdditionalEdgeOption("AddExcludedArgument", "enable-automation");
        //driver = new EdgeDriver(edgeOptions);

        //using a chrome driver
        var chromeOptions = new ChromeOptions();
        // Remove "controlled by automated software"
        chromeOptions.AddArgument("--start-maximized");
        chromeOptions.AddExcludedArgument("enable-automation");
        driver = new ChromeDriver(chromeOptions);

        driver.Navigate().GoToUrl(url);
        Thread.Sleep(GetRandInt());

        //list to hold every link we've already been to, avoiding redundant clicking
        List<IWebElement> clickedLinks = new List<IWebElement>();
        List<string> clickedStrings = new List<string>();
        bool tabIsOpen = true;

        //use javascript executor for scrolling + clicking
        //works much better than the Pathlink.click() from Selenium
        IJavaScriptExecutor executor = (IJavaScriptExecutor)driver;


        while (tabIsOpen)
        {
            bool paused = true;
            paused = ExecuteClient();

            ConjureLog log = new ConjureLog();
            IPAddress ip = Dns.GetHostEntry(Dns.GetHostName()).AddressList[1];
            log.ip = ip.ToString();

            log.user = Environment.UserName;
            log.type = "web-nav";
            log.url = url;

            //use paused to allow server to control the web navigation process
            if (!paused)
            {
                Thread.Sleep(GetRandInt());

                //find all links on current page
                var pathLinks = driver.FindElements(By.TagName("a"));
                //filter links to get clickable ones
                List<IWebElement> visibleLinks = GetVisibleLinks(pathLinks, log);

                if (CheckVisibleLinksSize(visibleLinks) == false)
                {
                    return;
                }

                IWebElement pathLink = null;
                string elementID = " ";


                //avoiding clicking on same links
                //filter element for id, make sure id is not in clickedStrings list
                //if id exists, pick a new one
                //if not, add string to clickedStrings and break from loop
                //limits the ability of the code to search for a long time, can comment out to allow for some errors and increase running time
                while (pathLink == null || clickedStrings.Contains(elementID))
                {
                    pathLink = visibleLinks[random.Next(visibleLinks.Count)];
                    elementID = pathLink.ToString();
                    elementID = elementID.Substring(14, 32);

                    if (clickedStrings.Contains(elementID))
                    {
                        visibleLinks.Remove(pathLink);
                        if (CheckVisibleLinksSize(visibleLinks) == false)
                        {
                            return;
                        }
                        pathLink = visibleLinks[random.Next(visibleLinks.Count)];
                    }
                    else
                    {
                        clickedStrings.Add(elementID);
                        break;
                    }
                }


                ScrollToElement(pathLink, executor);

                Thread.Sleep(GetRandInt());

                log.time = DateTime.UtcNow.ToString();

                try
                {
                    //use javascript executor to click on the selected web element 
                    executor.ExecuteScript("arguments[0].click();", pathLink);
                    log.url = driver.Url;
                    log.success = "success";
                    Logs.Add(log);
                }
                catch (Exception e)
                {
                    log.message = "Click Failure: " + e.Message;
                    log.url = driver.Url;
                    log.success = "failure";
                    Logs.Add(log);
                }
                visibleLinks.Clear();


                //change this quitnum value to make the program run longer (bigger quitnum range) or shorter (smaller range)
                int quitNum = random.Next(0, 200);
                if (quitNum == 0)
                {
                    tabIsOpen = false;
                    Console.WriteLine("quitnum = 0");
                    Thread.Sleep(500);
                    break;
                }
            }
        }
        driver.Quit();

    }

    //filter through all links to find ones that are clickable by driver, helps with clicking errors
    static List<IWebElement> GetVisibleLinks(IList<IWebElement> pathLinks, ConjureLog log)
    {
        log.time = DateTime.UtcNow.ToString();
        List<IWebElement> visibleLinks = new List<IWebElement>();
        foreach (var link in pathLinks)
        {
            try
            {
                if (link.Displayed && link.Enabled && HasSize(link))
                {
                    visibleLinks.Add(link);
                }
            }
            catch (Exception e)
            {
                log.success = "failure";
                log.message = "Failure in GetVisibleLink: " + e.Message;
                Logs.Add(log);
            }
        }
        return visibleLinks;
    }

    static bool CheckVisibleLinksSize(List<IWebElement> visibleLinks)
    {
        if (visibleLinks.Count == 0)
        {
            Thread.Sleep(3000);
            Console.WriteLine("No Visible Links :(\n");
            driver.Quit();
            return false;
        }
        else
        {
            return true;
        }
    }

    static bool HasSize(IWebElement link)
    {
        return link.Size.Height > 0 && link.Size.Width > 0;
    }

    static int GetRandInt()
    {
        int waitTime = random.Next(1, 2);
        return waitTime * 1000;
    }

    static void ScrollToElement(IWebElement element, IJavaScriptExecutor executor)
    {
        ConjureLog log = new ConjureLog();
        IPAddress ip = Dns.GetHostEntry(Dns.GetHostName()).AddressList[1];
        log.ip = ip.ToString();

        log.user = Environment.UserName;
        var height = element.Size.Height;
        var width = element.Size.Width;
        var pageHeight = 0;

        //get the height of the entire page
        //using javascript executor for the scrolling and html parsing info
        try
        {
            pageHeight = (int)(executor.ExecuteScript("return document.body.scrollHeight") as long? ?? 0) / (5 / 4);
        }
        catch (Exception e)
        {
            log.success = "failure";
            log.message = "Failure getting height: " + e.Message;
            Logs.Add(log);
        }
        //use to set range of scrolling 
        var minHeight = pageHeight / 20;
        if (pageHeight <= 100)
        {
            minHeight = 0;
        }
        var randHeight = random.Next(minHeight, pageHeight);
        var currPos = 0;
        var scrollHeight = 1;


        //use a loop to smoothly scroll down the page using the currPos as the random scrolling speed/distance
        while (currPos <= scrollHeight)
        {
            currPos += GetRandScrollSpeed();
            try
            {
                executor.ExecuteScript("window.scrollTo(0, " + currPos + ");");
            }
            catch (Exception e)
            {
                log.success = "failure";
                log.message = "Failure scrolling to element: " + e.Message;
                Logs.Add(log);
            }
            scrollHeight = height + randHeight;
        }
    }

    static int GetRandScrollSpeed()
    {
        return random.Next(5, 14);
    }

    //function to communicate with the conjure server
    //uses sockets to receive pause, continue, logs, end commands
    static bool ExecuteClient()
    {
        // Establish the remote endpoint for the socket. 
        // This example uses port 54321 on the local computer.
        IPHostEntry ips = Dns.GetHostEntry(Dns.GetHostName());

        //use computer IP to create the socket, will be the 2nd item in this address list
        IPAddress ipAddr = ips.AddressList[1];
        //enter IP of the conjure server
        IPAddress serverIPAddr = IPAddress.Parse("10.241.1.141");
        //the end point of the server that the socket will connect to 
        IPEndPoint serverPoint = new IPEndPoint(serverIPAddr, 54321);

        try
        {
            //create a socket using TCP to connect local system with the server
            Socket sender = new Socket(ipAddr.AddressFamily, SocketType.Stream, ProtocolType.Tcp);

            //Console.WriteLine("Trying to Connect...");

            //connect the socket binded to the local system to the server end point
            sender.Connect(serverPoint);


            Console.WriteLine("Socket connected to -> {0} ", sender.RemoteEndPoint.ToString());

            // Data buffer of bytes used to receive message
            byte[] messageReceived = new byte[1024];

            //receive message from server
            int byteRecv = sender.Receive(messageReceived);
            //convert message from bytes to string text
            string message = Encoding.ASCII.GetString(messageReceived, 0, byteRecv);
            Console.WriteLine("Message from Server -> {0}", message);

            //check the command sent from server
            if (message == "pause")
            {
                Console.WriteLine("Paused...");
                sender.Close();
                paused = true;
                return paused;
            }
            else if (message == "continue")
            {
                Console.WriteLine("Continuing...");
                sender.Close();
                paused = false;
                return paused;
            }
            else if (message == "end")
            {
                Console.WriteLine("Ending Program...");
                sender.Close();
                driver.Quit();
                Environment.Exit(0);
                return paused;
            }
            else if (message == "logs")
            {
                sendLogs(sender);
                return paused;
            }
            else if (message == "download")
            {
                //acknowledge to the server that download has been received
                string ackSend = "ack";
                byte[] ackMsg = Encoding.ASCII.GetBytes(ackSend);
                int byteSent = sender.Send(ackMsg);

                //read in the url for the file to be downloaded
                byte[] urlMsg = new byte[1024];
                int urlRecv = sender.Receive(urlMsg);
                string urlStr = Encoding.ASCII.GetString(urlMsg, 0, urlRecv);
                Console.WriteLine(urlStr);

                //pass the destination path of the download/where you want it to be downloaded, and the url of the file
                DownloadFromWeb("C:\\users\\vboxuser\\Desktop", urlStr);
            }
            //close the socket to free up the port
            //return the variable paused to maintain the current value
            //if server sent the pause command, code should stay paused until other command is received
            sender.Shutdown(SocketShutdown.Both);
            sender.Close();
            return paused;
        }

        //Manage of Socket's Exceptions
        catch (ArgumentNullException ane)
        {
            return paused;
        }

        catch (SocketException se)
        {
            return paused;
        }

        catch (Exception e)
        {
            return paused;
        }
    }

    //send the log data to the server if requested 
    static void sendLogs(Socket sender)
    {
        //list to hold every log and all its strings
        //easier to send over socket with list of lists of strings, rather than accessing each ConjureLog member while sending
        List<List<string>> logList = new List<List<string>>();
        //iterate over each Log in our list, assign each log string to a temp
        //make temp List of the temp data, add this to our list of logs to send to the server
        for (int idx = 0; idx < Logs.Count; idx++)
        {
            string tempMsg = Logs[idx].message;
            string tempDest = Logs[idx].dest;
            string tempURL = Logs[idx].url;
            string tempSuccess = Logs[idx].success;
            string tempTime = Logs[idx].time;
            string tempType = Logs[idx].type;
            string tempUser = Logs[idx].user;
            string tempIP = Logs[idx].ip;
            List<string> tmpLog = new List<string> {tempIP, tempSuccess, tempURL, tempUser, tempTime, tempMsg, tempType, tempDest};
            logList.Add(tmpLog);
        }

        //tell the server how many lists of logs are being sent
        string sizeLogs = logList.Count.ToString();
        byte[] logSizeMsg = Encoding.ASCII.GetBytes(sizeLogs);
        int byteSent = sender.Send(logSizeMsg);

        //iterate through each list of logs in Logs, then each member of each log, send to server
        for (int i = 0; i < logList.Count;)
        {
            for (int j = 0; j < logList[i].Count;)
            {
                byte[] logData = Encoding.ASCII.GetBytes(logList[i][j]);
                Console.WriteLine(Encoding.UTF8.GetString(logData));
                int logRet = sender.Send(logData);

                //server will send "next" command when log item is sent
                byte[] nextMsg = new byte[1024];
                int nextMsgBytes = sender.Receive(nextMsg);
                string nextStr = Encoding.ASCII.GetString(nextMsg, 0, nextMsgBytes);

                //we then receive the next command and increment the index to send the next item in the log data list
                if (nextStr == "next")
                {
                    j++;
                }
            }

            //receive ack message from server to know server saved list of logs properly
            byte[] messageReceived = new byte[1024];
            int byteRecv = sender.Receive(messageReceived);
            string ack = Encoding.ASCII.GetString(messageReceived, 0, byteRecv);
            //when we get the ack message, increment the index of lists to get the next log list
            if (ack == "ack")
            {
                Console.WriteLine("Log List Accepted");
                i++;
            }
        }
        //tell server we are done sending log data
        byte[] msg = Encoding.ASCII.GetBytes("done");
        int doneMsg = sender.Send(msg);
        Console.WriteLine("Sent Done Message");
    }
}

#pragma warning restore