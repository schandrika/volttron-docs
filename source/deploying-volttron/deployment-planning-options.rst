.. _Planning-Deployments:

=====================
Planning a Deployment
=====================


The 3 major installation types for VOLTTRON are doing development, doing research using VOLTTRON, and
collecting and managing physical devices.

Development and Research installation tend to be smaller footprint installations. For development, the
data is usually synthetic or copied from another source. The existing documentation covers development
installs in significant detail.

Other deployments will have a better installation experience if they consider certain kinds of questions
while they plan their installation.


Questions
=========

  * Do you want to send commands to the machines ?
  * Do you want to store the data centrally ?
  * How many machines do you expect to collect data from on each "collector" ?
  * How often will the machines collect data ?
  * Are all the devices visible to the same network ?
  * What types of VOLTTRON applications do you want to run ?


Commands
--------

If you wish to send commands to the devices, you will want to install and configure the Volttron Central
agent. If you are only using VOLTTRON to securely collect the data, you can skip install of the extra agents
to reduce the footprint.


Storing Data
------------

VOLTTRON supports multiple historians. Postgresql(with or without timescale support) is the most commonly used.
As you plan your installation, you should consider how quickly you need access to the data and where. If you are looking
at the health and well-being of an entire suite of devices, its likely that you want to do that from a
central location.  Analytics can be performed at the edge by VOLTTRON applications or can be performed
across the data usually from a central data repository.  The latency that you can tolerate in your data
being available will also determine choices in different agents (ForwardHistorian versus Data Mover)


How Many
--------

The ratio of how many devices-to-collector machine is based on several factors. These include:

      * how much memory and network bandwidth the collection machine has.  More = More devices
      * how fast the local storage is can affect how fast the data cache can be written.  Very slow
        storage devices can fall behind

The second half of the "how many" question is how many collector platforms are writing to a single
VOLTTRON platform to store data - and whether that storage is local, remote, big enough, etc.

If you are storing more than moderate amount of data, you will probably benefit from installing
your database on a different machine than your concrete historian machine.

.. note::

    This is contra-indicated if you have a slow network connection between you concrete historian and your database
    machine.

In synthetic testing up to 6 virtual machines hosting 500 devices each (18 points) were easily
supported by a single centralized platform writing to a Mongo database - using a high speed network.
That central platform experienced very little CPU or memory load when the VOLTTRON Central agent was disabled.


How Often
---------

This question is closely related to the last. A higher sampling frequency will create more data.  This
will place more work in the storage phase.


Networks
--------

In many cases, there are constraints on how networks can interact with each other. In many cases,
these include security considerations.  On some sites, the primary network will be protected from less
secure networks and may require different installation considerations.  For example, if a data collector
machine and the database machine are on the same network with sufficient security, you may choose
to have the data collector write directly to the database.  If the collector is on an isolated building
network then you will likely need to use the ForwardHistorian to bridge the two networks.


Other Considerations
--------------------

Physical location and maintenance of collector machines must be considered in all live deployments.
Although the number of data points may imply a heavy load on a data collection box, the physical constraints
may limit the practicality of having more than a single box.  The other side of that discussion is deploying
many collector boxes may be simpler initially, but may create a maintenance challenge if you don't
plan ahead on how you apply patches, etc.

Naming conventions should also be considered.  The ability to trace data through the system and identify
the collector machine and device can be invaluable in debugging and analysis.


.. _Deployment-Options:

Deployment Options
==================

There are several ways to deploy the VOLTTRON platform in a Linux environment. It is up to the user to determine which
is right for them. The following assumes that the platform has already been bootstrapped and is ready to run.


Simple Command Line
-------------------

With the VOLTTRON environment activated the platform can be started simply by running VOLTTRON on the command
line.

::

    $volttron -vv

This will start the platform in the current terminal with very verbose logging turned on. This
is most appropriate for testing Agents or testing a deployment for problems before switching to a
more long term solution. This will print all log messages to the console in real time.

This should not be used for long term deployment. As soon as an SSH session is terminated for whatever reason
the processes attached to that session will be killed. This also will not capture log message to a file.


Running VOLTTRON as a Background Process
----------------------------------------

A simple, more long term solution, is to run volttron in the background and disown it from the current terminal.

.. warning::
    If you plan on running VOLTTRON in the background and detaching it from the
    terminal with the ``disown`` command be sure to redirect stderr and stdout to ``/dev/null``.
    Even if logging to a file is used some libraries which VOLTTRON relies on output
    directly to stdout and stderr. This will cause problems if those file descriptors
    are not redirected to ``/dev/null``.

