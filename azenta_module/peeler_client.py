#!/usr/bin/env python 


from azenta_driver import peeler_client




if __name__ == "__main__":
    peeler_client = peeler_client.BROOKS_PEELER_CLIENT("/dev/ttyUSB0")

    status = False
    version = True

    if status:
        peeler_client.check_status()

    if version:
        peeler_client.check_version()

