Napr
====

|Python|_ |PyPI|_ |Downloads|_

.. |Python| image:: https://img.shields.io/pypi/pyversions/napr
.. _Python: https://img.shields.io/pypi/pyversions/napr
.. |PyPI| image:: https://img.shields.io/pypi/v/napr
.. _PyPi: https://pypi.org/project/napr
.. |Downloads| image:: https://img.shields.io/pypi/dm/napr
.. _Downloads: https://img.shields.io/pypi/dm/napr

.. |PytestMinVersion| replace:: 6.2.5

Napr is a Python package that takes a machine learning driven approach to navigate the natural products chemical space.

Install
-------
.. code-block:: bash

    pip install napr

To update napr to the latest version, add -U or --upgrade flag, i.e. :code:`pip install -U napr`.



Tutorials
---------

You can find the followings in the `tutorials <https://github.com/smortezah/napr/tree/main/tutorials>`_ directory:

- `Terpene-explore <https://github.com/smortezah/napr/tree/main/tutorials/Terpene-explore.ipynb>`_: exploratory data analysis of terpenes (the COCONUT dataset) in the natural products chemical space

Development
-----------

We welcome new contributors of all experience levels.

Testing
~~~~~~~

You can launch the test suite, after installation (``pytest`` >= |PyTestMinVersion| is required):

.. code-block:: console 

    pytest napr

Cite
----

If you use this package, please cite:

- Hosseini, Morteza, and David M. Pereira. "The chemical space of terpenes: insights from data science and AI." arXiv preprint `arXiv:2110.15047 <https://arxiv.org/abs/2110.15047>`_ (2021).