.. code-block:: bash

    $volttron -vv -l volttron.log > /dev/null 2>&1&

To keep the size of the log under control for more longer term deployments us the rotating log configuration file
``examples/rotatinglog.py``.

.. code-block:: bash

    $volttron -vv --log-config examples/rotatinglog.py > /dev/null 2>&1&

This will start a rotate the log file at midnight and limit the total log data to seven days worth.

The main downside to this approach is that the VOLTTRON platform will not automatically
resume if the system is restarted. It will need to be restarted manually after reboot.

.. _system service setup:

Setting up VOLTTRON as a System Service
---------------------------------------


Systemd
^^^^^^^

The below code block for systemd cas be used as a starting point for setting up VOLTTRON as a service. Note that as
this will redirect all the output that would be going to stdout - to the syslog.  This can be accessed using
`journalctl`.  For systems that run all the time or have a high level of debugging turned on, we recommend checking
the system's logrotate settings.

.. code-block:: console

    [Unit]
    Description=VOLTTRON Platform Service
    After=network.target

    [Service]
    Type=simple

    #Change this to the user that VOLTTRON will run as.
    User=volttron
    Group=volttron

    #Uncomment and change this to specify a different VOLTTRON_HOME
    #Environment="VOLTTRON_HOME=/home/volttron/.volttron"

    #Change these to settings to reflect the install location of VOLTTRON
    WorkingDirectory=/var/lib/volttron
    ExecStart=/var/lib/volttron/env/bin/volttron -vv
    ExecStop=/var/lib/volttron/env/bin/volttron-ctl shutdown --platform


    [Install]
    WantedBy=multi-user.target

After the script has been modified to reflect the setup of the platform you can install it with the
following commands. These need to be run as root or with sudo as appropriate.

.. code-block:: console

    #Copy the service file into place
    cp <file containing above script. ex. /home/user1/volttron.service> /etc/systemd/system/volttron.service

    #Set the correct permissions if needed
    chmod 644 /etc/systemd/system/volttron.service

    #Notify systemd that a new service file exists (this is crucial!)
    systemctl daemon-reload

    #Start the service
    systemctl start volttron.service


Init.d
^^^^^^

The below script can be used as a starting point for setting up VOLTTRON as a service on init.d based systems.

