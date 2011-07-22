Introduction
============

``python-magnatune`` provides a simple command line utility called ``magnatune`` that can be used to search the `magnatune`_ database and get the streaming urls.

For example, to get all the albums from Curl ::

    magnatune --artist Curl

To get the streaming urls of all songs from Curl ::

    magnatune --artist Curl --stream

The result can be user with mpc, for example to add all those songs to mpd ::

    magnatune --artist Curl --stream | mpc add

If you have a subscription login and want to hear the music without ads, you can use it ::

    magnatune --artist Curl --login login:passwd --stream

You can also download albums. This will download all the albums of curl, and extract them to the current dir ::

    magnatune --artist Curl --login login:passwd --download --dlformat ogg --extract

Of course, there is a short version. With the ``login`` and ``dlformat`` set in my config file, I just do ::

    magnatune -a Curl -de

Install
=======

``python-magnatune`` requires python 3. I strongly recommend that you use `virtualenv`_. With virtualenv installed, you can install python-magnatune by doing ::

	pip install magnatune

To work with the development version, clone the repository at https://github.com/madjar/python-magnatune and do ::

	pip install -e .


Config file
===========
``python-magnatune`` looks for default values of all arguments in the config file ``~/.python-magnatune/config.ini``. See ``config.ini.example`` for more information.

Contribute
==========

The source code is available on `github`_.

If you notice a bug or have a request, please file a `report`_

Credits
=======

:Author: Georges Dubus (madjar)


.. _`magnatune`: http://magnatune.com/
.. _`github`: https://github.com/madjar/python-magnatune
.. _`report`: https://github.com/madjar/python-magnatune/issues
.. _`virtualenv`: http://www.virtualenv.org/
