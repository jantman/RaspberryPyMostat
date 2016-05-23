Planning
========

|Project Status: Concept - Minimal or no implementation has been done
yet.|

A python-based intelligent home thermostat, targeted at (but not
requiring) the RaspberryPi and similar small computers. (Originally
"RaspberryPyMostat", for 'RaspberryPi Python Thermostat', but that's too
long to reasonably name a Python package).

Especially since the introduction of the `Nest
thermostat <http://en.wikipedia.org/w/index.php?title=Nest_Labs&redirect=no>`__,
a lot of people have attempted a project like this. I'd like to think
that mine is different - perhaps more polished, perhaps it stores
historical data in a real, logical way. Multiple temperatures are nice,
and the pluggable scheduling and decision engines are something I
haven't seen in any others yet. The completely open API, and the fact
that some of the out-of-the-box components use it is new too. And after
looking at some of the options out there, I think the idea of it being
packaged and distributed properly is pretty novel too, as are my hopes
for a platform-agnostic system; a lot of the options out there are
really hardware-hacking projects, and I want to make software that works
with as many hardware options as it can. But when it comes down to it,
this is an idea that I tried `a long time
ago <https://github.com/jantman/tuxostat>`__ and never finished, and
want to have another try at regardless of whether it does something
unique or becomes just another one of the hundred pieces of software
that do the same thing. I'm also going to be playing with some
technology that I've never used before, so for me this is as much about
learning and exploring as it is about producing a polished final
codebase.

See:

-  `Architecture.md <Architecture.md>`__ for an overview of the
   architecture, and most of the documentation that currently exists.
-  `DISCOVERY.md <DISCOVERY.md>`__ for some information on service
   discovery
-  `TWISTED.md <TWISTED.md>`__ for some docs on using Twisted for this

ToDo
----

1.  get a very basic framework of an app, with HTTP, DB access, and some
    signals that also hit the DB - just a skeleton
2.  get complete test coverage for it
3.  add in the discovery broadcast and some timers
4.  complete coverage
5.  logging
6.  start the sphinx docs - make sure code docs work, and then just
    document-as-I-go the rest; figure out nomenclature for everything
7.  figure out how to document the API
8.  more code, get at least some stuff working with integration testing
9.  Puppet module to install it (and dependencies?), Vagrant machine for
    testing
10. run it on an RPi
11. integration and functional tests
12. working prototype
13. temperature and relay devices
14. quick-and-dirty web interface in Flask

Features
--------

Features planned for the initial release:

-  Flexible rules-based scheduling. This can include cron-like schedules
   (do X at a given time of day, or time of day on one or more days of
   week, etc.), one-time schedule overrides ("I'm going to be away from
   December 21st to 28th this year, just keep the temperature above Y"),
   or instant adjustments ("make the temperature X degress NOW", in the
   web UI). The most specific schedule wins. Inital scheduling will
   support some mix of what can be represented by `ISO8601 time
   intervals <http://en.wikipedia.org/wiki/ISO_8601#Time_intervals>`__
   and `cron
   expressions <http://en.wikipedia.org/wiki/Cron#CRON_expression>`__.
-  Data on current and desired temperature(s) and heating/cooling state
   will be collected. This should allow the scheduling engine to build
   up historical data on how long it takes to heat or cool one degree at
   a given temperature, and should allow us to trigger heating/cooling
   to reach the scheduled temperature at the scheduled time (as opposed
   to starting the heating/cooling at the scheduled time).
-  Support for N temperature sensors, and scheduling based on them; i.e.
   set a daytime target temperature based on the temperature of your
   office, and a nighttime target based on the temperature in the
   bedroom.
-  Web UI with robust mobile support. Ideally, the entire system should
   be configurable by a web UI once it's installed (which should be done
   with a Puppet module).
-  I don't plan on supporting physical controls (screen and buttons on
   the wall) any time soon; in practice, I'm always closer to a laptop,
   tablet or phone than I am to that one out-of-the-way spot on the
   wall.
