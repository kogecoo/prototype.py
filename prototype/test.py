#!/usr/bin/env python
# -*- coding: utf-8 -*

from parallel.parallel_collections import ParallelGen
import itertools as it
import common.itertools_more as itm
import itr
import par
import types
import unittest


class TestItr(unittest.TestCase):

    def test_patch_detach(self):
        itr.attach()

        for k in itr.attrs.keys():
            self.assertTrue(k in list.__dict__)
            self.assertTrue(k in tuple.__dict__)
            self.assertTrue(k in types.GeneratorType.__dict__)

        itr.detach()

        for k in itr.attrs.keys():
            self.assertFalse(k in list.__dict__)
            self.assertFalse(k in tuple.__dict__)
            self.assertFalse(k in types.GeneratorType.__dict__)

    def test_map(self):
        itr.attach()

        l = list(range(10))
        t = tuple(range(10))
        g = lambda: (x for x in range(10))
        lf = lambda x: str(x)
        tf = lambda x: x % 3
        gf = lambda x: x % 2

        self.assertEqual(list(l.map(lf)), map(lf, l))
        self.assertEqual(list(t.map(tf)), map(tf, t))
        self.assertEqual(list(g().map(gf)), map(gf, g()))
        self.assertEqual(list(l.map(lf)), map(lf, l))
        self.assertEqual(list(t.map(tf)), map(tf, t))
        self.assertEqual(list(g().map(gf)), map(gf, g()))

        itr.detach()

    def test_reduce(self):
        itr.attach()

        l1 = list(range(10))
        l2 = list(range(10, 20))
        lf1 = lambda x, y: x + y
        lf2 = lambda x, y: x * y
        l_init = 10

        t1 = tuple(range(10))
        t2 = tuple(map(lambda x: str(x), range(30, 40)))
        tf1 = lambda x, y: x * y
        tf2 = lambda x, y: x + y
        t_init = "abc"

        g1 = lambda: (x for x in range(10))
        g2 = lambda: (y for y in map(lambda x: x % 2 == 0, range(10)))
        gf1 = lambda x, y: -x + y
        gf2 = lambda x, y: x and y
        g_init = True

        # list
        self.assertEqual(l1.reduce(lf1), reduce(lf1, l1))
        self.assertEqual(l2.reduce(lf2, l_init), reduce(lf2, l2, l_init))

        # tuple
        self.assertEqual(t1.reduce(tf1), reduce(tf1, t1))
        self.assertEqual(t2.reduce(tf2, t_init), reduce(tf2, t2, t_init))

        # generator
        self.assertEqual(g1().reduce(gf1), reduce(gf1, g1()))
        self.assertEqual(g2().reduce(gf2, g_init), reduce(gf2, g2(), g_init))

        itr.detach()

    def test_filter(self):
        itr.attach()

        l1 = list(range(10))
        l2 = list(map(lambda x: chr(x + 65), range(10)))

        t1 = tuple(range(10))
        t2 = tuple(map(lambda x: chr(x + 65), range(10)))

        g1 = lambda: (x for x in range(10))
        g2 = lambda: (chr(x + 65) for x in range(10))

        f1 = lambda x: x % 2 != 0
        f2 = lambda x: x < 'D'

        # list
        self.assertEqual(list(l1.filter(f1)), filter(f1, l1))
        self.assertEqual(list(l2.filter(f2)), filter(f2, l2))

        # tuple
        self.assertEqual(list(t1.filter(f1)), list(filter(f1, t1)))
        self.assertEqual(list(t2.filter(f2)), list(filter(f2, t2)))

        # generator
        self.assertEqual(list(g1().filter(f1)), list(filter(f1, g1())))
        self.assertEqual(list(g2().filter(f2)), list(filter(f2, g2())))

        itr.detach()

    def test_zip(self):
        itr.attach()

        l1 = list(range(10))
        l2 = list(map(lambda x: str(x), range(20, 40)))

        t1 = tuple(range(10))
        t2 = tuple(map(lambda x: str(x), range(20, 40)))

        g1 = lambda: (x for x in range(10))
        g2 = lambda: (str(x) for x in range(20, 40))

        # list
        self.assertEqual(list(l1.zip(l2)), zip(l1, l2))

        # tuple
        self.assertEqual(list(t1.zip(t2)), zip(t1, t2))

        # generator
        self.assertEqual(list(g1().zip(g2())), zip(g1(), g2()))

        # combination
        self.assertEqual(list(l1.zip(t2)), zip(l1, t2))
        self.assertEqual(list(t1.zip(l2)), zip(t1, l2))
        self.assertEqual(list(l1.zip(g2())), zip(l1, g2()))
        self.assertEqual(list(g1().zip(l2)), zip(g1(), l2))
        self.assertEqual(list(t1.zip(g2())), zip(t1, g2()))
        self.assertEqual(list(g1().zip(t2)), zip(g1(), t2))

        itr.detach()

    def test_takewhile(self):
        itr.attach()

        l = list(range(10))
        t = tuple(range(10))
        g = lambda: (x for x in range(10))

        f1 = lambda x: x < 2
        f2 = lambda x: x < 10
        f3 = lambda x: x > 100

        self.assertEqual(list(l.takewhile(f1)), list(it.takewhile(f1, l)))
        self.assertEqual(list(l.takewhile(f2)), list(it.takewhile(f2, l)))
        self.assertEqual(list(l.takewhile(f3)), list(it.takewhile(f3, l)))
        self.assertEqual(list(t.takewhile(f1)), list(it.takewhile(f1, t)))
        self.assertEqual(list(t.takewhile(f2)), list(it.takewhile(f2, t)))
        self.assertEqual(list(t.takewhile(f3)), list(it.takewhile(f3, t)))
        self.assertEqual(list(g().takewhile(f1)), list(it.takewhile(f1, g())))
        self.assertEqual(list(g().takewhile(f2)), list(it.takewhile(f2, g())))
        self.assertEqual(list(g().takewhile(f3)), list(it.takewhile(f3, g())))
        itr.detach()

    def test_take(self):
        itr.attach()

        l = list(range(10))
        t = tuple(range(20, 30))
        g = lambda: (x for x in range(30, 40))

        # list
        self.assertEqual(list(l.take(0)), [])
        self.assertEqual(list(l.take(5)), l[:5])
        self.assertEqual(list(l.take(20)), l[:20])
        self.assertEqual(list(t.take(0)), [])
        self.assertEqual(list(t.take(5)), list(t[:5]))
        self.assertEqual(list(t.take(20)), list(t[:20]))
        self.assertEqual(list(g().take(0)), [])
        self.assertEqual(list(g().take(5)), list(g())[:5])
        self.assertEqual(list(g().take(20)), list(g())[:20])

        itr.detach()

    def test_flatmap(self):
        itr.attach()

        l1 = [[1, 2, 3], [4], [], [5, 6, 7, 8, 9]]
        l2 = ["abc", "def", "ghi"]
        t1 = ((1, 2, 3), (4,), (5, 6), ())
        t2 = (("A", "B", "C"), ("D", "E", "F"), ("G", "H", "I"))

        def g1():
            child1 = (x for x in range(1, 4))
            child2 = (x for x in range(4, 6))
            child3 = (x for x in range(0))
            child4 = (x for x in range(6, 7))
            children = [child1, child2, child3, child4]
            for c in children:
                yield c

        def g2():
            child1 = "abcd"
            child2 = [1, 2, 3, 4]
            child3 = ("e", "f", "g")
            child4 = (x for x in range(1))
            children = [child1, child2, child3, child4]
            for c in children:
                yield c

        f1 = lambda x: x * 10
        f2 = lambda x: x.upper()
        f3 = lambda x: x * 10
        f4 = lambda x: x.lower()
        f5 = lambda x: x * 10
        f6 = lambda x: str(x).upper()

        e1 = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        e2 = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        e3 = [10, 20, 30, 40, 50, 60]
        e4 = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        e5 = [10, 20, 30, 40, 50, 60]
        e6 = ["A", "B", "C", "D", "1", "2", "3", "4", "E", "F", "G", "0"]

        self.assertEqual(list(l1.flatmap(f1)), e1)
        self.assertEqual(list(l2.flatmap(f2)), e2)
        self.assertEqual(list(t1.flatmap(f3)), e3)
        self.assertEqual(list(t2.flatmap(f4)), e4)
        self.assertEqual(list(g1().flatmap(f5)), e5)
        self.assertEqual(list(g2().flatmap(f6)), e6)

        itr.detach()

    def test_flatten(self):
        itr.attach()

        l1 = [[1, 2, 3], [4, 5], [6], []]
        l2 = ["abc", "de", "f", ""]
        t1 = ((1, 2, 3), (4, 5), (6,), ())
        t2 = ("abc", "de", "f", "")

        def g1():
            child1 = (x for x in range(1, 4))
            child2 = (x for x in range(4, 6))
            child3 = (x for x in range(6, 7))
            child4 = (x for x in range(0))
            children = [child1, child2, child3, child4]
            for c in children:
                yield c

        g2 = lambda: (c for c in ["abc", "de", "f", ""])

        e1 = list(range(1, 7))
        e2 = ["a", "b", "c", "d", "e", "f"]

        self.assertEqual(list(l1.flatten()), e1)
        self.assertEqual(list(l2.flatten()), e2)
        self.assertEqual(list(t1.flatten()), e1)
        self.assertEqual(list(t2.flatten()), e2)
        self.assertEqual(list(g1().flatten()), e1)
        self.assertEqual(list(g2().flatten()), e2)

        itr.detach()

    def test_foldl(self):
        itr.attach()

        l1 = list(range(10))
        l2 = list(range(10, 20))
        lf1 = lambda x, y: x + y
        lf2 = lambda x, y: x * y
        l_init = 10

        t1 = tuple(range(10))
        t2 = tuple(map(lambda x: str(x), range(30, 40)))
        tf1 = lambda x, y: x * y
        tf2 = lambda x, y: x + y
        t_init = "abc"

        g1 = lambda: (x for x in range(10))
        g2 = lambda: (y for y in map(lambda x: x % 2 == 0, range(10)))
        gf1 = lambda x, y: -x + y
        gf2 = lambda x, y: x and y
        g_init = True

        # list
        self.assertEqual(l1.foldl(lf1), reduce(lf1, l1))
        self.assertEqual(l2.foldl(lf2, l_init), reduce(lf2, l2, l_init))

        # tuple
        self.assertEqual(t1.foldl(tf1), reduce(tf1, t1))
        self.assertEqual(t2.foldl(tf2, t_init), reduce(tf2, t2, t_init))

        # generator
        self.assertEqual(g1().foldl(gf1), reduce(gf1, g1()))
        self.assertEqual(g2().foldl(gf2, g_init), reduce(gf2, g2(), g_init))

        itr.detach()

    def test_len(self):
        itr.attach()

        l = list(range(10))
        t = tuple(range(10, 25))
        g = lambda: (x for x in "this is a test sentence")

        # list
        self.assertEqual(l.len(), len(l))
        self.assertEqual(t.len(), len(t))
        self.assertRaises(TypeError, g().len)

        itr.detach()

    def test_to_iter(self):
        itr.attach()

        l = list(range(10))
        t = tuple(range(10))
        g = lambda: (x for x in range(10))

        self.assertEqual([x for x in l.to_iter()], l)
        self.assertEqual([x for x in t.to_iter()], list(t))
        self.assertEqual([x for x in g().to_iter()], list(g()))

        itr.detach()

    def test_to_list(self):
        itr.attach()

        l = list(range(10))
        t = tuple(range(10))
        g = lambda: (x for x in range(10))

        self.assertEqual(l.to_list(), l)
        self.assertEqual(t.to_list(), list(t))
        self.assertEqual(g().to_list(), list(g()))

        itr.detach()


