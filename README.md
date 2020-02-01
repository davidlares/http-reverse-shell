# HTTP Reverse Shell

The following is a refactored version for the `HTTP` protocol. The `TCP` version for this software is [here](https://github.com/davidlares/tcp-reverse-shell)

This repository contains a full outline example of how to perform `HTTP` Reverse Shell using only built-in commands from the Python core language. So, in a few words. an attacker should bypass the built-in or host-based firewall on the OS (default will block non-legit incoming traffic) and find a way to send a malicious file to a client.

## Why HTTP

In a considerable amount of scenarios, there are higher possibilities to have open connections for the `HTTP protocol` on the outbound firewall rules.

The `HTTP traffic` goes into every network and can be "harder" to analyze in case of infection.  

## Scenario

Same set-up for the `TCP` reverse shell example

## Dependencies

This PoC was built with Python 2.x to avoid encoding problems with the client-server connection and the byte data-types. It can be easily upgraded using the encoding methods for the resulting outputs generated during the experience.

You will need to install the `requests` Python package for performing `GET` and `POST` requests to the server in order to grab information and for sending commands to the client.

## How it works

Let me summarize this into single steps.

1. Set up a `Server` and a `Client` (`GET/POST` method to send data back and forth to the activities)
2. The client will start a reverse HTTP method (GET request) back to the server.
3. The server side we are going to start a shell and send the command back to the target
4. Once the client received, a `CMD` process will start for the `POST` method
5. TO make sure it cannot be banned, a 3-second sleep will set between requests

## How to use

First, the attacker should be listening to client connections by specifying a common IP and port for the `TCP` connection, both are hard-coded on the `client.py` and the `server.py` files. So, you should start running the `server.py` file before listening to client connections with the right network values (IP and ports).

Once the reverse `TCP tunnel` is made, we got the user-input that is sent to the target machine. Once received, the `client.py` will process that command with the help of the `subprocess` python-mode and send back the `stdout` or `stderr` of the resulting execution.

The `setup.py` file is needed for creating the `client.exe` binary. You will need to download the `py2exe 0.6.9 exe` file from the internet (python 2.x is required) an run it inside a Windows machine. Important: you should have both files (`client.py` and `setup.py`) at the same level as the installer.

There's an example of the `client.exe` with the log, on the `dist` directory.

## Persisting backdoor logic

The whole point of infecting a machine is, first besides "attacking" is to persist the connection to gather information more than once. For that there's the `persistence.py` file, it contains a full logic for generating a `Windows User Registry` and performs a `directory reconnaissance` to check if the `backdoor` file is present on a certain hard-coded directory.

This is done by creating a copy of the binary file in a different path (even when it could be deleted). And adding an `HKEY_CURRENT_USER` programmatically that let the program run and start automatically even if the machine if booted.


## Code actions

Once the connection is made, we have 3 particular actions that we can perform.

1. `Shell> [Type your command]`. this action will output the result of executing something.
2. `Shell> grab -f [file]`. the `grab -f` command will transfer or extract data from the target by setting a placeholder for the file. Basically evaluates if the type (on the header) `content-type` is `multipart/form-data`, if yes, we are getting the received file headers and request to the `cgi.FieldStorage` Class then `downloads` the file and `closes` the `HTTP connection`
3. `Shell> terminate`. Will close the socket connections

## Credits

 - [David E Lares](https://twitter.com/davidlares3)

## License

 - [MIT](https://opensource.org/licenses/MIT)
