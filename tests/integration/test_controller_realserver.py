# -*- coding: utf-8 -*-
"""
"""

from mcrconpy.controller import RconPy


import unittest


class TestControllerRealServer(unittest.TestCase):

    address = "127.0.0.1"
    port = 25575
    test_password = "test"

    def setUp(self) -> None:
        """
        """
        self.controller = RconPy(
                                address=TestControllerRealServer.address,
                                port=TestControllerRealServer.port,
                                password=TestControllerRealServer.test_password,
                                audit=False,
                            )

    def test_changepassword(self) -> None:
        """
        """
        oldpass = self.controller.get_password()

        self.controller.set_password("new")

        new = self.controller.get_password()

        self.controller.set_password("test")

        self.assertTrue(new == "new")

    def test_login(self) -> None:
        """
        """
        # no login
        self.assertFalse(self.controller.is_login())

        # # login
        self.controller.connect()
        self.controller.login()
        self.assertTrue(self.controller.is_login())

    def test_controller_flow(self) -> None:
        """
        """
        # before connection and login
        self.assertFalse(self.controller.check_connection())
        self.assertFalse(self.controller.is_login())

        # after connection and login
        self.controller.connect()
        self.assertTrue(self.controller.check_connection())
        self.assertFalse(self.controller.is_login())

        self.controller.login()
        self.assertTrue(self.controller.is_login())

        # test send command
        r = self.controller.command(command="/time query daytime")
        self.assertIsInstance(r, str)

        self.controller.disconnect()
        self.assertIsNone(self.controller.conn.socket)
        self.assertFalse(self.controller.check_connection())
        self.assertFalse(self.controller.is_login())

    def tearDown(self) -> None:
        """
        """
        self.controller.disconnect()
