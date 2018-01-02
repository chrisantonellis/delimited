Usage
=====

Basic usage of :py:class:`DelimitedDict`
----------------------------------------

Setup
^^^^^

.. code-block:: python
  
  from delimited import DelimitedDict
  
  data = {
    "profile": {
      "name": "Chris",
    },
    "account": {
      "location": {
        "city": "Boston",
        "state": "MA"
      }
    }
  }
  
  user = DelmitedDict(data)

Access
^^^^^^

.. code-block:: python
  
  user.get("account.location.city")
  # returns "Boston"
  
Modify
^^^^^^

.. code-block:: python
  
  user.set("profile.color", "blue")

Collapse
^^^^^^^^

.. code-block:: python

  user.collapse("account")
  # returns {"location.city": "Boston", "location.state": "MA"}
