

# Cafet HMI

This project is a simple user interface for the management of snacks at IMT Atlantique. We manage ourselves the provisioning of coffee, tea, chocolate, etc...  Thanks to a web solution [laclef](http://laclef.cc/). Thanks @github/bgaultier !

Before this solution, we would: 1) login on the web interface, 2) select the product of interest and 3) debit our account. We propose a connected device which will identify you with your nfc tag, let you select your product and quantity and then validate ! In a few quick steps our account is debited.

![Demo](https://github.com/marcokome/CafetHMI/blob/master/demo.gif)

Install
----------------------

The device consists of the parts depicted in the following picture:
1. A raspberry pi 3 with raspbian lite image
2. An official raspberry pi touch screen
3. A buzzer
4. An rfc reader

The interface is using ``PyQt5`` objects. I would recommend installing the project first on your personal computer for a first test. After cloning the project, run the install file. Make sure you have ``python 3.5.2`` or newer installed.

```
git clone https://github.com/marcokome/CafetHMI.git.
cd CafetHMI
python3 install.py
```
On your PC, If everything is ok then modify the file ``start_app.py`` to set ``application.rpi`` variable to ``False``. Once modified, save the file and run it

```
python3 start_app.py
```
As a result, you should see the program waiting for a scan. This is a demo on your PC, so to simulate the badge reader, change the value of ``id`` in ``test.json`` according to the following values:
- ``0``: still scanning
- ``1``: the badge exists in db
- ``2``: the badge is unknown.


Licensing
---------

The project is published under the MIT License. Don't hesitate to contact me for any enhancement or discussion.

Copyright (c) 2020-2021 Marco KOME <marcokome@gmail.com/>,

Troubleshooting
---------------
Please file at the [github issue tracker](issues).