-  Everything AGPL 3.0.
-  Ability to set schedules using a specific algorithm (plug-in
   architecture) and one or more specified temperature inputs.
-  Scheduling and decision (system run) implemented in plugins
   (packages, `entry
   points <http://pythonhosted.org/setuptools/setuptools.html#dynamic-discovery-of-services-and-plugins>`__)
   that use a defined API; some way of reflecting this in the Web UI
   (maybe this should come over the master API). Initially just
   implement scheduling as described above and setting temperature based
   on one temp input; subsequent plugins could include averaging across
   multiple inputs, weighted average, and predictive on/off cycles
   (including outside temperature input).
-  Historical data stored in some time-series database; should include
   all temperature values at the beginning of a run, and every X minutes
   during a run.
-  Everything should be modular.
-  Support running all on one RPi, or splitting components apart; should
   support as many OSes as possible. Support for smaller devices as
   temperature sensors would be nice.

Reference Implementation
------------------------

My planned reference implementation of the system is:

-  RaspberryPi physical control unit - USB relay output for control, and
   a temperature sensor, connecting via WiFi.

   -  `DS18B20 <https://www.sparkfun.com/products/245>`__ temperature
      sensor using GPIO
   -  For system control, either a
      `PiFace <https://www.sparkfun.com/products/11772>`__ or a
      `Phidgets
      1014 <http://www.phidgets.com/products.php?product_id=1014>`__ USB
      4 relay kit, both of which I already have.

-  RaspberryPi temperature sensor in another room, connecting via WiFi.

   -  `DS18B20 <https://www.sparkfun.com/products/245>`__ temperature
      sensor using GPIO

-  Master control process, web UI and a third temperature input on my
   desktop computer.

   -  `DS18S20 <https://www.sparkfun.com/products/retired/8366>`__
      temperature sensor connected via
      `DS9490R <http://www.maximintegrated.com/en/products/comms/ibutton/DS9490R.html>`__
      usb-to-1-wire adapter

Relevant Links
--------------

-  https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/temperature/
-  https://www.adafruit.com/product/1012
-  http://www.projects.privateeyepi.com/home/temperature-gauge
-  http://m.instructables.com/id/Raspberry-Pi-Temperature-Humidity-Network-Monitor/
-  `serial\_device2 <https://pypi.python.org/pypi/serial_device2/1.0>`__
   - Extends serial.Serial to add methods such as auto discovery of
   available serial ports in Linux, Windows, and Mac OS X
-  `pyusbg2 <https://pypi.python.org/pypi/pyusbg2>`__ - PyUSB offers
   easy USB devices communication in Python. It should work without
   additional code in any environment with Python >= 2.4, ctypes and an
   pre-built usb backend library (currently, libusb 0.1.x, libusb 1.x,
   and OpenUSB).

Some Technical Bits and Questions
---------------------------------

-  Sphinx and ReadTheDocs for docs (should start on this sooner rather
   than later).
-  TravisCI and pytest for testing. Might need to look into the special
   cases if we do a lot of threading, or use Twisted.
-  Web UI will probably use Flask, **TODO:** but I need to figure out
   how easy it is to get that to just wrap an API.
-  Assuming we're going with the API-based model, unit tests should be
   simple. Integration and acceptance tests are another question.
-  **TODO:** How to test the API server and client?
-  **TODO:** How to test the separate services, in isolation from the
   server?
-  just a concern for testing the API client. this should be simple
   enough.
-  **TODO:** Try to find a strong unit testing framework for the web UI;
   we can deal with integration/acceptance testing later.
-  `pytest-flask <https://pypi.python.org/pypi/pytest-flask>`__ looks
   like it should handle things quite well
-  **TODO:** Is there any way that we can generate (dynamically? code
   generation?) the API server and client? The web UI? Is there an
   existing web UI "thing" to just wrap a ReST API? Would this help
   testing?