def mul10(x):
    return x * 10


def evn(x):
    return x % 2 == 0


def add(x, y):
    return x + y


class TestPar(unittest.TestCase):

    def test_attrs(self):
        par.attach()

        l = list(range(10))
        t = tuple(range(10))
        g = lambda: (x for x in range(10))

        self.assertTrue(isinstance(l.par(), ParallelGen))
        self.assertTrue(isinstance(t.par(), ParallelGen))
        self.assertTrue(isinstance(g().par(), ParallelGen))

        par.detach()

    # Testig function of Python-Parallel-Collection through a builtin.par().
    def test_parallel(self):
        par.attach()

        l1 = list(range(100))
        l2 = [list(range(10)) for _ in range(100)]
        l3 = list(range(100))
        t1 = tuple(range(100))
        t2 = [tuple(range(10)) for _ in range(100)]
        t3 = list(range(100))
        g1 = lambda: (x for x in range(100))
        g2 = lambda: ((y for y in range(10)) for _ in range(100))
        g3 = lambda: (x for x in range(100))
        e3 = list(it.imap(lambda x: x * 10,  range(100)))

        # list
        self.assertEqual(list(l1.par().filter(evn)), list(filter(evn, l1)))
        self.assertEqual(list(l2.par().flatten()), list(itm.iflatten(l2)))
        self.assertEqual(list(l1.par().map(mul10)), list(it.imap(mul10, l1)))
        self.assertEqual(list(l2.par().flatmap(mul10)), list(itm.iflatmap(l2, mul10)))
        self.assertEqual(l1.par().reduce(add, 0), reduce(add, l1, 0))
        temp = l3.par()
        temp.foreach(mul10)
        self.assertEqual(list(temp), e3)

        # tuple
        self.assertEqual(list(t1.par().filter(evn)), list(filter(evn, t1)))
        self.assertEqual(list(t2.par().flatten()), list(itm.iflatten(t2)))
        self.assertEqual(list(t1.par().map(mul10)), list(it.imap(mul10, t1)))
        self.assertEqual(list(t2.par().flatmap(mul10)), list(itm.iflatmap(t2, mul10)))
        self.assertEqual(t1.par().reduce(add, 0), reduce(add, t1, 0))
        temp = t3.par()
        temp.foreach(mul10)
        self.assertEqual(list(temp), e3)

        # generator
        self.assertEqual(list(g1().par().filter(evn)), list(filter(evn, g1())))
        self.assertEqual(list(g2().par().flatten()), list(itm.iflatten(g2())))
        self.assertEqual(list(g1().par().map(mul10)), list(it.imap(mul10, g1())))
        self.assertEqual(list(g2().par().flatmap(mul10)), list(itm.iflatmap(g2(), mul10)))
        self.assertEqual(g1().par().reduce(add, 0), reduce(add, g1(), 0))
        temp = g3().par()
        temp.foreach(mul10)
        self.assertEqual(list(temp), e3)

        par.detach()

    def test_fold(self):
        par.attach()

        l = list(range(10))
        t = tuple(range(10))
        g = lambda: (x for x in range(10))
        f = lambda x, y: x * y
        init = 10
        e1 = reduce(f, range(10))
        e2 = reduce(f, range(10), init)

        self.assertEqual(l.par().fold(f), e1)
        self.assertEqual(l.par().fold(f, init), e2)
        self.assertEqual(t.par().fold(f), e1)
        self.assertEqual(t.par().fold(f, init), e2)
        self.assertEqual(g().par().fold(f), e1)
        self.assertEqual(g().par().fold(f, init), e2)

        par.detach()

    def test_both(self):
        par.attach()
        itr.attach()

        l = list(range(10))
        self.assertEqual(l.par().map(mul10).to_single().reduce(add), 450)

        itr.detach()
        par.detach()


if __name__ == '__main__':
    unittest.main()
