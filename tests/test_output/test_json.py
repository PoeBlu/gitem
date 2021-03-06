#!/usr/bin/env python

import collections
import io
import textwrap
import unittest

from gitem import output


class TestJson(unittest.TestCase):

    @staticmethod
    def dedent_helper(s):
        return textwrap.dedent(s).lstrip()

    def test_basic(self):
        data = collections.OrderedDict([
            ('key', 'value'),
        ])

        with io.StringIO() as stream:
            outputter = output.Json(file_=stream)
            outputter.output(data)
            result = stream.getvalue()

        expected = self.dedent_helper('''
            {"key":"value"}
        ''')

        assert result == expected

    def test_list(self):
        data = collections.OrderedDict([
            ('key1', collections.OrderedDict([
                ('key2', ['value1', 'value2']),
            ])),
        ])

        with io.StringIO() as stream:
            outputter = output.Json(file_=stream)
            outputter.output(data)
            result = stream.getvalue()

        expected = self.dedent_helper('''
            {"key1":{"key2":["value1","value2"]}}
        ''')

        assert result == expected

    def test_recurse(self):
        data = collections.OrderedDict([
            ('key1', 'value1'),
            ('key2', collections.OrderedDict([
                ('key3', 'value2'),
            ])),
        ])

        with io.StringIO() as stream:
            outputter = output.Json(file_=stream)
            outputter.output(data)
            result = stream.getvalue()

        expected = self.dedent_helper('''
            {"key1":"value1","key2":{"key3":"value2"}}
        ''')

        assert result == expected

    def test_multi(self):
        data1 = collections.OrderedDict([
            ('key1', 'value1'),
        ])
        data2 = collections.OrderedDict([
            ('key2', 'value2'),
        ])

        with io.StringIO() as stream:
            outputter = output.Json(file_=stream)
            outputter.output(data1)
            outputter.output(data2)
            result = stream.getvalue()

        expected = self.dedent_helper('''
            {"key1":"value1"}
            {"key2":"value2"}
        ''')

        assert result == expected


if __name__ == "__main__":
    unittest.main()