-  I know some of the python API clients I've worked with do this... I
   just need to figure out how, because it's an area I've never really
   looked into.
-  Not sure how to handle this programmatically, as most ReST API tools
   are built to be part of a web application, which this isn't.
-  `Flask API <https://github.com/tomchristie/flask-api>`__ looks OK but
   development seems to have stopped and there are many issues
-  `Restless <https://github.com/toastdriven/restless>`__ a generic ReST
   "miniframework", intended for Python web frameworks
-  A quick `Flask ReST API
   tutorial <http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask>`__
   `and another <http://blog.luisrei.com/articles/flaskrest.html>`__
-  `eve <http://python-eve.org/>`__ a "ReST API framework in a box"
   using Flask, MongoDB and Redis.
-  `Flask-restful <https://github.com/flask-restful/flask-restful>`__
   and its
   `quickstart <http://flask-restful.readthedocs.org/en/latest/quickstart.html>`__
-  `raml <http://raml.org/>`__ - RESTful API Modeling Language
-  `architecting version-less
   APIs <http://urthen.github.io/2013/05/16/ways-to-version-your-api-part-2/>`__
-  Maybe a lot of this should use message queues instead of HTTP APIs.
   But we'd need a message broker, and AFAIK few of them are lightweight
   (though Celery supports Redis, RabbitMQ, or using MongoDB or
   SQLAlchemy).
-  **TODO:** How do I do acceptance/integration testing with service
   discovery if I have this running (like, in my house) on my LAN? Just
   use some "system number" variable?
-  The main process will likely have to have a number of threads: API
   serving (ReST API), timer/cron for scheduling and comparing temp
   values to thresholds, main thread (am I missing anything?)
-  Should we use `Twisted <https://twistedmatrix.com/trac/>`__?
-  If so, can we use pytest for it (unit tests)? looks like yes -
   `pytest-twisted <https://github.com/schmir/pytest-twisted>`__,
   `pytest
   docs <http://pytest.org/latest/faq.html#how-does-pytest-relate-to-twisted-s-trial>`__,
   `twisted's testing
   docs <https://twistedmatrix.com/documents/14.0.0/core/howto/trial.html>`__
   which focus on their unittest-like
   `trial <http://twistedmatrix.com/trac/wiki/TwistedTrial>`__ framework
   (`also
   this <http://twistedmatrix.com/documents/14.0.0/core/development/policy/test-standard.html>`__),
   a `random blog
   post <http://www.mechanicalcat.net/richard/log/Python/Tips_for_Testing_Twisted>`__
   on testing Twisted without Trial.
-  Should we just do threading ourselves? If so, is there anything to
   help with the API?
-  How do we do integration tests?
-  Flask `might <http://stackoverflow.com/a/22900255/211734>`__ be able
   to do this, but `this <http://stackoverflow.com/a/24101692/211734>`__
   implies otherwise. It supports celery `but as a separate
   process <http://flask.pocoo.org/docs/0.10/patterns/celery/>`__.
-  Twisted `Klein <http://klein.readthedocs.org/en/latest/>`__ might be
   the union of what I need; here's `a
   tutorial <http://tavendo.com/blog/post/going-asynchronous-from-flask-to-twisted-klein/>`__.
-  Temperature and control daemons can probably be single-threaded, the
   logic there is pretty simple. Timeouts should do all we need.
-  `bottle <http://bottlepy.org/docs/dev/index.html>`__ might be a
   simple option
-  Web UI can just be a normal webapp, all it does is provide a
   graphical interface to the decision engine API
-  **TODO:** what database to use?
-  Mongo? `MongoEngine <http://mongoengine.org/>`__ (mongo "orm")
-  Scheduling
-  implement it from scratch?
-  Crazy thought: maybe adding an API onto the decision engine process
   is a bad idea. Maybe I should think a little less "tiny system" -
   maybe some sort of message queue is the right idea, or we should have
   a "main process" that simply stores data and provides a ReST API (and
   maybe the Web UI too?) and have a scheduling engine that's a separate
   thing?

