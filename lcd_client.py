#!/usr/bin/env python
import rpyc
import sys
import time

stringdata = "My dear friend, Believe me that I was sincerely afflicted when I learned of the loss you have suffered: a steam powered urinal is not easily replaced. Yours, which had among other peculiarities, the ability to sing the Marseillaise when in use, was certainly worthy of the esteem you bestowed upon it. So, it is easy for me to understand the despair that your sister felt when it became evident that the urinal was definitely lost. Nevertheless, from that to suicide is quite a step! And, although I know that many fond memories were associated with its possession, I cannot but sondem such a fatal resolve. But this censure does not prevent me from profoundly deploring her sad end."
# source "The Surrealism Server"
#

def main():
    # In order to uniquely identify the service, pass in a
    # socket id on the command line
    if len(sys.argv) == 2:
        socket_id = int(sys.argv[1])
    elif len(sys.argv) > 1:
        print "Usage: lcd_service.py (socket_id)"
        sys.exit(2)
    else:
        # defaults
        socket_id = 18861

    print "Using socket id", socket_id

    c = rpyc.connect("localhost", socket_id)
    while True:
        c.root.print_string(stringdata[0:160])
        time.sleep(2)
        c.root.print_string(stringdata[160:320])
        time.sleep(2)


if __name__ == "__main__":
    main()





