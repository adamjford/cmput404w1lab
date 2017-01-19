#!/usr/bin/env python

import socket, os, sys, errno, select

# AF_INET means we want an IPv4 socket
# SOCK_STREAM means we want a TCP socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# tells the OS that we'd like to reuse the socket rapidly (Question 3)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Can't use port 80 because we don't have root
serverSocket.bind(("0.0.0.0", 8000))
serverSocket.listen(5)

while True:
    (incomingSocket, address) = serverSocket.accept()
    print "Got a connection from %s" % (repr(address))
    
    try:
        reaped = os.waitpid(0, os.WNOHANG)
    except OSError, e:
        if e.errno != errno.ECHILD:
            raise
    else:
        print "Reaped %s" % repr(reaped)

    if os.fork() != 0:
        # parent
        continue

    # AF_INET means we want an IPv4 socket
    # SOCK_STREAM means we want a TCP socket (Question 1)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    clientSocket.connect(("www.google.com", 80))

    incomingSocket.setblocking(0)
    clientSocket.setblocking(0)
    
    while True:
        request = bytearray()

        while True:
            try:
                part = incomingSocket.recv(1024)
            except IOError, e:
                if e.errno == socket.errno.EAGAIN:
                    break
                else:
                    raise
            if part:
                request.extend(part)
                clientSocket.sendall(part)
            else:
                sys.exit(0)

        if request:
            print request

        response = bytearray()

        while True:
            try:
                part = clientSocket.recv(1024)
            except IOError, e:
                if e.errno == socket.errno.EAGAIN:
                    break
                else:
                    raise
            if part:
                request.extend(part)
                incomingSocket.sendall(part)
            else:
                sys.exit(0)

        if response:
            print response
        
        select.select(
            [incomingSocket, clientSocket], # read
            [],                             # write
            [incomingSocket, clientSocket], # exceptions
            1.0)                            # timeout