What the Processes Need to Do
-----------------------------

Web UI
~~~~~~

Just provide a pretty (or usable) wrapper around the decision engine
API. Honestly I'd love it if this could be generated entirely
dynamically - i.e. the decision engine's plugins know about some input
data types, and the web UI knows how to render them. The web UI is just
a pile of components, and pulls information about what it needs
dynamically from the decision engine. That's really complicated to
implement, but OTOH, I'm not sure how else we allow pluggable scheduling
and decision modules.

Temperature Sensors
~~~~~~~~~~~~~~~~~~~

Dead-simple:

1. Process starts up, uses service discovery to find the decision
   engine.
2. Registers itself with some sort of unique ID (hardware UUID,
   RaspberryPi serial number, etc.)
3. Discovers available temperature sensors, and some sort of unique
   (never-changing) ID for each.
4. Reads values from sensors, POST to decision engine API.
5. Repeat #4 indefinitely. (if connection to decision engine goes away,
   start back at #1).

Relay/Physical Control Unit
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Also dead-simple:

1. Process starts up, uses service discovery to find the decision
   engine.
2. Registers itself with some sort of unique ID (hardware UUID,
   RaspberryPi serial number, etc.)
3. Discovers available relay outputs and their states, assigns a unique
   ID to each.
4. POST this information to the decision engine.
5. Start a web server.
6. Wait for an API request from the decision engine, which is either a
   GET (current status) or POST (set state).

Decision Engine / Master Control Process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here's where the complexity lies.

-  Run a web server for the ReST API used by the other services
   (including the Web UI).
-  Maintain database of all configuration and settings; versioning and
   ORM?
-  Ability to store configuration to push to other daemons (like
   temperature polling rate).
-  Keep (time-series?) database of historical data on temperature,
   system state, etc. (including data required for predictive system
   operation)
-  Determine the current and next (N) schedules.
-  Constantly (every N seconds) compare temperature data to current
   schedule and operate system accordingly
-  Re-read schedules whenever a change takes place
-  Show end-user current system state and upcoming schedules
-  Provide a plugin interface for schedule algorithms
-  Provide a plugin interface for decision (system run/stop) algorithms
-  Support third-party web UIs via its API, which needs to include
   support for the plug-in scheduling and decision algorithms (which
   exist only in this process, not the web UI)
-  Support versioning of ReST and internal APIs

From a threading or work-oriented model, this boils down to:

1. Main thread
2. ReST API
3. Database(s)?
4. Schedule determination and temperature evaluation (these could be
   triggered events based on a timer or some action/signal)

Twisted supports scheduling/timeouts/repeating events, which seems like
it could handle quite a bit of this.

Framework Considerations
------------------------

There are essentially two options (aside from doing it all from scratch)
that appear obvious:

1. An async/event processing framework (Twisted) with ReST bolted on
2. A web framework with async/event processing bolted on

The main concerns/evaluation points that I can think of:

-  ReST API serving (data to/from the database, and shared/main thread
   memory)
-  Signals or some other sort of notification mechanism
-  Scheduled tasks
-  Database access from multiple threads (whatever we use as a
   datastore, and whatever we use as a TSDB)
-  test-ability (i.e. pytest, possibly something else to test the
   threading/network)

Datastore
---------

NoSQL or document-object sounds good, since for the most part we're
storing simple objects, but they may have arbitrary properties
(plugins). And schema migrations are a pain. But I'm not sure how these
work on tiny systems; Mongo is the most popular, but it's certainly not
geared towards one node with a small amount of memory and CPU (and
disk).

I'm leaning towards Mongo, which some people say they have running on
the RPi but I'm not sure about performance (the RPi is about as far from
the target usage of Mongo as you can get):

-  `Emerson's Site \| MongoDB + Raspberry Pi (without building
   anything!) <https://emersonveenstra.net/mongodb-raspberry-pi/>`__
