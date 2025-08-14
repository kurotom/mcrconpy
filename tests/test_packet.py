# -*- coding: utf-8 -*-
"""
"""

from mcrconpy.packet import Packet

import unittest


class TestPacket(unittest.TestCase):

    def fragments(
        self,
        data: bytes
    ) -> tuple:
        """
        """
        return (
            data[0:4],
            data[4:8],
            data[4:12],
            data[12:],
            data[len(data) - 2:]
        )


    def test_build_packet(self) -> None:
        """
        """
        packet = Packet.build(
                            req_id=1,
                            packet_type=2,
                            data="test",
                        )

        length_, id_, type_, body_, ends_ = self.fragments(data=packet)


        self.assertTrue(isinstance(packet, bytes))

        self.assertTrue(
            isinstance(int.from_bytes(length_, byteorder='little'), int)
        )
        self.assertTrue(
            isinstance(int.from_bytes(id_, byteorder='little'), int)
        )
        self.assertTrue(
            isinstance(int.from_bytes(type_, byteorder='little'), int)
        )
        self.assertTrue(
            isinstance(body_.decode('ascii'), str)
        )


    def test_decode_packet(self) -> None:
        """
        """
        packet = Packet.build(
                            req_id=1,
                            packet_type=2,
                            data="test",
                        )

        decoded_ = Packet.decode(data=packet)
        self.assertEqual(decoded_[1], 1)
        self.assertEqual(decoded_[2], 2)
        self.assertEqual(decoded_[3], "test")

    def test_build_packet_incorrect_typos(self) -> None:
        """
        """
        packet = Packet.build(
                            req_id="1",
                            packet_type=2,
                            data="test",
                        )
        self.assertIsNone(packet)

        packet = Packet.build(
                            req_id=1,
                            packet_type="2",
                            data="test",
                        )
        self.assertIsNone(packet)

        packet = Packet.build(
                            req_id=1,
                            packet_type=2,
                            data=3,
                        )
        self.assertIsNone(packet)


    def test_decode_packet_incorrect_typos(self) -> None:
        """
        """
        decoded_ = Packet.decode(data="str")
        self.assertEqual(decoded_, ())
        self.assertEqual(len(decoded_), 0)
