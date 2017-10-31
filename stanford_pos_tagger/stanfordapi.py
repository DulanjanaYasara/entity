# -*- coding: utf-8 -*-
import socket
import time
from subprocess import Popen

from unidecode import unidecode


class StanfordAPI:
    """Used to initialize the Stanford POS tagger in servlet mode and then connect to it using a socket"""

    def __init__(self, path_to_model='stanford_pos_tagger/english-bidirectional-distsim.tagger',
                 path_to_jar='stanford_pos_tagger/stanford-postagger.jar', port=5000, buffer_size=4096):
        """Used to initialize the StanfordAPI object with the host, port and buffer"""
        self.host = socket.gethostname()
        self.port = port
        self.buffer = buffer_size
        self.process = Popen(
            ['java', '-mx2g', '-cp', path_to_jar, 'edu.stanford.nlp.tagger.maxent.MaxentTaggerServer',
             '-model', path_to_model, '-port', '5000', '-sentenceDeLimiter', 'newline'])
        time.sleep(5)

    def pos_tag(self, message):
        """Used to send requests to the socket"""
        s = socket.socket()
        s.connect((self.host, self.port))
        if message.strip() == '':
            s.close()
            return []
        s.send(to_ascii(message))
        data = s.recv(self.buffer)
        s.close()
        return [tuple(x.rsplit('_', 1)) for x in str(data).encode('ascii', 'ignore').strip().split()]

    def __del__(self):
        """ Terminating the process """
        self.process.terminate()


def to_ascii(message):
    if message is None or message.strip() == '':
        return ''
    return (unidecode(message) + '\n').encode('ascii', errors='ignore')


def test():
    """Test method for the Stanford API class"""
    stanford_api = StanfordAPI()
    text = '''moçambique I'm attempting to produce a stream of comments from a Facebook page. 
    Ultimately I'd like a response from WSO2 like this: I'm using the API module for WSO2 ESB to provide an 
    abstraction layer over a Facebook page to get a simple stream of all the comments on a page after a given 
    timestamp. The logic I'm working on right now is taking all the posts on a given Facebook page (using the WSO2 
    Facebook Connector), iterating over all the posts (using an iterate mediator), checking if the post has comments 
    (using the filter mediator), if there are comments I'm then iterating over the '''
    print(stanford_api.pos_tag(unidecode(text.decode('utf-8')).decode('ascii', 'ignore')))


if __name__ == "__main__":
    test()
