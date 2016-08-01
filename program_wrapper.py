# -*- coding:utf-8 -*-
import sys
from subprocess import PIPE, Popen
from threading  import Thread
from Queue import Queue, Empty
import time
import signal
from argparse import ArgumentParser
from multi_thread_closing import MultiThreadClosing


class ProgramWrapper(MultiThreadClosing):

    def __init__(self, cmd):
        super(ProgramWrapper, self).__init__()
        self.cmd = cmd
        self.on_posix = 'posix' in sys.builtin_module_names
        self.child_p = Popen(self.cmd, stdout=PIPE, stderr=PIPE, bufsize=1, close_fds=self.on_posix, shell=True)

    def enqueue_output(self, out, queue, _type):
        for line in iter(out.readline, ''):
            if line != "\n":
                queue.put((_type, line))
        out.close()

    def start(self):
        q = Queue()
        t1 = Thread(target=self.enqueue_output, args=(self.child_p.stdout, q, "info"))
        self.threads.append(t1)
        t2 = Thread(target=self.enqueue_output, args=(self.child_p.stderr, q, "error"))
        self.threads.append(t2)
        for thread in self.threads:
            thread.start()
        while True:
            try:
                _type, line = q.get_nowait()
            except Empty:
                time.sleep(1)
                alive = False
                for thread in self.threads:
                    alive = alive or thread.isAlive()
                if not alive and q.empty():
                    break
            else:
                getattr(self.logger, _type)(line.strip()),

    def stop(self, *args):
        super(ProgramWrapper, self).stop(*args)
        if self.child_p:
            self.child_p.send_signal(signal.SIGTERM)

    @classmethod
    def parseArgs(cls):
        parser = ArgumentParser(description="record stdout and stderr")
        parser.add_argument('-c', '--cmd', dest="cmd", help='command to execute')
        return cls(**vars(parser.parse_args()))

if __name__ == "__main__":
    ac = ProgramWrapper.parseArgs()
    ac.set_logger()
    ac.start()