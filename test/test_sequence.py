import sys; sys.path.append("../")

import unittest
import copy

from delimited.path import TuplePath
from delimited.path import DelimitedStrPath

from delimited.sequence import ListIndex
from delimited.sequence import NestedList


class TestNestedList(unittest.TestCase):

    # __init__

    def test___init____no_args(self):
        a = NestedList()
        self.assertEqual(a.data, [])
    
    def test___init____list_arg(self):
        a = NestedList(["v"])
        self.assertEqual(a, ["v"])
    
    # __call__
    
    def test___call____no_args(self):
        a = NestedList(["v"])
        a()
        self.assertEqual(a, [])
    
    def test___call____dict_arg(self):
        a = NestedList()
        a(["v"])
        self.assertEqual(a, ["v"])
    
    # __bool__
    
    def test___bool____empty_data__returns_False(self):
        self.assertFalse(bool(NestedList()))
    
    def test___bool____non_empty_data__returns_True(self):
        self.assertTrue(bool(NestedList(["v"])))
    
    # __repr__
    
    def test___repr__(self):
        a = NestedList(["v"])
        self.assertEqual(repr(a), "NestedList(['v'])")
    
    # __eq__
    
    def test___eq____returns_True(self):
        a1 = NestedList(["v"])
        a2 = NestedList(["v"])
        self.assertTrue(a1 == a2)
    
    def test___eq____same_class__returns_False(self):
        a1 = NestedList(["foo"])
        a2 = NestedList(["bar"])
        self.assertFalse(a1 == a2)
    
    def test___eq____different_class__returns_True(self):
        a1 = NestedList(["v"])
        a2 = ["v"]
        self.assertTrue(a1 == a2)
    
        a3 = NestedList()
        a4 = []
        self.assertTrue(a3 == a4)
    
    # __ne__
    
    def test___ne____returns_True(self):
        a1 = NestedList(["foo"])
        a2 = NestedList(["bar"])
        self.assertTrue(a1 != a2)
    
    def test___ne____returns_False(self):
        a1 = NestedList(["v"])
        a2 = NestedList(["v"])
        self.assertFalse(a1 != a2)
    
    # __hash__
    
    def test___hash__(self):
        a1 = hash(NestedList(["v"]))
        a2 = hash(NestedList(["v"]))
        self.assertTrue(a1 == a2)
    
    # __iter__
    
    def test___iter__(self):
        a = NestedList(["v"])
        for v in a:
            self.assertEqual(v, "v")
    
    # __contains__
    
    def test___contains__(self):
        a = NestedList(["v"])
        self.assertTrue("v" in a)
    
    # __getitem__
    
    def test___getitem__int_arg__returns_value(self):
        a = NestedList(["v"])
        self.assertEqual(a[ListIndex(0)], "v")
    
    def test___getitem__delimited_tuple_arg__returns_value(self):
        a = NestedList([[["v"]]])
        self.assertEqual(a[(ListIndex(0), ListIndex(0), ListIndex(0))], "v")
    
    # __setitem__
    
    def test___setitem__string_arg__sets_value(self):
        a = NestedList(["v"])
        a[ListIndex(0)] = "foo"
        self.assertEqual(a, ["foo"])
    
    def test___setitem__delimited_string_arg__sets_value(self):
        a = NestedList([[["v"]]])
        a[(ListIndex(0), ListIndex(0), ListIndex(0))] = "foo"
        self.assertEqual(a.data, [[["foo"]]])
    
    # __delitem__
    
    def test___delitem__string_arg__deletes_value(self):
        a = NestedList(["v"])
        del a[ListIndex(0)]
        self.assertEqual(a.data, [])
    
    def test___delitem__delimited_string_arg__deletes_value(self):
        a = NestedList([[["v"]]])
        del a[(ListIndex(0), ListIndex(0), ListIndex(0))]
        self.assertEqual(a.data, [[[]]])
    
    # __len__
    
    def test___len__(self):
        a = NestedList(["v"])
        self.assertEqual(len(a), 1)
    
    # __copy__
    
    def test___copy__(self):
        a1 = NestedList([[["foo"]]])
        a2 = copy.copy(a1)
        self.assertIsNot(a1, a2)
        self.assertEqual(a1, a2)
        a1.set((ListIndex(0), ListIndex(0), ListIndex(0)), "bar")
        self.assertEqual(a1, a2)
    
    # __deepcopy__
    
    def test___deepcopy__(self):
        a1 = NestedList([[["foo"]]])
        a2 = copy.deepcopy(a1)
        self.assertIsNot(a1, a2)
        self.assertEqual(a1, a2)
        a1.data[0][0][0] = "bar"
        self.assertNotEqual(a1, a2)
    
    # ref
    
    def test_ref__no_arg__returns_all_attributes(self):
        a = NestedList(["v"])
        self.assertEqual(a.ref(), ["v"])
    
    def test_ref__string_arg__returns_value(self):
        a = NestedList(["v"])
        self.assertEqual(a.ref(ListIndex(0)), "v")
    
    def test_ref___raises_IndexError(self):
        a = NestedList()
        with self.assertRaises(IndexError):
            a.ref(ListIndex(0))
    
    def test_ref__long_path_arg__raises_ValueError(self):
        a = NestedList([["v"]])
        with self.assertRaises(IndexError):
            print(a.ref((ListIndex(0), ListIndex(1))))
    
    def test_ref__delimited_arg__returns_value(self):
        a = NestedList([[["v"]]])
        self.assertEqual(a.ref((ListIndex(0), ListIndex(0), ListIndex(0))), "v")
    
    def test_ref__True_create_arg_key_missing__creates_missing_containers(self):
        a = NestedList()
        a.ref((ListIndex(0), ListIndex(0)), create=True)
        self.assertEqual(a.data, [[[]]])
    
    # get
    
    def test_get__string_arg__returns_value(self):
        a = NestedList(["v"])
        self.assertEqual(a.get(0), "v")
    
    def test_get__string_arg_missing_key__returns_default_value(self):
        a = NestedList()
        self.assertEqual(a.get(0, "foo"), "foo")
    
    def test_get__string_arg__raises_IndexError(self):
        a = NestedList()
        with self.assertRaises(IndexError):
            a.get(0)
    
    def test_get__string_arg__raises_IndexError(self):
        a = NestedList([["v"]])
        with self.assertRaises(IndexError):
            a.get((ListIndex(0), ListIndex(0), ListIndex(1)))
    
    def test_get__path_arg__returns_value(self):
        a = NestedList([[["v"]]])
        self.assertEqual(a.get((ListIndex(0), ListIndex(0), ListIndex(0))), "v")
    
    # has
    
    def test_has__returns_True(self):
        self.assertTrue(NestedList(["v"]).has())
    
    def test_has__returns_False(self):
        self.assertFalse(NestedList().has())
    
    def test_has__path_arg__returns_True(self):
        a = NestedList([[["v"]]])
        self.assertTrue(a.has((ListIndex(0), ListIndex(0), ListIndex(0))))
    
    def test_has__path_arg__returns_False(self):
        a = NestedList([[["v"]]])
        self.assertFalse(a.has((ListIndex(1),)))
    
    # copy
    
    def test_copy(self):
        a1 = NestedList([[["v"]]])
        a2 = a1.copy()
        self.assertEqual(a1, a2)
        a1[ListIndex(0)] = "foo"
        self.assertNotEqual(a1, a2)
    
    # clone
    
    def test_clone(self):
        a1 = NestedList([[["v"]]])
        a2 = a1.clone()
        self.assertEqual(a1, a2)
        a1[ListIndex(0)] = "foo"
        self.assertEqual(a1, a2)
    
    # set
    
    def test_set__index_arg(self):
        a = NestedList(["foo"])
        a.set(ListIndex(0), "bar")
        self.assertEqual(a, ["bar"])
    
    def test_set__path_arg(self):
        a = NestedList([[["foo"]]])
        a.set((ListIndex(0), ListIndex(0), ListIndex(0)), "bar")
        self.assertEqual(a, [[["bar"]]])
    
    def test_set__raises_TypeError(self):
        a = NestedList([["foo"]])
        with self.assertRaises(TypeError):
            a.set((ListIndex(0), ListIndex(0), ListIndex(0)), "bar", create=False)
    
    # push
    
    def test_push__index_arg(self):
        a = NestedList([["foo"]])
        a.push(ListIndex(0), "bar")
        self.assertEqual(a, [["foo", "bar"]])
    
    def test_push__index_arg__convert_existing_value(self):
        a = NestedList(["foo"])
        a.push(ListIndex(0), "bar")
        self.assertEqual(a, [["foo", "bar"]])
    
    def test_push__path_arg(self):
        a = NestedList([[["foo"]]])
        a.push((ListIndex(0), ListIndex(0)), "bar")
        self.assertEqual(a, [[["foo", "bar"]]])
    
    def test_push__True_create_arg__creates_list(self):
        a = NestedList([[]])
        a.push(ListIndex(0), "bar")
        self.assertEqual(a, [["bar"]])
    
    def test_push__False_create_arg__raises_IndexError(self):
        a = NestedList()
        with self.assertRaises(IndexError):
            a.push(ListIndex(0), "foo", create=False)
    
    def test_push__False_create_arg__raises_TypeError(self):
        a = NestedList(["foo"])
        with self.assertRaises(AttributeError):
            a.push(ListIndex(0), "bar", create=False)
    
    # pull
    
    def test_pull__index_arg(self):
        a = NestedList([["foo"]])
        a.pull(ListIndex(0), "foo")
        self.assertEqual(a, [[]])
    
    def test_pull__cleanup_arg_True__removes_empty_containers(self):
        a = NestedList([[["v"]]])
        a.pull((ListIndex(0), ListIndex(0)), "v", cleanup=True)
        self.assertEqual(a, [[]])
    
    def test_pull__path_arg___raises_IndexError(self):
        a = NestedList()
        with self.assertRaises(IndexError):
            a.pull(ListIndex(0), "v")
    
    def test_pull__path_arg__raises_ValueError(self):
        a = NestedList([["foo"]])
        with self.assertRaises(ValueError):
            a.pull(ListIndex(0), "bar")
    
    def test_pull__path_arg__raises_TypeError(self):
        a = NestedList(["v"])
        with self.assertRaises(TypeError):
            a.pull((ListIndex(0), ListIndex(0)), "v")
    
    # unset
    
    def test_unset__path_arg(self):
        a = NestedList([[["v"]]])
        a.unset((ListIndex(0), ListIndex(0)))
        self.assertEqual(a, [[]])
    
    def test_unset__cleanup_arg_True__removes_empty_containers(self):
        a = NestedList([[["v"]]])
        a.unset((ListIndex(0), ListIndex(0)), cleanup=True)
        self.assertEqual(a, [])
    
    def test_unset__path_arg__raises_IndexError(self):
        a = NestedList([[["v"]]])
        with self.assertRaises(IndexError):
            a.unset((ListIndex(1), ListIndex(0)))
    
    # # merge
    # 
    # def test_merge__dict_param(self):
    #     a = NestedDict({("k1",): "v"})
    #     b = a.merge({("k2",): "v"})
    #     self.assertEqual(b, {"k1": "v", "k2": "v"})
    
    # def test_merge__nested_data__nested_data_param(self):
    #     a = NestedDict({"k1": {"k2": "v"}})
    #     b = a.merge({"k1": {"k3": "v"}})
    #     self.assertEqual(b, {"k1": {"k2": "v", "k3": "v"}})
    # 
    # def test_merge__NestedDict_param(self):
    #     a = NestedDict({("k1",): "v"})
    #     b = a.merge(NestedDict({("k2",): "v"}))
    #     self.assertEqual(b, {"k1": "v", "k2": "v"})
    # 
    # def test_merge__incompatible_types(self):
    #     a = NestedDict({("k1,"): "v"})
    #     b = a.merge("foo")
    #     self.assertEqual(b, "foo")
    # 
    # # update
    # 
    # def test_update__dict_param(self):
    #     a = NestedDict({("k1",): "v"})
    #     a.update({("k2",): "v"})
    #     self.assertEqual(a, {
    #         "k1": "v",
    #         "k2": "v"
    #     })
    # 
    # def test_update__NestedDict_param(self):
    #     a = NestedDict({("k1",): "v"})
    #     a.update(NestedDict({("k2",): "v"}))
    #     self.assertEqual(a, {
    #         "k1": "v",
    #         "k2": "v"
    #     })
    # 
    # # collapse
    # 
    # def test_collapse(self):
    #     a = NestedDict({("k1",): {("k2",): {("k3",): "v"}}})
    #     b = a.collapse()
    #     self.assertEqual(b, {("k1", "k2", "k3"): "v"})
    # 
    # def test_collapse__function_param(self):
    #     a = NestedDict({("k1", "k2", "$foo", "k3", "k4"): "v"})
    # 
    #     def detect_mongo_operator(path, value):
    #         return path[0] == "$"
    # 
    #     b = a.collapse(func=detect_mongo_operator)
        # self.assertEqual(b, {("k1", "k2"): {"$foo": {("k3", "k4"): "v"}}})


if __name__ == "__main__":
    unittest.main()
