#!/usr/bin/env python3

import unittest
import read_temperature

class TestReadTemperature(unittest.TestCase):
    
    def test_convert_hex_to_celsius(self):
        # arrange
        hex_values = [0x0017, 0x8017, 0x80FF, 0x00E7]
        ok_values = [23.0, 23.5, -0.5, -25.0]
        
        # act
        # assert
        for i in range(len(hex_values)):
            with self.subTest(i):
                result = read_temperature.convert_hex_to_celsius(hex_values[i])
                self.assertEqual(result, ok_values[i])        
        
if __name__ == '__main__':
    unittest.main()        
