import SpectrumImage
import unittest
import collections
import numpy as np
import traceback

class DictifierTest(unittest.TestCase):

	def testDictifyOneLevel(self):
		self.assertEqual(SpectrumImage.make_dict_from_tags(['root = 65']),
                     {'root': '65'})
                     
	def testDictifyMultipleValues(self):
		self.assertEqual(SpectrumImage.make_dict_from_tags(['foo = 12', 'bar = 16']),
                     {'foo': '12', 'bar': '16'})

	def testDictifyMultipleLevels(self):
		self.assertEqual(SpectrumImage.make_dict_from_tags(['root.foo.bar = 12']),
                     {'root': {'foo': {'bar': '12'}}})

	def testDictifyCollision(self):
		self.assertEqual(SpectrumImage.make_dict_from_tags(['bar = 10', 'bar = 12']),
					{'bar': '10'})

	def testDictifyEmptyValue(self):
		self.assertEqual(SpectrumImage.make_dict_from_tags(['root = ']), 
					{'root': ''})

class EELSSpectrumImageTest(unittest.TestCase):
	
	def assertArraysEqual(self, array1, array2):
		self.assertTrue(np.array_equal(array1, array2), 'Arrays are not equal')
	
	def testInitECalibrationZLP(self):
		try:
			eels = SpectrumImage.EELSSpectrumImage(self.data, ZLP=True, dispersion=0.3, SpectrumRange=None, channel_eV=None)
		except ValueError:
			self.fail("Got value error, didn't want one anyway")
		self.assertEqual(eels.dispersion, 0.3)
		self.assertTrue(eels.ZLP)
		self.assertArraysEqual(eels.data, self.data)
		
	def testInitECalibrationZLPnoDispersion(self):
		with self.assertRaisesRegexp(ValueError, 'Dispersion needs to be a real number!'):
			eels = SpectrumImage.EELSSpectrumImage(self.data, ZLP=True, SpectrumRange=None, dispersion=None, channel_eV=None)

	def testZLPandSpectrumRange(self):
		with self.assertRaisesRegexp(ValueError, "You don't need to define a SpectrumRange and ZLP/dispersion!"):
			eels = SpectrumImage.EELSSpectrumImage(self.data, ZLP=True, SpectrumRange=np.array([0, 1, 2, 4, 5]), dispersion=0.3, channel_eV=None)
			
	def testInitECalibrationSpectrumRange(self): 
		try:
			eels = SpectrumImage.EELSSpectrumImage(self.data, ZLP=False, dispersion=None, SpectrumRange=np.array([0, 1, 2, 3, 4]), channel_eV=None)
		except ValueError:
			self.fail("Got value error, didn't want one anyway " + traceback.format_exc())
		self.assertEqual(eels.dispersion, 1)
		self.assertArraysEqual(eels.SpectrumRange, np.array([0, 1, 2, 3, 4]))
			
	def testSpectrumRangeWrongLength(self):
		with self.assertRaisesRegexp(ValueError, "Your SpectrumRange is not the same size as your energy axis!"):
			eels = SpectrumImage.EELSSpectrumImage(self.data, ZLP=False, SpectrumRange=np.array([0, 1, 2, 4]), dispersion=None, channel_eV=None)

	def testInitECalibrationChanneleV(self):
		try:
			eels = SpectrumImage.EELSSpectrumImage(self.data, ZLP=False, dispersion=0.3, SpectrumRange=None, channel_eV=[2, 0.5])
		except ValueError:
			self.fail("Got value error, didn't want one anyway")
		self.assertEqual(eels.dispersion, 0.3)
		self.assertAlmostEqual(eels.SpectrumRange[2], 0.5)
		self.assertArraysEqual(eels.data, self.data)

	def testInitECalibrationChanneleVwrong(self):
		with self.assertRaisesRegexp(ValueError, 'channel_eV must have length 2!'):
			eels = SpectrumImage.EELSSpectrumImage(self.data, ZLP=False, SpectrumRange=None, dispersion=0.3, channel_eV=[2, 0.5, 1])
				
	def testInitECalibrationChanneleVnoDispersion(self):
		with self.assertRaisesRegexp(ValueError, 'Dispersion needs to be a real number!'):
			eels = SpectrumImage.EELSSpectrumImage(self.data, ZLP=False, SpectrumRange=None, dispersion=None, channel_eV=[2, 0.5])

	def testInitECalibrationNone(self):
		with self.assertRaisesRegexp(ValueError, 'You need to input an energy calibration!'):
			eels = SpectrumImage.EELSSpectrumImage(self.data, ZLP=False, SpectrumRange=None, dispersion=None, channel_eV=None)

	def setUp(self):
		self.data = np.arange(20).reshape(2,2,5)

if __name__ == '__main__':
	unittest.main()					