-  `Raspberry Pi MongoDB Installation – The working guide! -
   Hardware\_Hacks <http://c-mobberley.com/wordpress/2013/10/14/raspberry-pi-mongodb-installation-the-working-guide/>`__
   - build from source on RPi
-  `heimcontrol.js - Home automation in Node.js with Raspberry PI and
   Arduino <https://ni-c.github.io/heimcontrol.js/get-started.html>`__ -
   source or some guy's 2.1.1 package
-  `ArduPi/mongodb-rpi at master ·
   brice-morin/ArduPi <https://github.com/brice-morin/ArduPi/tree/master/mongodb-rpi>`__
-  `Installing mongodb on Raspberry Pi (using pre-compiled binaries) -
   Jonas
   Widriksson <http://www.widriksson.com/install-mongodb-raspberrypi/>`__
-  `skrabban/mongo-nonx86 <https://github.com/skrabban/mongo-nonx86>`__
   - SPARC/ARM port of Mongo, but only 2.1.1
-  `SERVER-1811 ARM support -
   MongoDB <https://jira.mongodb.org/browse/SERVER-1811>`__ - updated
   August 2014 with status, sounds like a long time coming
-  `Packages \| Arch Linux
   ARM <http://archlinuxarm.org/packages?search=mongodb>`__ - ArchLinux
   ARM has supposedly-working mongodb 2.6.6-1 and pymongo 2.7.2 packages
-  `mongoDB 2.6 and Node.js 0.10.29 on Raspberry
   Pi <http://andyfelong.com/2014/07/mongodb-2-6-and-nodejs-10-29-on-raspberry-pi-oh-joy/>`__
   - the old 2.1 stuff doesn't work on the Pi B+; the Arch packages work
   fine

TSDB
----

We want to store historical data on temperatures, runs, etc. Initially
we can just use something simple, but we'll probably want to find a
good, optimized storage for this.

Packaging
---------

`qwcode <https://github.com/qwcode>`__ suggested using one repository
and setuptools extras. I did some tests to make sure ``pip`` supports
them correctly.

Using the default ``pip`` on my machine, I had some issues. However, if
I upgraded to the latest ``pip`` (6.0.3 at this time), most common
requirement patterns worked fine:

-  ``projectname[extra]``
-  ``projectname[extra]>=X.Y.Z``
-  ``projectname[extra] <massive version spec here, like: ">0.0.3,<0.0.6,!=0.0.4">``
-  ``[-e] (git+git|git+https)://url#egg=projectname[extra]``
-  ``[-e] (git+git|git+https)://url@<hash or branch or tag>#egg=projectname[extra]``
-  ``-e /path/to/local/git/clone/of/projectname[extra]``

The only supported specifiers that don't seem to handle installing the
extras are:

-  ``/path/to/local/git/clone/of/projectname[extra]`` (note, without
   ``-e``)
-  ``file:///path/to/archive/of/project.zip[extra]``

**Question:** will this work with multiple extras? (i.e.
``[hub,sensor,control]``)

So, with this, my plan is going to be:

-  ``rpymostat`` - central, shared code and the decision engine ("hub"?)
-  install as ``rpymostat[hub]`` (or via requirements files) for the hub
   dependencies
-  ``rpymostat-webui`` - separate repo, separate distribution
-  ``rpymostat-sensor`` - separate repo, separate distribution
-  ``rpymostat-relays`` - separate repo, separate distribution

I haven't yet decided if I'm going to use `namespace
packages <http://pythonhosted.org/setuptools/setuptools.html#namespace-packages>`__.
That would be more logical and elegant (i.e. ``rpymostat.sensor``
instead of ``rpymostat_sensor``). My only reservation is if I'm claiming
to have a pluggable architecture (i.e. the sensor, relay or web UI can
be replaced with a third party one that just respects our API), maybe
these things should be relatively separate in order to promote that?

That Temperature Thing
----------------------

Yup, I've got a million links and they're all about system architecture
and frameworks and implementation details, and nothing about what this
thing actually does. So here's some links:

