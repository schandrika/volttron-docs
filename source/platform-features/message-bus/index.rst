.. _Message-Bus:

===========
Message Bus
===========

The VOLTTRON message bus is the mechanism responsible for enabling communication between agents, drivers, and platform
instances.  The message bus supports communication using the :ref:`Publish/Subscribe Paradigm <VIP-Overview>` and
:ref:`JSON RPC <Remote-Procedure-Calls>`.
Currently VOLTTRON may be configured to use only Zero MQ as message bus. We are working on porting RabbitMQ
support from monolithic version of VOLTTRON(version < 10) to the latest modular version of VOLTTRON(version>=10)

To standardize message bus communication, VOLTTRON implements VIP - VOLTTRON Interconnect Protocol.  VIP defines
patterns for pub/sub communication as well as JSON-RPC, and allows for the creation of agent communication subsystems.

For more information please explore the message bus documentation linked below:

.. toctree::
    :caption: Message Bus Topics
    :maxdepth: 2

    topics
    vip/vip-overview

