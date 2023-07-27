.. _vip-pubsub-subsystem:

================
Pubsub Subsystem
================

VOLTTRON core provides a 'pubsub' subsystem to publish and subscribe to topics on the message bus. The agent's VIP
connection can be used to access the pubsub subsystem. The message published and topic to publish to are determined by
the agent implementation. For example, the :ref:`platform driver agent <Platform-Driver-Agent>` publishes scraped
device data in a pre-defined format to topic names that start with the prefix "devices".

Publish/Subscribe based on topic name
=====================================

Publish to a topic
------------------
Below line shows an example of an agent publishing to a specific topic 'some/topic', a json string as message and
dictionary object as header.

.. code-block:: python

    self.vip.pubsub.publish('pubsub',
                            'some/topic',
                            message=f'{"value": "{self.publish_value}"',
                            headers={"datetime":"2015-12-02T00:00:00")


Subscribe to a topic
--------------------
Below line shows an example of an agent subscribing to a topic "this/topic" and registering a method onmessage() to
callback when a message gets published to the topic "this/topic". More than one callback method can be registered to
the same topic

.. code-block:: python

    self.vip.pubsub.subscribe(my_id, "this/topic", self.onmessage)

When a message is published to any topic that starts with the prefix "this/topic", the onmessage() method of the agent
will get called with the details of the actual sender, the message bus name, the actual topic name, the headers and
the message that got posted to the topic

.. code-block:: python

    def onmessage(self, peer, sender, bus, topic, headers, message):
        print("received: peer=%r, sender=%r, bus=%r, topic=%r, headers=%r, message=%r" %
              (peer, sender, bus, topic, headers, message))


Unsubscribe to a topic
----------------------

Below line shows an example of an agent unsubscribing to a topic "devices/campus1/building1/device1".
If a callback method is provided, only that method is removed from the list of methods that get
called when a message is sent to this topic prefix. If a specific callback method is not provided, all registered
callback methods will stop getting called when messages are sent to this topic.

.. code-block:: python

    self.vip.pubsub.unsubscribe_by_tags('pubsub',
                                        "devices/campus1/building1/device1",
                                        self.callback_method).get(timeout=5)

Publish/Subscribe based on semantic tags
========================================

Pubsub subsystem enables subscription and publishing to topics based semantic tags instead of specific topic names. This
helps to create a abstraction layer above vendor specific or application specific naming conventions often used for
naming devices and points. VOLTTRON provides a :ref:`tagging framework <Base-Tagging-Agent>` to enable adding semantic
tags to topics and topic prefixes. A VOLTTRON instance with a active tagging agent and tagging data store can empower
application agents to subscribe and publish to topics based on semantic tags instead of actual topic string. This
provides several advantages

  1. Application need not loop through or repeat subscription to individual entities but rather identify and
     subscribe/publish to a group of entities. For example, an agent can subscribe to "all Air Handling Units(AHUs) in
     a specific building" based on a set of tags that identify these AHUs instead of repeating subscription to
     "building1/ahu1", "building1/ahu2", etc.
  2. VOLTTRON instance or individual agents can be configured to periodically check if new entities/topics match a given
     set of tags. For example, if a new AHU gets added to a building, a subscription by tags to
     "all AHUs in that building" will automatically add subscription to the new AHU at the next refresh interval.
  3. VOLTTRON instance or individual agents can be configured to point to different tagging agents that point to
     different tag data store. Different application agents within a VOLTTRON instance can potentially make use of
     different tagging models to identity relevant entities.

Precedence
----------

Subscribe/unsubscribe by a specific topic will always get precedence over subscription by tags. For example, if you
subscribe explicitly to topic "devices/building1/ahu1" and then unsubscribe to all ahu topics by calling
unsubscribe_by_tags with condition that match "all ahus in building1", you will continue to receive messages from ahu1.

Configurations
--------------

Tagging Agent to Query
+++++++++++++++++++++++

  - When publishing or subscribing by a set of tags, the pubsub subsystem makes an RPC call to the
    "get_topics_by_tags" api of the configured tagging agent, passing the condition parameter.
  - The parameter "tag-vip-id=<tagging agent's vip id>" can be added to $VOLTTRON_HOME/config to default the tagging
    agent to be called for all publish/subscribe by tags operations
  - Individual agents can override this and point to specific tagging agent by passing the parameter "tag_vip_id" to
    Agent class' init method
  - If neither of the above is configured, the RPC call is made to the vip identity "platform.tagging"

Tag refresh interval
++++++++++++++++++++

After subscribing to topics based on a specific set of tags, VOLTTRON instance or individual agents can be
configured to periodically re-run the tag query (i.e. call to "get_topics_by_tags") and update subscription as needed.
This can be configured
  - At VOLTTRON instance level, using "tag-refresh-interval=<seconds>" in VOLTTRON_HOME/config
  - Individual agent level, using the parameter "tag_refresh_interval=<seconds>" to Agent class' init method
  - If neither is set, tag queries are NOT re-run

Topic source
+++++++++++++

In VOLTTRON, message topics are often prefixed with a word that denotes the source of the data or the agent that
generates/controls the data. For example, data scraped from devices by the
:ref:`platform driver agent <Platform-Driver-Agent>` are published to topics with prefix "devices".

A set of semantic tags or tagging query condition maps to a set of physical entities. For example, the tag condition
'ahu AND siteRef="@building1"' maps to all AHUs in building1, say 'building1/ahu1' and 'building1/ahu2'.

To derive topic name that corresponds to data related to these AHUs, we need to
prefix it with the right topic source. For example, data scraped from ahu1 and ahu2 by platform driver agent will get
published to topics 'devices/building1/ahu1' and 'devices/building1/ahu2' respectively. Whereas, analysis data of
ahu1 and ahu2 would get published to topics 'analysis/building1/ahu1' and 'analysis/building1/ahu2'

Both subscribe_by_tags and publish_by_tags functions accepts an optional 'topic_source' parameter that is used to
derive topic names from entities. The default value for topic_source is "devices" and the prefix "devices/" is added
to each of the tagging query result, to arrive at the final topic to subscribe/publish.

For example:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Parameter
     - Example value
   * - Tag query condition
     - 'ahu AND siteRef="@building1"'
   * - Matching entities
     - 'building1/ahu1' and 'building1/ahu2'
   * - topic_source
     - 'devices'
   * - Topic published/subscribed
     - 'devices/building1/ahu1' and 'devices/building1/ahu2'

Subscribe by tags
-----------------

The below code shows a example call to subscribe_by_tags with a tag query 'ahu AND siteRef="@building1"'.
With haystack model this condition will map to all AHUs in building1 and the code subscribes to devices topics of
matching AHUs. For example, "devices/building1/ahu1"

.. code-block:: python

    self.vip.pubsub.subscribe_by_tags('pubsub',
                                      'ahu AND siteRef="@building1")',
                                      self.callback_method).get(timeout=20)

The below code snippet shows subscribe_by_tags call with optional topic_source parameter set to "analysis"
With haystack model this condition will map to all AHUs in building1 and the below code results in subscription to
analysis topics of matching AHUs. For example, "analysis/building1/ahu1"

.. code-block:: python

    self.vip.pubsub.subscribe_by_tags('pubsub',
                                      'ahu AND siteRef="@building1")',
                                      self.callback_method,
                                      topic_source='analysis').get(timeout=20)

Unsubscribe by tags
-------------------

The below code shows a example call to unsubscribe_by_tags with a tag query 'ahu AND siteRef="@building1"'.
With haystack model this condition will map to all AHUs in building1. The below code unsubscribes to 'devices' topics
of matching AHUs. For example, "devices/building1/ahu1", "devices/building1/ahu2" etc.

.. code-block:: python

    self.vip.pubsub.unsubscribe_by_tags('pubsub',
                                      'ahu AND siteRef="@building1")',
                                      self.callback_method_ahus).get(timeout=20)

Note: if you had a explicit subscription by topic prefix, for example,
self.vip.pubsub.subscribe('pubsub', "devices/building1/ahu2", self.callback_method_ahu2'), then the method,
callback_method_ahu2, will continue to get called whenever a message is posted to the topic "devices/building1/ahu2".
This is because subscription by topic prefix get precedence over subscription by tags

Publish by tags
---------------

The below code shows a example call to publish_by_tags with a tag query
'point AND air AND temp AND sp AND campusRef="campus1" AND equipRef="device1"'. With haystack model this condition will
map to a dry bulb temperature setpoint point in equipment, device1, that is in campus, campus1. This would equate to a
topic suffix such as "campus1/device1/air-temp-sp". The below code snippet will use the default topic_source, "devices",
and publish to "devices/campus1/device1/air-temp-sp"

.. code-block:: python

    agent.vip.pubsub.publish_by_tags('pubsub',
                                     'point AND air AND temp AND sp AND campusRef="campus1" AND equipRef="device1"',
                                     headers=headers, message=[68.2, {"units": "F"}])


Optional Parameters:
    - topic_source:  prefix to add to the result of tag query to derive topic_name. defaults to "devices"
    - max_publish_count: Maximum number of publishes allowed. publish is a blocking call and maximum number of publishes
      is restricted for performance reasons. Default value=1.

The below code snippet shows a example code with topic_source="analysis" and max_publish_count=2

.. code-block:: python

    agent.vip.pubsub.publish_by_tags('pubsub',
                                     'point AND air AND temp AND sp AND campusRef="campus1" AND equipRef="device1"',
                                     headers=headers, message=[68.2, {"units": "F"}],
                                     topic_source="analysis",
                                     max_publish_count=2)