-  `Raspberry Pi Thermostat Part 1: System Overview - The
   Nooganeer <http://www.nooganeer.com/his/projects/homeautomation/raspberry-pi-thermostat-part-1-overview/>`__
-  `Willseph/RaspberryPiThermostat <https://github.com/Willseph/RaspberryPiThermostat>`__
-  `python - Thermostat Control Algorithms - Stack
   Overflow <http://stackoverflow.com/questions/8651063/thermostat-control-algorithms>`__
-  `VE2ZAZ - Smart Thermostat on the Raspberry
   Pi <http://ve2zaz.net/RasTherm/RasTherm.htm>`__
-  `Raspberry Pi • View topic - Web enabled thermostat
   project <http://www.raspberrypi.org/forums/viewtopic.php?f=37&t=24115>`__
-  `Rubustat - the Raspberry Pi Thermostat \| Wyatt Winters \| Saving
   the world one computer at a
   time <http://wyattwinters.com/rubustat-the-raspberry-pi-thermostat.html>`__
-  `Makeatronics: Raspberry Pi Thermostat
   Hookups <http://makeatronics.blogspot.com/2013/04/raspberry-pi-thermostat-hookups.html>`__
-  `Makeatronics: Thermostat
   Software <http://makeatronics.blogspot.com/2013/04/thermostat-software.html>`__

.. |Project Status: Concept - Minimal or no implementation has been done yet.| image:: http://www.repostatus.org/badges/0.1.0/concept.svg
   :target: http://www.repostatus.org/#concept

RPyMostat Similar Projects
--------------------------

-  `Willseph/RaspberryPiThermostat: A Raspberry Pi-powered smart
   thermostat written in Python and
   PHP. <https://github.com/Willseph/RaspberryPiThermostat>`__ - Python
   sensors and control but PHP LAMP web UI. MIT license. Looks like it's
   got a good bit of information, especially on wiring/setup and photos
   of the install on `Imgur <http://imgur.com/gallery/YxElS>`__.
-  `ianmtaylor1/thermostat: Raspberry Pi Thermostat
   code <https://github.com/ianmtaylor1/thermostat>`__ - Python project
   that reads 1-wire temps and uses SQLAlchemy. Relatively simple beyond
   that.
-  `chaeron/thermostat: Raspberry Pi
   Thermostat <https://github.com/chaeron/thermostat>`__ - Fairly nice
   touchscreen UI and pretty complete, but one untested python file and
   only one physical piece.
-  `mharizanov/ESP8266\_Relay\_Board: Three Channel WiFi
   Relay/Thermostat
   Board <https://github.com/mharizanov/ESP8266_Relay_Board>`__ -
   firmware source code and hardware designs for a WiFi relay/thermostat
   board. Probably won't use this, but interesting.
-  `mdarty/thermostat: Raspberry Pi Thermostat
   Controller <https://github.com/mdarty/thermostat>`__ - python/flask
   app for a Python RPi thermostat.
-  `tom91136/thermostat: A simple thermostat for RaspberryPi written in
   Python <https://github.com/tom91136/thermostat>`__ - Another Flask,
   DS18B20 thermostat with GPIO relays.
-  `jeffmcfadden/PiThermostat: Build a Raspberry Pi
   Thermostat <https://github.com/jeffmcfadden/PiThermostat>`__ - Rails
   app for an RPi thermostat.
-  `Forever-Young/thermostat-web: Django application for thermostat
   control <https://github.com/Forever-Young/thermostat-web>`__ -
   single-host
-  `wywin/Rubustat: A thermostat controller for Raspberry Pi on
   Flask <https://github.com/wywin/Rubustat>`__
-  `tommybobbins/PiThermostat: Raspberry Pi, TMP102 and 433 Transmitter
   to make an Redis based Central heating
   system <https://github.com/tommybobbins/PiThermostat>`__ -
   Redis-based system using Google Calendar for scheduling
