def is_binary_number(a):
    a_str = str(a)
    for char in a_str:
        if char != '0' and char != '1':
            return False
    return True
def search_bin_3(a):
    is_binary = True
    a_str = str(a)
    for char in a_str:
        if char not in '01':
            is_binary = False
            break
    if is_binary:
        print(f"Число {a} - двоичное")
        return True, a
    else:
        print(f"Число {a} - не двоичное")
        return False, None

def read_numbers_from_file(filename):
    numbers = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                if ',' in line:
                    # Числа разделенные запятыми
                    parts = line.split(',')
                    for part in parts:
                        part = part.strip()
                        if part.isdigit():
                            numbers.append(int(part))
                            print(f"Строка {line_num}: прочитано число {part}")
                        else:
                            print(f"Строка {line_num}: пропущено '{part}' (не число)")
                else:
                    # Одно число на строку
                    if line.isdigit():
                        numbers.append(int(line))
                        print(f"Строка {line_num}: прочитано число {line}")
                    else:
                        print(f"Строка {line_num}: пропущено '{line}' (не число)")
                print(f"Прочитано {len(numbers)} чисел из файла")
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден")

    return numbers

def process_numbers(numbers_list):
    binary_numbers = []
    non_binary_numbers = []
    print("----------")
    print(f"Проверка чисел на двоичность")

    for number in numbers_list:
        status, binary_num = search_bin_3(number)
        if status:
            binary_numbers.append(binary_num)
        else:
            non_binary_numbers.append(number)
    print("ИТОГ")
    print(f"Всего проверено: {len(numbers_list)} чисел")
    print(f"Двоичных чисел: {len(binary_numbers)}")
    print(f"Не двоичных чисел: {len(non_binary_numbers)}")

    if binary_numbers:
        print(f"\nСписок двоичных чисел:")
        for i, num in enumerate(binary_numbers, 1):
            print(f"{i}. {num}")

    if non_binary_numbers:
        print(f"\nСписок не двоичных чисел:")
        for i, num in enumerate(non_binary_numbers, 1):
            print(f"{i}. {num}")
    return binary_numbers, non_binary_numbers

def manual_input():
    numbers = []
    print("Вводите числа по одному, завершения '-':")

    while True:
        user_input = input("Введите число: ").strip()
        if user_input.lower() == '-':
            break
        if user_input.isdigit():
            numbers.append(int(user_input))
            print(f"Добавлено число: {user_input}")
        else:
            print("Введите целое число или '-' для завершения")
    return numbers

def main():
    while True:
        print("\nВыберите источник данных:")
        print("1. Ввести числа вручную")
        print("2. Прочитать числа из файла")
        choice = input("\nВаш выбор (1-2): ").strip()
        if choice == '1':
            # Ручной ввод
            numbers = manual_input()
            if numbers:
                binary_nums, non_binary_nums = process_numbers(numbers)
                # Дополнительная информация
                if binary_nums:
                    print(
                        f"\nДвоичные числа составляют: {len(binary_nums)} от общего количества")
            else:
                print("Не введено ни одного числа")


        elif choice == '2':
            # Чтение из файла
            filename = input("\nВведите имя файла : ").strip()
            numbers = read_numbers_from_file(filename)
            if numbers:
                binary_nums, non_binary_nums = process_numbers(numbers)
                if binary_nums:
                    print(
                        f"\nДвоичные числа составляют: {len(binary_nums)} от общего количества")
            else:
                print("Не удалось прочитать числа из файла")

if __name__ == "__main__":
    main()