import unittest
from io import StringIO
from unittest.mock import patch, mock_open

# Импортируем функции напрямую из файла в той же папке
import sys
import os

# Добавляем текущую директорию в путь Python
sys.path.append(os.path.dirname(__file__))

from binary_checker import is_binary_number, search_bin_3, process_numbers, read_numbers_from_file

class TestBinaryFunctions(unittest.TestCase):

    def test_1_is_binary_number_correct(self):
        """Тест 1: Корректные двоичные числа"""
        self.assertTrue(is_binary_number(101))
        self.assertTrue(is_binary_number(0))
        self.assertTrue(is_binary_number(1))
        self.assertTrue(is_binary_number(111000))

    def test_2_is_binary_number_incorrect(self):
        """Тест 2: Некорректные двоичные числа"""
        self.assertFalse(is_binary_number(123))
        self.assertFalse(is_binary_number(102))
        self.assertFalse(is_binary_number(999))

    def test_3_search_bin_3_binary(self):
        """Тест 3: Проверка вывода для двоичного числа"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result, value = search_bin_3(101)
            output = mock_stdout.getvalue()
            self.assertIn("Число 101 - двоичное", output)
            self.assertTrue(result)
            self.assertEqual(value, 101)

    def test_4_search_bin_3_non_binary(self):
        """Тест 4: Проверка вывода для не двоичного числа"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result, value = search_bin_3(123)
            output = mock_stdout.getvalue()
            self.assertIn("Число 123 - не двоичное", output)
            self.assertFalse(result)
            self.assertIsNone(value)

    def test_5_process_numbers(self):
        """Тест 5: Проверка работы process_numbers"""
        test_numbers = [101, 123, 0, 111, 456]
        with patch('sys.stdout', new_callable=StringIO):
            binary_nums, non_binary_nums = process_numbers(test_numbers)
            self.assertEqual(binary_nums, [101, 0, 111])
            self.assertEqual(non_binary_nums, [123, 456])

if __name__ == "__main__":
    unittest.main(verbosity=2)