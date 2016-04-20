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
line script depends on docopt. Tests require pytest.

blind can be installed with ``python setup.py install`` or similar.


Blinding files
==============

Run ``blind --help`` from the command line for instructions.

If you prefer a GUI, you can run ``blind_gui``.
