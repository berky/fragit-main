"""
**********************************************************************
tests/test_util.py - test cases for util.py

Copyright (C) 2011 Casper Steinmann

This file is part of the FragIt project.

FragIt is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

FragIt is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
02110-1301, USA.
***********************************************************************/
"""
import os
import unittest
import util

class TestUtilModule(unittest.TestCase):

    def setUp(self):
        self.btrue = True
        self.bfalse = False

        self.ione = 1
        self.fone = 1.0
        self.isix = 6

        self.lsimple = range(self.ione, self.isix)
        self.tsimple = tuple(self.lsimple)
        self.ssimple = "lorem ipsum dolor."
        self.dsimple = {'a':'value','b':'myvalue'}

    def delete_file(self,filename):
        try:
                f = open(filename)
        except IOError:
                return
        finally:
                f.close()
                os.remove(filename)

    def test_file_exists(self):
        self.assertRaises(TypeError, util.file_exists, self.ione)
        self.assertRaises(TypeError, util.file_exists, self.fone)
        self.assertRaises(TypeError, util.file_exists, self.btrue)
        self.assertRaises(TypeError, util.file_exists, self.tsimple)
        self.assertRaises(TypeError, util.file_exists, self.lsimple)

        self.assertFalse( util.file_exists("temp") )
        f = open("temp","w")
        f.write("")
        f.close()
        self.assertTrue( util.file_exists("temp") )
        self.delete_file("temp")

    def test_file_extension(self):
        self.assertRaises(TypeError, util.file_extension, self.ione)
        self.assertRaises(TypeError, util.file_extension, self.fone)
        self.assertRaises(TypeError, util.file_extension, self.btrue)
        self.assertRaises(TypeError, util.file_extension, self.tsimple)
        self.assertRaises(TypeError, util.file_extension, self.lsimple)

	teststring1 = "file.txt"
	self.assertEqual(util.file_extension(teststring1), ".txt")

	teststring2 = "/home/user/file2.ext"
	self.assertEqual(util.file_extension(teststring2), ".ext")

    def test_file_basename(self):
        self.assertRaises(TypeError, util.file_basename, self.ione)
        self.assertRaises(TypeError, util.file_basename, self.fone)
        self.assertRaises(TypeError, util.file_basename, self.btrue)
        self.assertRaises(TypeError, util.file_basename, self.tsimple)
        self.assertRaises(TypeError, util.file_basename, self.lsimple)

	teststring1 = "file.txt"
	self.assertEqual(util.file_basename(teststring1), "file")

	teststring2 = "/home/user/file2.ext"
	self.assertEqual(util.file_basename(teststring2), "file2")

    def test_isEqual_integer(self):
        answer1 = util.isEqual(self.ione, self.isix)
        answer2 = util.isEqual(self.isix, self.ione)
        self.assertEqual( answer1, answer2 )

    def test_TupleToStringTypeRepresentation(self):
        self.assertRaises(TypeError, util.TupleToStringTypeRepresentation, self.ione)
        self.assertRaises(TypeError, util.TupleToStringTypeRepresentation, self.fone)

        test_tuple = (self.ione, self.isix)
        answer1 = util.TupleToStringTypeRepresentation( test_tuple )
        self.assertEqual( answer1, "Int: 1, Int: 6")
        
    def test_toString(self):
        # we check several things here
        self.assertEqual( util.toString(self.ione), "Int: 1")
        self.assertEqual( util.toString(self.fone), "Float: 1.0")
        self.assertEqual( util.toString(self.lsimple), "List: [1, 2, 3, 4, 5]")

        # the odd case of None type
        self.assertEqual( util.toString(None), "None: None" )

    def test_toList(self):
        self.assertEqual( util.toList( self.lsimple ), self.lsimple )
        self.assertEqual( util.toList( self.tsimple ), self.lsimple )
        self.assertEqual( util.toList( "123" ), ['1','2','3'] )

    def test_is_int(self):
        self.assertTrue( util.is_int(self.ione))

    def test_is_float(self):
        self.assertTrue( util.is_float(self.fone))

    def test_is_list(self):
        self.assertTrue( util.is_list(self.lsimple))

    def test_is_string(self):
        self.assertTrue( util.is_string(self.ssimple))

    def test_is_bool(self):
        self.assertTrue( util.is_bool(self.btrue))
        self.assertTrue( util.is_bool(self.bfalse))

    def test_is_tuple(self):
        self.assertTrue( util.is_tuple(self.tsimple))

    def test_is_dictionary(self):
        self.assertTrue( util.is_dictionary(self.dsimple))

    def test_Uniqify(self):
        self.assertRaises( TypeError, util.Uniqify, self.ione )
        self.assertRaises( TypeError, util.Uniqify, self.fone )
        self.assertRaises( TypeError, util.Uniqify, self.btrue )
        self.assertRaises( TypeError, util.Uniqify, self.ssimple )
        self.assertEqual( util.Uniqify( self.lsimple ), self.lsimple )
        self.assertEqual( util.Uniqify( [1,2,2,3,4,5,5] ), self.lsimple )

    def test_maximum_value(self):
        # returns the maximum value of the list, be it positive or negative
        self.assertRaises( TypeError, util.maximum_value, self.ione )
        self.assertRaises( TypeError, util.maximum_value, self.fone )
        self.assertRaises( TypeError, util.maximum_value, self.btrue )
        self.assertRaises( TypeError, util.maximum_value, self.ssimple )
        test_array = [1,2,3,5,9]
        self.assertEqual(util.maximum_value(test_array), 9)
        test_array = [1,2,3,5,-9]
        self.assertEqual(util.maximum_value(test_array), -9)
        self.assertEqual(util.maximum_value([]),0)

    def test_uniqifyListOfLists(self):
        test_array = [[1,2,3,4],[5,2,3,4],[1,2,3,4]]
        self.assertEqual( util.uniqifyListOfLists( test_array ), [[1,2,3,4],[5,2,3,4]] )

    def test_ravel2D(self):
        test_array = []
        self.assertEqual( util.ravel2D( test_array ), [] )

    def test_ravel2D(self):
        test_array = [[1,2,3,4],[1,2,3,4]]
        self.assertEqual( util.ravel2D( test_array ), [1,2,3,4,1,2,3,4] )

    def test_ravel2DOddSize(self):
        test_array = [[1,2,3,4],[1,2,3,4,5]]
        self.assertEqual( util.ravel2D( test_array ), [1,2,3,4,1,2,3,4,5] )

    def test_ravel2DEmptySublists(self):
        test_array = [[1,2,3,4],[],[1,2,3,4]]
        self.assertEqual( util.ravel2D( test_array ), [1,2,3,4,1,2,3,4] )

    def test_deepLength(self):
        test_array = [[1,2,3,4],[1,2,3,4]]
        self.assertEqual( util.deepLength(test_array), 8 )

    def test_listDiff(self):
        test_array1 = range(10)
        test_array2 = range(3,7)
        self.assertEqual( util.listDiff( test_array1, test_array2 ), [0,1,2,7,8,9] )
        self.assertRaises( ValueError, util.listDiff, test_array2, test_array1 )

    def test_lenOfLists(self):
        test_array = [[1,2,3,4],[1,2,3,4],[5,4,3,2,1]]
        # returns a list of the individual sub lists
        self.assertEqual( util.lenOfLists(test_array), [4,4,5] )

    def test_listTo2D(self):
        # check empty, it should return the correct dimension still
        test_array = []
        final_array = [[]]
        self.assertEqual( util.listTo2D( test_array, 5 ), final_array )

        test_array = range(20)
        final_array = [[0,1,2,3,4],[5,6,7,8,9],[10,11,12,13,14],[15,16,17,18,19]]
        self.assertEqual( util.listTo2D(test_array, 5), final_array)

        # test the odd sized conversion too
        test_array = range(19)
        final_array = [[0,1,2,3,4],[5,6,7,8,9],[10,11,12,13,14],[15,16,17,18]]
        self.assertEqual( util.listTo2D(test_array, 5), final_array)

    def test_join2D(self):
        test_array = [['a','b','c'],['ab','cd','ef']]
        self.assertEqual( util.join2D( test_array, "|", "--"), 'a|b|c--ab|cd|ef')

        test_array = [['1','2',4],['1','2','5']]
        self.assertRaises( TypeError, util.join2D, test_array, "|", "--" )

    def test_joinIntList(self):
        self.assertRaises(TypeError, util.joinIntList, "", self.ione)
        self.assertRaises(TypeError, util.joinIntList, "", self.fone)
        self.assertRaises(TypeError, util.joinIntList, "", self.btrue)
        self.assertRaises(TypeError, util.joinIntList, "", self.ssimple)
        self.assertRaises(TypeError, util.joinIntList, "", [1.0,2.3])
        test_array1 = [1,2,3]
        self.assertEqual(util.joinIntList("",test_array1),"123")
        self.assertEqual(util.joinIntList(",",test_array1),"1,2,3")

    def test_intlistToString(self):
        self.assertRaises(TypeError, util.intlistToString, self.ione)
        self.assertRaises(TypeError, util.intlistToString, self.fone)
        self.assertRaises(TypeError, util.intlistToString, self.btrue)
        self.assertRaises(TypeError, util.intlistToString, self.ssimple)
        test_array1 = [1,2,3]
        self.assertEqual(util.intlistToString(test_array1),"1,2,3")

    def test_intlistFromString(self):
        self.assertRaises(TypeError, util.intlistFromString, self.ione)
        self.assertRaises(TypeError, util.intlistFromString, self.fone)
        self.assertRaises(TypeError, util.intlistFromString, self.btrue)
        self.assertRaises(TypeError, util.intlistFromString, self.tsimple)
        self.assertRaises(TypeError, util.intlistFromString, self.lsimple)
        self.assertEqual(util.intlistFromString(""),[])
        self.assertEqual(util.intlistFromString("1,2,3"),[1,2,3])
        self.assertEqual(util.intlistFromString("-1,2,3"),[-1,2,3])

    def test_floatlistToString(self):
        self.assertRaises(TypeError, util.floatlistFromString, self.ione)
        self.assertRaises(TypeError, util.floatlistFromString, self.fone)
        self.assertRaises(TypeError, util.floatlistFromString, self.btrue)
        self.assertRaises(TypeError, util.floatlistFromString, self.tsimple)
        self.assertRaises(TypeError, util.floatlistFromString, self.lsimple)
        self.assertEqual(util.floatlistFromString(""),[])
        self.assertEqual(util.floatlistFromString("1.0,2.0,3.0"),[1.0,2.0,3.0])
        self.assertEqual(util.floatlistFromString("-1.0,2.0,3.0"),[-1.0,2.0,3.0])

    def test_listOfDoubleIntTupleToString(self):
        self.assertEqual(util.listOfDoubleIntTupleToString( [(1,2),(3,4)] ), "(1,2);(3,4)")

    def test_listOfDoubleIntTupleFromString(self):
        self.assertRaises(TypeError, util.listOfDoubleIntTupleFromString, self.ione)
        self.assertRaises(TypeError, util.listOfDoubleIntTupleFromString, self.fone)
        self.assertRaises(TypeError, util.listOfDoubleIntTupleFromString, self.btrue)
        self.assertRaises(TypeError, util.listOfDoubleIntTupleFromString, self.tsimple)
        self.assertRaises(TypeError, util.listOfDoubleIntTupleFromString, self.lsimple)
        self.assertEqual(util.listOfDoubleIntTupleFromString("(1,2);(3,4)"), [(1,2),(3,4)])

    def test_isStringList(self):
        self.assertRaises(TypeError, util.isStringList, self.ione)
        self.assertRaises(TypeError, util.isStringList, self.fone)
        self.assertRaises(TypeError, util.isStringList, self.btrue)
        self.assertRaises(TypeError, util.isStringList, self.tsimple)
        self.assertRaises(TypeError, util.isStringList, self.ssimple)
        test_array = ['a','2','cv']
        self.assertEqual( util.isStringList( test_array ), True )
        test_array = [['1','f'],['3','5']]
        self.assertEqual( util.isStringList( test_array ), True )
        test_array = [['1','f'],['3',5]]
        self.assertEqual( util.isStringList( test_array ), False )

    def test_isIntegerList(self):
        self.assertRaises(TypeError, util.isIntegerList, self.ione)
        self.assertRaises(TypeError, util.isIntegerList, self.fone)
        self.assertRaises(TypeError, util.isIntegerList, self.btrue)
        self.assertRaises(TypeError, util.isIntegerList, self.ssimple)

        test_array = [1,2,3]
        self.assertEqual( util.isIntegerList( test_array ), True )

        test_array = [[2,4],[5,1]]
        self.assertEqual( util.isIntegerList( test_array ), True )

        test_array = [['1',2],[4,5]]
        self.assertEqual( util.isIntegerList( test_array ), False )

        test_array = [[1.0,2],[4,5]]
        self.assertEqual( util.isIntegerList( test_array ), False )

    def test_WriteStringToFile(self):
        test_string="Hello World"
        test_filename="test.dat"
        util.WriteStringToFile(test_filename, test_string)
        f = open(test_filename,'r')
        read_string = f.read()
        f.close()
        self.assertEqual( read_string, test_string )

        # only strings can be written
        self.assertRaises(TypeError, util.WriteStringToFile, test_filename, self.ione)
        self.assertRaises(TypeError, util.WriteStringToFile, test_filename, self.fone)
        self.assertRaises(TypeError, util.WriteStringToFile, test_filename, self.btrue)
        self.assertRaises(TypeError, util.WriteStringToFile, test_filename, self.tsimple)
        self.assertRaises(TypeError, util.WriteStringToFile, test_filename, self.lsimple)

        # filename must be a string
        self.assertRaises(TypeError, util.WriteStringToFile, self.ione, test_string)
        self.assertRaises(TypeError, util.WriteStringToFile, self.fone, test_string)
        self.assertRaises(TypeError, util.WriteStringToFile, self.btrue, test_string)
        self.assertRaises(TypeError, util.WriteStringToFile, self.tsimple, test_string)
        self.assertRaises(TypeError, util.WriteStringToFile, self.lsimple, test_string)

        self.delete_file(test_filename)

    def test_WriteStringListToFile(self):
        test_list=['Hello World','Welcome Home']
        test_string="Hello World\nWelcome Home\n"
        test_filename="test.dat"
        util.WriteStringListToFile(test_filename, test_list)
        f = open(test_filename,'r')
        read_string = f.read()
        f.close()
        self.assertEqual( read_string, test_string )

        # only lists can be written
        self.assertRaises(TypeError, util.WriteStringListToFile, test_filename, self.ione)
        self.assertRaises(TypeError, util.WriteStringListToFile, test_filename, self.fone)
        self.assertRaises(TypeError, util.WriteStringListToFile, test_filename, self.btrue)
        self.assertRaises(TypeError, util.WriteStringListToFile, test_filename, self.tsimple)
        self.assertRaises(TypeError, util.WriteStringListToFile, test_filename, self.ssimple)
        self.assertRaises(TypeError, util.WriteStringListToFile, test_filename, self.dsimple)

        # filename must be a string
        self.assertRaises(TypeError, util.WriteStringListToFile, self.ione, test_string)
        self.assertRaises(TypeError, util.WriteStringListToFile, self.fone, test_string)
        self.assertRaises(TypeError, util.WriteStringListToFile, self.btrue, test_string)
        self.assertRaises(TypeError, util.WriteStringListToFile, self.tsimple, test_string)
        self.assertRaises(TypeError, util.WriteStringListToFile, self.lsimple, test_string)
        self.assertRaises(TypeError, util.WriteStringListToFile, self.dsimple, test_string)

        self.delete_file(test_filename)

    def test_ReadStringFromFile(self):
        test_string="Hello World"
        test_filename="test.dat"
        f = open(test_filename,'w')
        f.write(test_string)
        f.close()
        read_string = util.ReadStringFromFile(test_filename)
        self.assertEqual( read_string, test_string )
        # filename must be a string
        self.assertRaises(TypeError, util.ReadStringFromFile, self.ione)
        self.assertRaises(TypeError, util.ReadStringFromFile, self.fone)
        self.assertRaises(TypeError, util.ReadStringFromFile, self.btrue)
        self.assertRaises(TypeError, util.ReadStringFromFile, self.tsimple)
        self.assertRaises(TypeError, util.ReadStringFromFile, self.lsimple)
        self.assertRaises(TypeError, util.ReadStringFromFile, self.dsimple)
        self.delete_file(test_filename)
        
    def test_ReadStringListFromFile(self):
        test_string="Hello World\nWelcome Home"
        test_list=["Hello World","Welcome Home"]
        test_filename="test.dat"
        f = open(test_filename,'w')
        f.write(test_string)
        f.close()
        read_list = util.ReadStringListFromFile(test_filename)
        self.assertEqual( read_list, test_list )
        # filename must be a string
        self.assertRaises(TypeError, util.ReadStringListFromFile, self.ione)
        self.assertRaises(TypeError, util.ReadStringListFromFile, self.fone)
        self.assertRaises(TypeError, util.ReadStringListFromFile, self.btrue)
        self.assertRaises(TypeError, util.ReadStringListFromFile, self.tsimple)
        self.assertRaises(TypeError, util.ReadStringListFromFile, self.lsimple)
        self.assertRaises(TypeError, util.ReadStringListFromFile, self.dsimple)
        self.delete_file(test_filename)

    def test_tupleValuesInEitherList(self):
        list1 = [1,2,3,4]
        list2 = [5,6,7,8]
        self.assertEqual(util.tupleValuesInEitherList((1,5),list1,list2),True)
        self.assertEqual(util.tupleValuesInEitherList((5,1),list1,list2),True)
        self.assertEqual(util.tupleValuesInEitherList((1,9),list1,list2),False)
        self.assertEqual(util.tupleValuesInEitherList((6,9),list1,list2),False)

    def test_listToRanges(self):
        list1 = range(1,10)
        self.assertEqual(util.listToRanges(list1),[(1,9)])
        list2 = [1,2] + range(5,10)
        self.assertEqual(util.listToRanges(list2),[1,2,(5,9)])
        list3 = [1,2,3] + range(5,10)
        self.assertEqual(util.listToRanges(list3),[(1,3),(5,9)])
        list4 = [1,2,4] + range(7,10)
        self.assertEqual(util.listToRanges(list4),[1,2,4,(7,9)])
        list5 = [2,3] + range(5,9) + [12,13] + range(15,20) + [31]
        self.assertEqual(util.listToRanges(list5),[2,3,(5,8),12,13,(15,19),31])
        list6 = [2,3] + range(5,9) + [12,13] + range(15,20) + [31,32]
        self.assertEqual(util.listToRanges(list6),[2,3,(5,8),12,13,(15,19),31,32])

def suite():
  s = unittest.TestSuite()
  s.addTest(unittest.makeSuite(TestUtilModule))
  return s

if __name__ == '__main__':
  unittest.main()
