Introduction
============

``python-magnatune`` provides a simple command line utility called ``magnatune`` that can be used to search the `magnatune`_ database and get the streaming urls.

For example, to get all the albums from Curl ::

    magnatune --artist Curl

To get the streaming urls of all songs from Curl ::

    magnatune --artist Curl --stream

The result can be user with mpc, for example to add all those songs to mpd ::

    magnatune --artist Curl --stream | mpc add

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
