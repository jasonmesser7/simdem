# -*- coding: utf-8 -*-
""" system level test class """

import configparser
import logging
import sys
import unittest

from ddt import data, ddt

from simdem.parser import simdem1
from simdem.executor import bash
from simdem.mode import demo


@ddt
class SimDemSystemTestSuite(unittest.TestCase):
    """Advanced test cases."""

    simdem = None

    def setUp(self):
        config = configparser.ConfigParser()
        config.read("examples/config/unit_test.ini")
        self.demo = demo.DemoMode(config, simdem1.SimDem1Parser(), bash.BashExecutor())

        log_formatter = logging.Formatter(config.get('log', 'format', raw=True))
        root_logger = logging.getLogger()
        root_logger.setLevel(config.get('log', 'level'))
        file_handler = logging.FileHandler(config.get('log', 'file'))
        file_handler.setFormatter(log_formatter)
        root_logger.addHandler(file_handler)

    # https://docs.python.org/3/library/unittest.html#unittest.TestResult.buffer
    @data('simple', 'simple-variable', 'results-block',
          'results-block-fail', 'prerequisites')
    def test_process(self, directory):
        """ Each examples directory is expected to have a README.md and an expected_result.out
            this allows us to test each of them easily
        """
        self.demo.process_file('./examples/' + directory + '/README.md')
        # Unsure why Pylint complains that 'TextIOWrapper' has no 'getvalue' member.
        # I'm not Python smart enough yet to know why this works, but Pylint says it shouldn't.
        res = sys.stdout.getvalue() # pylint: disable=E1101
        exp_res = open('./examples/' + directory + '/expected_result.demo', 'r').read()
        self.assertEqual(exp_res, res)


if __name__ == '__main__':
    unittest.main()