-  `jpardobl/django-thermostat: Django app to control a
   heater <https://github.com/jpardobl/django-thermostat>`__
-  `tinkerjs/Pi-Thermostat: A Raspberry Pi based
   thermostat <https://github.com/tinkerjs/Pi-Thermostat>`__ - Python
   and RPi, but single-host. `Blog
   post <http://technicalexplorer.blogspot.com/2015/08/the-thermostat.html>`__
   has some nice diagrams, pictures, and information on HVAC systems.
-  `cakofony/thermostat: Web enabled thermostat project to run on the
   raspberry pi. <https://github.com/cakofony/thermostat>`__ - Python,
   includes support for an Adafruit character LCD display.
-  `Raspberry Pi Thermostat Part 1: System Overview - The
   Nooganeer <http://www.nooganeer.com/his/projects/homeautomation/raspberry-pi-thermostat-part-1-overview/>`__
   - nice web UI demo
-  `VE2ZAZ - Smart Thermostat on the Raspberry
   Pi <http://ve2zaz.net/RasTherm/RasTherm.htm>`__ - Flask UI
-  `openHAB <http://www.openhab.org/>`__ - JVM-based, vendor-agnostic
   home automation "hub". Includes web UI. Rule creation appears to be
   via a Java UI though.
-  `home-assistant/home-assistant: Open-source home automation platform
   running on Python
   3 <https://github.com/home-assistant/home-assistant>`__ - Python3
   home automation server with web UI. Looks like it could be really
   interesting, but not sure how much support it has for the advanced
   scheduling I want.
-  `WTherm – a smart thermostat \|
   NiekProductions <http://niekproductions.com/p/wtherm/>`__ - Arduino,
   PHP but has some good concepts.
-  `Home \| pimatic - smart home automation for the raspberry
   pi <https://pimatic.org/>`__ - node.js home automation framework.
   Once again, doesn't have support for the kind of scheduling I want.
-  `Matt Brenner / PyStat ·
   GitLab <https://gitlab.com/madbrenner/PyStat>`__ - multi-threaded
   Ptrhon thermostat; Flask, RPi.
   `screenshots <http://imgur.com/a/7vkZO>`__. Looks nice, but doesn't
   seem to have the type of scheduling I want, and runs as a single
   process/single host.

Other Notes
-----------

-  `sphinxcontrib.httpdomain — Documenting RESTful HTTP APIs —
   sphinxcontrib-httpdomain 1.4.0
   documentation <https://pythonhosted.org/sphinxcontrib-httpdomain/>`__
-  packaging - one repo/package per component
-  docs - how? working theory is main RPyMostat repo (which contains the
   main engine itself) has its own sphinx docs, but also installs the
   other dependencies and produces docs for them? Or maybe we build
   sphinx docs for each repo itself, but then we also have a alldocs
   task in the master repo that builds docs for ALL of the packages, and
   pushes them somewhere? Or maybe we just rely on sphinx mappings to
   link as needed...
-  Wall mount tablet for the UI? There's some
   `cheap <http://www.amazon.com/s/ref=sr_st_price-asc-rank?lo=computers&rh=n%3A172282%2Cn%3A!493964%2Cn%3A541966%2Cn%3A13896617011%2Cn%3A1232597011%2Cp_n_operating_system_browse-bin%3A3077590011&qid=1463663130&sort=price-asc-rank>`__
   ones, and `AutoStart - No root - Android Apps on Google
   Play <https://play.google.com/store/apps/details?id=com.autostart&hl=en>`__
   to autostart an app (browser) at boot...
