# Computer_Networks
# Assignment 1



Skeleton code and part of README provided by Professor Andy Gokhale at Vanderbilt University.

The purpose of this assignment is to program an Application Layer custom protocol for a Smart Refrigerator IoT edge device. It can send either a grocery order or health status message to two different servers: a grocery server and a health status server. 

The message format is defined in the specification where data serialization can easily be JSON (as json) or Flatbuffers (as fbufs).

The business logic layer code is as follows:
  (1) refrigerator.py - represents the client-side logic of the smart refrigerator
  (2) grocery_server.py - represents the server-side logic of the grocery server
  (3) health_server.py - represents the server-side logic of the health server
  (4) config.ini - represents a common system-wide set of configurations.

We define the data serialization in config.ini.

The Application Layer code is as follows (defined under the applnlayer subfolder):
  (1) ApplnMessageTypes.py - defines skeletons for the 3 message types supported by our
  (2) CustomApplnProtocol.py - defines all the logic to send/receive the different messages and the exceptions that can be raised (custom application protocol)

The Transport Layer is as follows (defined under the transportlayer subfolder)
  (1) CustomTransportProtocol.py - mostly a No-Op; delegates to network layer

The Network Layer is as follows (defined under the networklayer subfolder)
  (1) CustomNetworkProtocol.py - Mostly a No-OP. Simply delegates to ZeroMQ

The Psuedo Link Layer is suported by our ZeroMQ messaging layer

The (Pseudo) Physical Layer supports the actual communication. This can be intra-host using localhost, or mininet, or Docker Swarm/Kubernetes cluster or actual distributed hosts


# How to run Assignment 1 in mininet:
Define what serialization you want to use in config.ini as either json or fbufs.

Then, there are three mininet tests that we want to run. 

# Mininet Test 1
Open a bash shell and type in the following commands to create 3 hosts and 1 switch.

$ sudo mn --topo=single,3 --link=tc, delay=10ms

Then type:
$ xterm h1 h2 h3

You want to deploy refrigerator client on h1, grocery server on h2, and health server on h3.

On each xterm window that pops up, navigate to the directory where these files are located on system.

For h1, type in that terminal:
$ python3 refrigerator.py -g 10.0.0.2 -s 10.0.0.3

For h2, type in that terminal:
$ python3 grocery_server.py

For h3, type in that terminal:
$ python3 health_server.py

# Mininet Test 2
Open a bash shell and type in the following commands to create 3 hosts and 3 switches

$ sudo mn --topo=linear,3 --link=tc, delay=10ms

Then type:
$ xterm h1 h2 h3

You want to deploy refrigerator client on h1, grocery server on h2, and health server on h3.

On each xterm window that pops up, navigate to the directory where these files are located on system.

For h1, type in that terminal:
$ python3 refrigerator.py -g 10.0.0.2 -s 10.0.0.3

For h2, type in that terminal:
$ python3 grocery_server.py

For h3, type in that terminal:
$ python3 health_server.py

# Mininet Test 3
Open a bash shell and type in the following commands to create 27 hosts and 13 switches

$ sudo mn --topo=tree,depth=3,fanout=3 --link=tc,delay=10ms

Then type:
$ xterm h1 h12 h27

You want to deploy refrigerator client on h12, grocery server on h1, and health server on h27 (or any other middle leaves).

On each xterm window that pops up, navigate to the directory where these files are located on system.

For h1, type in that terminal:
$ python3 grocery_server.py

For h12, type in that terminal:
$ python3 refrigerator.py -g 10.0.0.1 -s 10.0.0.27

For h27, type in that terminal:
$ python3 health_server.py

# Running Assignment 1 on a single VM
You can also just test the code on a single VM by opening three different bash cells. On each one, navigate to the directory of the three needed python files (refrigerator.py, grocery_server.py, health_server.py. Type one of these commands in each of the three bash shells:
bash shell 1:
$ python3 refrigerator.py

bash shell 2:
$ python3 grocery_server.py

bash shell 3:
$ python3 health_server.py
