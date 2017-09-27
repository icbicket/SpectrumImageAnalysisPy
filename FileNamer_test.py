import unittest
import FileNamer

class FindLastFilenameTest(unittest.TestCase):
	def testfilenumber0(self):
		filename = 'testfolder/test/testfile.csv'
		new_filename = FileNamer.NameFile(filename)
		self.assertEqual('testfolder/test/testfile-11.csv', new_filename)

	def testdifffile(self):
		filename = 'testfolder/test/differentname.csv'
		new_filename = FileNamer.NameFile(filename)
		self.assertEqual('testfolder/test/differentname.csv', new_filename)

	def testfilenumber1(self):
		filename = 'testfolder/test/testfile1.csv'
		new_filename = FileNamer.NameFile(filename)
		self.assertEqual('testfolder/test/testfile1-1.csv', new_filename)


class NumberFileNamesTest(unittest.TestCase):
	def testfilenumber1(self):
#		Test numbering of first string
		filename = 'stuff.csv'
		new_filename = FileNamer.NumberFileNames(filename)
		self.assertEqual('stuff-1.csv', new_filename)
		
	def testfilenumber2(self):
#		Test sequential numbering
		filename = 'stuff-1.csv'
		new_filename = FileNamer.NumberFileNames(filename)
		self.assertEqual('stuff-2.csv', new_filename)
		
	def testfilenumber10(self):
#		Test sequential numbering with two digits
		filename = 'stuff-10.csv'
		new_filename = FileNamer.NumberFileNames(filename)
		self.assertEqual('stuff-11.csv', new_filename)
	
	def testfiledot(self):
		filename = 'test1.0.csv'
		new_filename = FileNamer.NumberFileNames(filename)
		self.assertEqual('test1.0-1.csv', new_filename)
	
	def testfolderdash1(self):
		filename = '/home/home/t-5/pvt/stuff.csv'
		new_filename = FileNamer.NumberFileNames(filename)
		self.assertEqual('/home/home/t-5/pvt/stuff-1.csv', new_filename)
		
	def testfolderdash2(self):
		filename = '/home/home/t-5/pvt/stuff-1.csv'
		new_filename = FileNamer.NumberFileNames(filename)
		self.assertEqual('/home/home/t-5/pvt/stuff-2.csv', new_filename)
		
	def testfolderdash10(self):
		filename = '/home/home/t-5/pvt/stuff-10.csv'
		new_filename = FileNamer.NumberFileNames(filename)
		self.assertEqual('/home/home/t-5/pvt/stuff-11.csv', new_filename)

	def testfolderdot1(self):
		filename = '/home/home/t5/.pvt/stuff.csv'
		new_filename = FileNamer.NumberFileNames(filename)
		self.assertEqual('/home/home/t5/.pvt/stuff-1.csv', new_filename)
		
	def testfolderdot2(self):
		filename = '/home/home/t5/.pvt/stuff-1.csv'
		new_filename = FileNamer.NumberFileNames(filename)
		self.assertEqual('/home/home/t5/.pvt/stuff-2.csv', new_filename)
		
	def testfolderdot10(self):
		filename = '/home/home/t5/.pvt/stuff-10.csv'
		new_filename = FileNamer.NumberFileNames(filename)
		self.assertEqual('/home/home/t5/.pvt/stuff-11.csv', new_filename)
		
if __name__ == '__main__':
	unittest.main()	