- visual schedule overlay like PagerDuty
- web UI is just an API client
- heuristic algorithm to track every HVAC run, how long it takes to get from one temp to another, inside and outside temps, time of day, maybe also day or night/how long from sunrise or sunset; build database to determine how early to start to reach desired temp
- schedules and overrides
- schedules have start and end time, that are cron-like
- overrides have a specific start time, and end time that's either specific (input can be a specific datetime, or a duration) or when the next schedule starts
- backend - when a schedule or override is input, backend recalculates the next X hours of instructions (schedule with overrides applied), caches them, makes them accessible via API
- schedules and overrides
- API - CRUD for schedules/overrides, get instructions, get current state, get sensor state, name sensors
- default temperature thresholds (how much over/under to trigger/overshoot and how often to run)
- schedules/overrides have temperature targets and thresholds - which sensors to look at, how to weight them. Can be a "simple" input (look at only one sensor, one target temp) or a weighted combination. Can save a default calculation method/sensor weighting.
- make sure we don't start/stop the system too often
- Wall mount touchscreens:
  - https://www.adafruit.com/products/1892
  - https://www.adafruit.com/products/2033
  - https://www.adafruit.com/products/2534
  - https://www.adafruit.com/products/2260
  - Could just use an old phone for now... or set it up somewhere on a bookcase or table...
  - https://blog.adafruit.com/2014/09/05/wall-mounted-touchscreen-raspberry-pi-home-server-piday-raspberrypi-raspberry_pi/
  - http://www.neosecsolutions.com//products.php?62&cPath=21
  - http://www.modmypi.com/blog/raspberry-pi-7-touch-sreen-display-case-assembly-instructions
  - http://www.thingiverse.com/thing:1082431
  - http://www.thingiverse.com/thing:1034194
  - https://www.element14.com/community/docs/DOC-78156/l/raspberry-pi-7-touchscreen-display
- Pi3 Model B - $35-40 - - https://www.raspberrypi.org/products/raspberry-pi-3-model-b/
  - wifi (2.4GHz 802.11n??? - might need USB?)
  - USB
  - GPIO
  - HDMI
  - DSI display interface
- Pi Zero - https://www.raspberrypi.org/products/pi-zero/ - sold out everywhere :(
  - Mini HDMI
  - USB On-The-Go
  - MicroUSB power
  - HAT-compatible 40-pin header
  - onboard wifi hack: https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=127449
  - starter kit - https://www.adafruit.com/products/2816
  - would need USB WiFi dongle and GPIO sensors
- RPi DS18B20
  - https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/temperature/
  - https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/hardware
  - http://www.modmypi.com/blog/ds18b20-one-wire-digital-temperature-sensor-and-the-raspberry-pi
  - https://www.raspberrypi.org/forums/viewtopic.php?t=54238&p=431812

Other Hardware
--------------

-  `Miniature WiFi 802.11b/g/n Module: For Raspberry Pi and more ID: 814
   - $11.95 : Adafruit Industries, Unique & fun DIY electronics and
   kits <https://www.adafruit.com/products/814>`__
-  `USB WiFi 802.11b/g/n Module: For Raspberry Pi and more ID: 1012 -
   $12.95 : Adafruit Industries, Unique & fun DIY electronics and
   kits <https://www.adafruit.com/product/1012>`__
-  `Assembled Pi Cobbler Plus - Breakout Cable for Pi B+/A+/Pi 2/Pi 3
   ID: 2029 - $6.95 : Adafruit Industries, Unique & fun DIY electronics
   and kits <https://www.adafruit.com/products/2029>`__
-  `Assembled Pi T-Cobbler Plus - GPIO Breakout for RasPi A+/B+/Pi 2/Pi
   3 ID: 2028 - $7.95 : Adafruit Industries, Unique & fun DIY
   electronics and kits <https://www.adafruit.com/products/2028>`__
-  `GPIO Header for Raspberry Pi A+/B+/Pi 2/Pi 3 2x20 Female Header ID:
   2222 - $1.50 : Adafruit Industries, Unique & fun DIY electronics and
   kits <https://www.adafruit.com/products/2222>`__
-  `0.1 2x20-pin Strip Right Angle Female Header ID: 2823 - $1.50 :
   Adafruit Industries, Unique & fun DIY electronics and
   kits <https://www.adafruit.com/products/2823>`__
