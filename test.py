import unittest
from io import StringIO
from unittest.mock import patch, mock_open

# Импортируем функции напрямую из файла в той же папке
import sys
import os

sys.path.append(os.path.dirname(__file__))

from binary_checker import is_binary_number, search_bin_3, process_numbers, read_numbers_from_file, manual_input


class TestBinaryFunctions(unittest.TestCase):

    def test_1_is_binary_number_correct(self):
        """Тест 1: Корректные двоичные числа"""
        self.assertTrue(is_binary_number(101))
        self.assertTrue(is_binary_number(0))
        self.assertTrue(is_binary_number(1))
        self.assertTrue(is_binary_number(111000))
        self.assertTrue(is_binary_number(1111111111))

    def test_2_is_binary_number_incorrect(self):
        """Тест 2: Некорректные двоичные числа"""
        self.assertFalse(is_binary_number(123))
        self.assertFalse(is_binary_number(102))
        self.assertFalse(is_binary_number(999))
        self.assertFalse(is_binary_number(1002))
        self.assertFalse(is_binary_number(123456789))

    def test_3_is_binary_number_edge_cases(self):
        """Тест 3: Граничные случаи для is_binary_number"""
        # Строковый ввод
        self.assertTrue(is_binary_number("101"))
        self.assertTrue(is_binary_number("0"))
        self.assertTrue(is_binary_number("1"))
        self.assertFalse(is_binary_number("102"))
        self.assertFalse(is_binary_number("abc"))  # Не числа вообще
        self.assertFalse(is_binary_number("1a1"))  # Смесь цифр и букв
        self.assertFalse(is_binary_number("1 0"))  # С пробелом

        # Числа с ведущими нулями
        self.assertTrue(is_binary_number("001"))
        self.assertTrue(is_binary_number("0001"))

    def test_4_is_binary_number_special_cases(self):
        """Тест 4: Специальные случаи"""
        # Отрицательные числа
        self.assertFalse(is_binary_number(-101))
        self.assertFalse(is_binary_number(-1))

        # Ноль в разных форматах
        self.assertTrue(is_binary_number(0))
        self.assertTrue(is_binary_number("0"))
        self.assertTrue(is_binary_number(00))  # Два нуля

    # Тесты для search_bin_3
    def test_5_search_bin_3_binary(self):
        """Тест 5: Проверка вывода для двоичного числа"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result, value = search_bin_3(101)
            output = mock_stdout.getvalue()
            self.assertIn("Число 101 - двоичное", output)
            self.assertTrue(result)
            self.assertEqual(value, 101)

    def test_6_search_bin_3_non_binary(self):
        """Тест 6: Проверка вывода для не двоичного числа"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result, value = search_bin_3(123)
            output = mock_stdout.getvalue()
            self.assertIn("Число 123 - не двоичное", output)
            self.assertFalse(result)
            self.assertIsNone(value)

    def test_7_search_bin_3_zero_and_one(self):
        """Тест 7: Проверка граничных значений 0 и 1"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result, value = search_bin_3(0)
            output = mock_stdout.getvalue()
            self.assertIn("Число 0 - двоичное", output)
            self.assertTrue(result)
            self.assertEqual(value, 0)

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result, value = search_bin_3(1)
            output = mock_stdout.getvalue()
            self.assertIn("Число 1 - двоичное", output)
            self.assertTrue(result)
            self.assertEqual(value, 1)


    def test_8_search_bin_3_large_numbers(self):
        """Тест 8: Проверка больших чисел"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result, value = search_bin_3(111111111111)  # Большое двоичное
            output = mock_stdout.getvalue()
            self.assertIn("двоичное", output)
            self.assertTrue(result)

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result, value = search_bin_3(999999999999)  # Большое недвоичное
            output = mock_stdout.getvalue()
            self.assertIn("не двоичное", output)
            self.assertFalse(result)

    # Тесты для process_numbers
    def test_9_process_numbers_functionality(self):
        """Тест 9: Проверка работы process_numbers"""
        test_numbers = [101, 123, 0, 111, 456]
        with patch('sys.stdout', new_callable=StringIO):
            binary_nums, non_binary_nums = process_numbers(test_numbers)
            self.assertEqual(binary_nums, [101, 0, 111])
            self.assertEqual(non_binary_nums, [123, 456])

    def test_10_process_numbers_empty_list(self):
        """Тест 10: Обработка пустого списка"""
        with patch('sys.stdout', new_callable=StringIO):
            binary_nums, non_binary_nums = process_numbers([])
            self.assertEqual(binary_nums, [])
            self.assertEqual(non_binary_nums, [])

    def test_11_process_numbers_all_binary(self):
        """Тест 11: Все числа двоичные"""
        test_numbers = [101, 0, 1, 111, 1000]
        with patch('sys.stdout', new_callable=StringIO):
            binary_nums, non_binary_nums = process_numbers(test_numbers)
            self.assertEqual(binary_nums, [101, 0, 1, 111, 1000])
            self.assertEqual(non_binary_nums, [])

    def test_12_process_numbers_all_non_binary(self):
        """Тест 12: Все числа не двоичные"""
        test_numbers = [123, 456, 789, 234, 567]
        with patch('sys.stdout', new_callable=StringIO):
            binary_nums, non_binary_nums = process_numbers(test_numbers)
            self.assertEqual(binary_nums, [])
            self.assertEqual(non_binary_nums, [123, 456, 789, 234, 567])

    def test_13_process_numbers_single_element(self):
        """Тест 13: Один элемент в списке"""
        with patch('sys.stdout', new_callable=StringIO):
            # Один двоичный элемент
            binary_nums, non_binary_nums = process_numbers([101])
            self.assertEqual(binary_nums, [101])
            self.assertEqual(non_binary_nums, [])

            # Один недвоичный элемент
            binary_nums, non_binary_nums = process_numbers([123])
            self.assertEqual(binary_nums, [])
            self.assertEqual(non_binary_nums, [123])

    # Тесты для read_numbers_from_file
    def test_14_read_numbers_from_file_valid(self):
        """Тест 14: Чтение корректных данных из файла"""
        test_data = "101\n123\n0\n1\n111000"

        with patch('builtins.open', mock_open(read_data=test_data)):
            with patch('sys.stdout', new_callable=StringIO):
                numbers = read_numbers_from_file('test.txt')
                self.assertEqual(numbers, [101, 123, 0, 1, 111000])

    def test_15_read_numbers_from_file_with_commas(self):
        """Тест 15: Чтение чисел с запятыми"""
        test_data = "101, 123, 0, 1, 111000"

        with patch('builtins.open', mock_open(read_data=test_data)):
            with patch('sys.stdout', new_callable=StringIO):
                numbers = read_numbers_from_file('test.txt')
                self.assertEqual(numbers, [101, 123, 0, 1, 111000])

    def test_16_read_numbers_from_file_mixed(self):
        """Тест 16: Чтение файла со смешанным содержимым"""
        test_data = "101\nabc\n123\n45,67,89\nxyz\n999"

        with patch('builtins.open', mock_open(read_data=test_data)):
            with patch('sys.stdout', new_callable=StringIO):
                numbers = read_numbers_from_file('test.txt')
                self.assertEqual(numbers, [101, 123, 45, 67, 89, 999])


        with patch('builtins.open', mock_open(read_data=test_data)):
            with patch('sys.stdout', new_callable=StringIO):
                # Читаем числа из файла
                numbers = read_numbers_from_file('test.txt')
                self.assertEqual(numbers, [101, 123, 0, 111, 456])

                # Обрабатываем числа
                binary_nums, non_binary_nums = process_numbers(numbers)
                self.assertEqual(binary_nums, [101, 0, 111])
                self.assertEqual(non_binary_nums, [123, 456])

    # Тесты на производительность и стабильность
    def test_28_performance_large_input(self):
        """Тест 28: Обработка большого количества чисел"""
        test_numbers = [101] * 100 + [123] * 100  # 200 чисел

        with patch('sys.stdout', new_callable=StringIO):
            binary_nums, non_binary_nums = process_numbers(test_numbers)
            self.assertEqual(len(binary_nums), 100)
            self.assertEqual(len(non_binary_nums), 100)

    def test_29_special_characters(self):
        """Тест 29: Специальные символы и граничные случаи"""
        # Проверяем обработку различных входных данных
        self.assertFalse(is_binary_number("1.0"))  # Точка
        self.assertFalse(is_binary_number("1-0"))  # Дефис
        self.assertFalse(is_binary_number("1+0"))  # Плюс
        self.assertFalse(is_binary_number(" "))  # Пробел
        self.assertFalse(is_binary_number(" 1 "))  # Пробелы вокруг


if __name__ == "__main__":
    unittest.main(verbosity=2)
