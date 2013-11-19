=======
 blind
=======

blind is a small program that temporarily renames files or directories.
This is useful in a research setting, where quantification of the
results should not be influenced by knowledge of the experimental
condition.

For example, suppose you had these files::

  .
  |_ condition-1.txt
  |_ condition-2.txt
  |_ control-1.txt
  |_ control-2.txt

Masking them (with randomly selected four-letter words) could result
in

::

  .
  |_ glim.txt
  |_ irks.txt
  |_ tabu.txt
  |_ waur.txt

Following analyses, they can be unmasked to the original file names.


Dependencies and installation
=============================

The blind GUI depends on wxPython, including wx.lib.agw, and the command
line script depends on docopt. Tests require pytest. blind can be
installed with ``python setup.py install`` or similar.

I created the GUI for a person that is using Windows (without a python
install), so I'ved used pyinstaller_ to bundle the program as a
stand-alone exe. The lastest version can be downloaded from here_. If
you think this program would be of use to you, but you are using OS X
and are not comfortable with Python, contact me and I'll try to do
similar for OS X.


Blinding files
==============

Run ``blind --help`` from the command line for instructions.

If you prefer a GUI, you can run ``blind_gui``.

.. _pyinstaller: http://www.pyinstaller.org/
.. _here: https://www.dropbox.com/sh/579ot10oqnte90q/kSEPmSfz8M
