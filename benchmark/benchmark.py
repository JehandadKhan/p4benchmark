#!/usr/bin/env python

import os
from subprocess import call, Popen, PIPE
import shlex
import time
import p4gen
import argparse

class P4Benchmark(object):
    def __init__(self, parent_dir, directory, offer_load):
        assert os.environ.get('P4BENCHMARK_ROOT')
        assert os.environ.get('PYTHONPATH')
        pypath = os.environ.get('PYTHONPATH')
        p4bench = os.environ.get('P4BENCHMARK_ROOT')
        bmv2 = os.path.join(p4bench, 'behavioral-model')
        self.p4c = os.path.join(p4bench, 'p4c-bm/p4c_bm/__main__.py')
        self.switch_path = os.path.join(bmv2, 'targets/simple_switch/simple_switch')
        self.cli_path = os.path.join(bmv2, 'tools/runtime_CLI.py')
        self.pktgen = os.path.join(p4bench, 'pktgen/build/p4benchmark')
        self.analyse = os.path.join(p4bench, 'benchmark/analyse.R')
        self.nb_packets = 5000
        self.log_level = ''
        self.parent_dir = parent_dir
        self.directory = directory
        self.offer_load = offer_load
        self.ipg = int(10**9 / offer_load)


    def add_rules(self, json_path, commands, retries):
        if retries > 0:
            cmd = [self.cli_path, '--json', json_path]
            if os.path.isfile(commands):
                with open(commands, "r") as f:
                    p = Popen(cmd, stdin=f, stdout=PIPE, stderr=PIPE)
                    out, err = p.communicate()
                    if out:
                        print out
                        if "Could not" in out:
                            print "Retry in 1 second"
                            time.sleep(1)
                            return self.add_rules(json_path, port_number, commands, retries-1)
                        elif  "DUPLICATE_ENTRY" in out:
                            pass
                    if err:
                        print err
                        time.sleep(1)
                        return self.add_rules(json_path, port_number, commands, retries-1)

    def has_lost_packet(self):
        with open('%s/loss.csv' % self.directory, 'r') as f:
            for line in f:
                pass
            data = shlex.split(line)
            assert (len(data) == 3)
            sent = float(data[0])
            recv = float(data[1])
        return (recv < sent)


    def run_analyser(self):
        cmd = '{0} {1}'.format(self.analyse, self.parent_dir)
        print cmd
        args = shlex.split(cmd)
        p = Popen(args)
        p.wait()

    def tearDown(self):
        cmd = 'sudo pkill lt-simple_swi'
        args = shlex.split(cmd)
        p = Popen(args)
        out, err = p.communicate()
        if out:
            print out
        if err:
            print err
        self.p.wait()
        assert (self.p.poll() != None)
        time.sleep(5)

    def start(self):
        # run switch
        self.run_behavioral_switch()
        # run packet generator
        self.run_packet_generator()
        # stop the switch
        self.tearDown()

    def run_behavioral_switch(self):
        pass

    def run_packet_generator(self):
        pass