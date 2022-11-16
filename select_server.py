# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select
import queue

def run_server(port):
    # TODO--fill this in
    s = socket.socket()
    s.setblocking(0)
    s.bind(('', port))
    s.listen()
    inputs = [s]
    outputs = []
    message_queue = {}
    while True:
        r, w, e = select.select(inputs, outputs, inputs)
        for server in r:
            if server is s:

                new_socket, connect_info = server.accept()
                print(new_socket.getpeername(), ':  connected')
                new_socket.setblocking(0)
                inputs.append(new_socket)
                message_queue[new_socket] = queue.Queue()
            else:
                
                data = server.recv(4096)
                if len(data) != 0:
                     print(server.getpeername(), len(data), 'bytes' , data)
                     message_queue[server].put(data)

                     if server not in outputs:
                        outputs.append(server)
                else:
                    if server in outputs:
                        outputs.remove(server)
                    inputs.remove(server)
                    print(server.getpeername(), ':  disconnected')
                    server.close()
                    
                    del message_queue[server]

                # for server in w:
                #     try:
                #         next_byte_string = message_queue[server].get_nowait()
                #     except queue.Empty:

                #         print('output queue for', server.getpeername(), 'is empty')
                        
                #         outputs.remove(server)
                #         server.close()
                #         print(new_socket.getpeername(), ':  disconnected')
                #     else:
                #         print(server.getpeername(), len(next_byte_string), 'bytes' , next_byte_string)
                #         server.send(next_byte_string)
                
                # for server in e:
                #     print('handling exceptional condition for', server.getpeername())
                #     inputs.remove(server)
                #     if server in outputs:
                #         outputs.remove(server)
                #     server.close()
                #     del message_queue[server]



                    
        # if connect_info != None:
        #     print(s.getpeername(), ':  connected')
        # while True:
        #     data = s.recv(4096)
        
        #     print(s.getpeername(), len(data), new_socket)
        #     if data == 0:
        #         s.close()
        #         print(s.getpeername(), ':  disconnected')
    

#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
