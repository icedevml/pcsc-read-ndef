import binascii
import io
import sys

import ndef
from smartcard.Exceptions import NoCardException, CardConnectionException
from smartcard.System import readers
from smartcard.util import toHexString


def send_command(conn, cmd):
    # send a PC/SC command and get response
    cmd_arr = [x for x in cmd]
    res = conn.transmit(cmd_arr)
    return bytes(res[0])


def parse_data(data):
    buf = io.BytesIO(data)

    while True:
        tag = buf.read(1)

        if tag == b"\x00":
            # NULL TLV reached
            break
        elif tag == b"\x03":
            # NDEF Message TLV reached
            ndef_len = ord(buf.read(1))
            yield buf.read(ndef_len)
        elif tag == b"":
            # we didn't read anything, it shouldn't happen
            # the data might be incomplete
            raise RuntimeError('Failed to parse T2T data')
        else:
            # unknown TLV, skip
            tlv_len = ord(buf.read(1))
            buf.read(tlv_len)


def check_version(conn):
    try:
        # verify whether we are talking to NTAG 21x
        version = send_command(conn, b"\xFF\xEF\x00\x00\x01\x60")

        if version[0:6] != binascii.unhexlify("000404020100"):
            print('Version mismatch, unsupported tag')
            return False

        if version[6:7] not in [b"\x0F", b"\x11", b"\x13"]:
            # this is not NTAG 213, 215 nor 216
            print('Version mismatch, unsupported subtype of tag')
            return False

        if version[7:] != b"\x03":
            print('Version mismatch, unsupported protocol')
            return False
    except CardConnectionException:
        print('Failed to get version')
        return False

    return True


def read_ndef(conn):
    content = b""

    # read Capability Container at page #3
    cc = send_command(conn, b"\xFF\xEF\x00\x00\x02\x30\x03")

    # calculate total memory size
    total_bytes = cc[2] * 8
    total_pages = total_bytes // 4
    total_quads = total_pages // 4

    # read all memory pages
    for i in range(1, total_quads + 1):
        content += send_command(conn, b"\xFF\xEF\x00\x00\x02\x30" + bytes([4 * i]))

    # parse TLV
    data = b"".join(parse_data(content))

    # parse NDEF
    decoded = list(ndef.message_decoder(data))
    return decoded


def scan_for_ndef():
    for reader in readers():
        try:
            connection = reader.createConnection()
            connection.connect()

            print(reader, toHexString(connection.getATR()))

            if check_version(connection):
                res = read_ndef(connection)

                if res:
                    return res
        except NoCardException:
            print(reader, 'no card inserted')
    else:
        print('Card not found')


if __name__ == "__main__":
    scan_res = scan_for_ndef()

    print(scan_res)

    if 'win32' == sys.platform:
        print('press Enter to continue')
        sys.stdin.read(1)