.. code-block:: bash

    #! /bin/sh
    ### BEGIN INIT INFO
    # Provides:          volttron
    # Required-Start:    $remote_fs $syslog
    # Required-Stop:     $remote_fs $syslog
    # Should-Start:      $network $named
    # Should-Start:      $network $named
    # Default-Start:     2 3 4 5
    # Default-Stop:      0 1 6
    # Short-Description: VOLTTRON (TM) Daemon
    # Description:       VOLTTRON (TM) agent execution platform.
    ### END INIT INFO

    # Author: Brandon Carpenter <brandon.carpenter@pnnl.gov>

    # Do NOT "set -e"

    # PATH should only include /usr/* if it runs after the mountnfs.sh script
    PATH=/sbin:/usr/sbin:/bin:/usr/bin
    DESC="VOLTTRON (TM) agent execution platform"
    NAME=volttron

    # Change this to the user VOLTTRON will run as.
    USER=volttron

    # Change this to path to volttron executable. For example, <path to venv>/bin/
    VOLTTRON_EXE_PATH=/my/venv dir/path/bin

    # Update VOLTTRON_HOME path as needed
    VOLTTRON_HOME=/home/volttron/.volttron

    DAEMON=$VOLTTRON_EXE_PATH/$NAME
    DAEMON_ARGS="-v -l $VOLTTRON_HOME/volttron.log"
    PIDFILE=/var/run/$NAME.pid
    SCRIPTNAME=/etc/init.d/$NAME

    export VOLTTRON_HOME=$VOLTTRON_HOME

    # Exit if the package is not installed
    [ -x "$DAEMON" ] || exit 0

    # Read configuration variable file if it is present
    [ -r /etc/default/$NAME ] && . /etc/default/$NAME

    # Load the VERBOSE setting and other rcS variables
    . /lib/init/vars.sh

    # Define LSB log_* functions.
    # Depend on lsb-base (>= 3.2-14) to ensure that this file is present
    # and status_of_proc is working.
    . /lib/lsb/init-functions


    setup_cgroups()
    {
      CGROUP=/sys/fs/cgroup
      if ! mountpoint -q $CGROUP; then
        mkdir -p $CGROUP
        mount -t tmpfs cgroup $CGROUP
      fi
      if ! mountpoint -q $CGROUP/cpu; then
        mkdir $CGROUP/cpu
        mount -t cgroup -o cpu cgroup-cpu $CGROUP/cpu
      fi
      if ! mountpoint -q $CGROUP/memory; then
        mkdir $CGROUP/memory
        mount -t cgroup -o memory cgroup-memory $CGROUP/memory
      fi
      [ -d $CGROUP/cpu/volttron ] || mkdir $CGROUP/cpu/volttron
      [ -d $CGROUP/memory/volttron ] || mkdir $CGROUP/memory/volttron
      chgrp volttron $CGROUP/cpu/volttron $CGROUP/memory/volttron
      chmod 775 $CGROUP/cpu/volttron $CGROUP/memory/volttron
    }

    #
    # Function that starts the daemon/service
    #
    do_start()
    {
      # Return
      #   0 if daemon has been started
      #   1 if daemon was already running
      #   2 if daemon could not be started
      #setup_cgroups
      start-stop-daemon --start --quiet --pidfile $PIDFILE --exec $DAEMON --test > /dev/null || return 1
      start-stop-daemon --start --quiet --pidfile $PIDFILE --exec $DAEMON --background --make-pidfile --chuid $USER -- $DAEMON_ARGS || return 2
    }

    #
    # Function that stops the daemon/service
    #
    do_stop()
    {
      # Return
      #   0 if daemon has been stopped
      #   1 if daemon was already stopped
      #   2 if daemon could not be stopped
      #   other if a failure occurred
      start-stop-daemon --stop --quiet --retry=INT/30/KILL/5 --pidfile $PIDFILE --name $NAME
      RETVAL="$?"
      [ "$RETVAL" = 2 ] && return 2
      start-stop-daemon --stop --quiet --oknodo --retry=0/30/KILL/5 --exec $DAEMON
      [ "$?" = 2 ] && return 2
      # Many daemons don't delete their pidfiles when they exit.
      rm -f $PIDFILE
      return "$RETVAL"
    }

    case "$1" in
      start)
      [ "$VERBOSE" != no ] && log_daemon_msg "Starting $DESC" "$NAME"
      do_start
      case "$?" in
        0|1) [ "$VERBOSE" != no ] && log_end_msg 0 ;;
        2) [ "$VERBOSE" != no ] && log_end_msg 1 ;;
      esac
      ;;
      stop)
      [ "$VERBOSE" != no ] && log_daemon_msg "Stopping $DESC" "$NAME"
      do_stop
      case "$?" in
        0|1) [ "$VERBOSE" != no ] && log_end_msg 0 ;;
        2) [ "$VERBOSE" != no ] && log_end_msg 1 ;;
      esac
      ;;
      status)
      status_of_proc "$DAEMON" "$NAME" && exit 0 || exit $?
      ;;
      restart|force-reload)
      #
      # If the "reload" option is implemented then remove the
      # 'force-reload' alias
      #
      log_daemon_msg "Restarting $DESC" "$NAME"
      do_stop
      case "$?" in
        0|1)
        do_start
        case "$?" in
          0) log_end_msg 0 ;;
          1) log_end_msg 1 ;; # Old process is still running
          *) log_end_msg 1 ;; # Failed to start
        esac
        ;;
        *)
        # Failed to stop
        log_end_msg 1
        ;;
      esac
      ;;
      *)
      echo "Usage: $SCRIPTNAME {start|stop|status|restart|force-reload}" >&2
      exit 3
      ;;
    esac

    :


Minor changes may be needed for the file to work on the target system. Specifically
the ``USER``, ``VOLTTRON_EXE_PATH``, and ``VOLTTRON_HOME`` variables may need to be changed.


The script can be installed with the following commands.  These need to be run as root or with `sudo` as appropriate.

.. code-block:: console

    #Copy the script into place
    cp <path to above script. for example. /home/user1/volttron> /etc/init.d/volttron

    #Make the file executable
    chmod 755 /etc/init.d/volttron

    #Change the owner to root
    chown root:root /etc/init.d/volttron

    #These will set it to startup automatically at boot
    update-rc.d volttron defaults

    #Start the service
    /etc/init.d/volttron start
