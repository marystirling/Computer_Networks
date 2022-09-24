# Computer_Networks
# Assignment 1

################################################################################################

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

Then, there are three mininet tests that we want to run. Open a bash shell and type in the following commands

$ sudo mn --topo=single,3 --link=tc, delay=10ms


#################################################################################################
