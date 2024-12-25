# Chat with sockets
This is my simple project about web sockets, I made it for training purpose and may update it later.

## Setup
1. open terminal and run `server.py` file. Check the `misc/debug_vars.py` for a flexible output adjustments
2. run `client.py` (you can run unlimited amout of clients at the same time, each one will create a separated client)

Check `socketinfo.py` if you want to adjust any behavior

## Debug commands
### There are a few debug commands which you can input into server's terminal
1. `clients` - will print port of every connected client
2. `dc all` - will forcefully disconnect every client from the server and automatically clear the `active_sockets` list
3. `debug print_recieved` - check `misc/debug_vars.py` for info
4. `debug print_softshut` - check `misc/debug_vars.py` for info

