# -*- coding: utf-8 -*-
"""
"""

from mcrconpy.packet import Packet


import socket
from threading import Thread
from time import sleep

import random



class FakeServer(Thread):

    def __init__(
        self,
        address: str,
        port: int = 25575,
        test_password: str = "test",
        daemon: bool = True
    ) -> None:
        """
        """
        super().__init__(daemon=daemon)
        self.test_password = test_password
        self.address = address
        self.port = port
        self.server = None
        self.is_ready = False
        self.running = True

        self.connections = []

        # random.seed(3)

    def run(self) -> None:
        """
        """
        print(self.address, self.port)


        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server.bind((self.address, self.port))

        self.server.listen(1)


        self.is_ready = True

        while self.running:
            try:
                current_conn, address = self.server.accept()

                self.connections.append(current_conn)

                Thread(
                    target=self.handle_client,
                    args=(current_conn,),
                    daemon=True
                ).start()

            except OSError:
                break

    def handle_client(
        self,
        current_conn: socket.socket
    ) -> None:
        """
        """
        try:
            while True:
                length_packet = self.__read(connection=current_conn, size=4)
                if not length_packet:
                    break

                chunk_size = int.from_bytes(length_packet, byteorder="little")
                data = self.__read(connection=current_conn, size=chunk_size)
                if not data:
                    break

                packet = Packet.decode(length_packet + data)


                if int(packet[2]) == Packet.SERVERDATA_AUTH:
                    if self.test_password == packet[3]:
                        id_response = packet[1]
                    else:
                        id_response = -1

                    res_packet = Packet.build(
                                            req_id=id_response,
                                            packet_type=2,
                                            data=b'\x00',
                                        )
                elif int(packet[2]) == Packet.SERVERDATA_EXECCOMMAND:
                    # print("command")
                    res_packet = Packet.build(
                                            req_id=packet[1],
                                            packet_type=0,
                                            data='Command OK!',
                                        )
                else:
                    # print("ping")
                    res_packet = Packet.build(
                                            req_id=packet[1],
                                            packet_type=0,
                                            data='PING',
                                        )

                sleep(0.1)
                current_conn.sendall(res_packet)

        except Exception as e:
            print(">>> ", e)
        finally:
            current_conn.close()

    def __read(
        self,
        connection: socket.socket,
        size: int = 4
    ) -> bytes:
        """
        """
        data = b''
        while len(data) < size:
            res = connection.recv(size - len(data))
            if not res:
                break
            data += res
        return data

    def wait_to_setup(self) -> None:
        """
        """
        while True:
            if self.is_ready:
                print("> Server is READY!!!!")
                break

    def close(self) -> None:
        """
        """
        print("Closing Fake Server.")
        self.running = False

        for conn in self.connections:
            conn.close()

        if hasattr(self.server, "close"):
            self.server.shutdown(socket.SHUT_RDWR)  # fuerza cierre
            self.server.close()
        print("Server Closed!")
