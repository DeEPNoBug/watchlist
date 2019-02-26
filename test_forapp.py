#!/usr/bin/python3
# -*- coding: utf-8 -*-


import unittest

from app import say_hello


class SayHelloTestCase(unittest.TestCase):
    """测试用例"""

    def setUp(self):
        # 在每个测试方法执行前被调用
        pass

    def tearDown(self):
        # 在每一个测试方法执行后调用
        pass

    def test_sayhello(self):
        # 第1 个 测试
        rv = say_hello()
        self.assertEqual(rv, "Hello!")

    def test_sayhello_to_somebody(self):
        # 第 2 个测试
        rv = say_hello(to="Grey")
        self.assertEqual(rv, "Hello, Grey!")


"""
常用的断言方法
assertEqual(a, b)
assertNotEqual(a, b)
assertTrue(x)
assertFalse(x)
assertIs(a, b)
assertIsNot(x)
assertIsNone(x)
assertIsNotNone(x)
assertIn(a, b)
assertNotIn(a, b)
"""

if __name__ == '__main__':
    unittest.main()
