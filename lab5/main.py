import random
import time
import os
import getpass
import threading

# Константа для времени бездействия
INACTIVITY_TIMEOUT = 300  # 300 секунд (5 минут)

# Функция для генерации случайной фразы
# def generate_phrase():
#     characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
#     return ''.join(random.choices(characters, k=25))

# Функция для проверки генерации случайной фразы (меняем characters и k= для разных букв и символов)
def generate_phrase():
    characters = '01'
    return ''.join(random.choices(characters, k=3))

# Функция для создания файла с фразами
def create_phrase_file():
    print("Генерация файлов со случайными фразами...")
    with open("phrases.txt", "w") as file:
        for _ in range(10):
            phrase = generate_phrase()
            file.write(f"{phrase}\n")
    print("Файлы успешно созданы.")


# Создаем файл с фразами
create_phrase_file()

# Функция для вычисления отклонения
def calculate_deviation(phrase, ideal_value):
    values = [ord(char) for char in phrase]  # Преобразование строки в список чисел
    print("\nОтклонение успешно вычислено.")
    return sum(abs(x - ideal_value) for x in values) / len(phrase)


# Функция для вычисления идеального значения
def calculate_ideal_value(phrase):
    values = [ord(char) for char in phrase]  # Преобразование строки в список чисел
    print("\nИдеальное значение успешно вычислено.")
    return sum(values) / len(phrase)

def register_user():
    username = input("Введите ваше имя пользователя: ").strip()

    # Проверяем, существует ли уже файл с пользователями
    if not os.path.exists("C:/university/3 course/2 семестр/защита информации/lab5/users.txt"):
        # Если файла нет, создаем его
        with open("C:/university/3 course/2 семестр/защита информации/lab5/users.txt", "w") as file:
            pass  # Просто создаем пустой файл

    # Проверяем, существует ли уже пользователь с таким именем
    with open("C:/university/3 course/2 семестр/защита информации/lab5/users.txt", "r") as file:
        for line in file:
            try:
                stored_username, _ = line.strip().split(":")
            except ValueError:
                # Если строку не удастся разделить правильно, мы просто игнорируем ее и переходим к следующей
                continue
            if stored_username == username:
                confirm = input("Пользователь с таким именем уже существует. Хотите перезаписать информацию? (y/n): ")
                if confirm.lower() != 'y':
                    print("Регистрация отменена.")
                    return

    # Выбираем рандомную фразу из файла и выводим её
    with open("phrases.txt", "r") as file:
        phrases = file.readlines()
        random_phrase = random.choice(phrases).strip()
        print(f"Ваша фраза для регистрации: {random_phrase}")

    # Проверяем, существует ли уже пользователь с таким именем
    with open("C:/university/3 course/2 семестр/защита информации/lab5/users.txt", "r") as file:
        for line in file:
            stored_username, _, _, _ = line.strip().split(":")
            if stored_username == username:
                print("Пользователь с таким именем уже существует.")
                return

    # Запрашиваем пароль у пользователя
    password_attempts = []
    for i in range(4):
        password = ""
        print(f"Введите пароль ({i + 1}/4) посимвольно. Для завершения ввода нажмите Enter.")
        start_time = time.time()
        while True:
            char = input("Введите символ: ")
            if char.strip() == "":  # Если символ пустой, то это означает нажатие Enter
                break  # Пользователь нажал Enter, завершаем ввод
            password += char
            elapsed_time = time.time() - start_time
            if elapsed_time > 10:  # Проверяем, превышено ли время ввода
                print("\nПревышено время ввода.")
                return
            start_time = time.time()  # Обновляем время начала ожидания после каждого ввода символа
        password_attempts.append(password)

    # Проверяем правильность введенного пароля
    if not all(attempt == random_phrase for attempt in password_attempts):
        print("\nНеверный пароль.")
        return

    # Считаем статистики
    ideal_values = []
    deviations = []
    for attempt in password_attempts:
        print(attempt, end=" ")
        ideal_value = calculate_ideal_value(attempt)
        deviation = calculate_deviation(attempt, ideal_value)
        ideal_values.append(ideal_value)
        deviations.append(deviation)

    # Считаем среднее значение идеального значения и отклонения
    avg_ideal_value = sum(ideal_values) / len(ideal_values)
    avg_deviation = sum(deviations) / len(deviations)

    # Записываем результаты в файл
    with open("users.txt", "a") as file:
        file.write(f"{username}:{random_phrase}:{avg_ideal_value}:{avg_deviation}\n")

    print("\nПользователь успешно зарегистрирован.")


# Функция для проверки аутентификации и разрешения пользователя
def check_user_permission(username, password):
    if not os.path.isfile("users.txt"):
        return False

    with open("users.txt", "r") as file:
        for line in file:
            stored_username, stored_password, stored_ideal_value, stored_deviation = line.strip().split(":")
            if stored_username == username and stored_password == password:
                return True, float(stored_ideal_value), float(stored_deviation)

    return False, None, None

def check_authentication():
    if not os.path.isfile("users.txt"):
        print("Файл с пользователями не найден. Пожалуйста, зарегистрируйтесь, если вы первый раз запускаете терминал!")
        return None
    else:
        username = input("Введите ваше имя пользователя: ")

        with open("users.txt", "r") as file:
            for line in file:
                stored_username, stored_password, stored_ideal_value, stored_deviation = line.strip().split(":")
                if stored_username == username:
                    # Выводим фразу, которую хотим ввести
                    print(f"Фраза для ввода: {stored_password}")

                    # Пользователь вводит пароль посимвольно
                    password = ""
                    start_time = time.time()
                    while True:
                        char = input("Введите символ пароля: ")
                        if char.strip() == "":
                            break  # Если ввод закончен (нажат Enter), выходим из цикла
                        password += char
                        elapsed_time = time.time() - start_time
                        if elapsed_time > 10:
                            print("\nПревышено время ввода.")
                            return None
                        start_time = time.time()

                    # Проверяем правильность ввода пароля
                    if password != stored_password:
                        print("\nНеверный пароль.")
                        return None

                    # Проверяем идеальное значение
                    epsilon = 0.1  # Значение эпсилон, можно настроить по вашему усмотрению
                    ideal_value_diff = abs(float(stored_ideal_value) - calculate_ideal_value(stored_password))
                    if ideal_value_diff > epsilon:
                        print("Не прошли проверку по идеальному значению...")
                        return None

                    # Проверяем отклонение
                    deviation_diff = abs(float(stored_deviation) - calculate_deviation(stored_password, float(stored_ideal_value)))
                    if deviation_diff > epsilon:
                        print("Не прошли проверку по отклонению...")
                        return None

                    # Если все проверки пройдены успешно, возвращаем кортеж (username, password)
                    return (username, password)

            print("\nНеверное имя пользователя.")
            return None


# Основная функция
def main():
    authenticated_user = None  # Инициализируем переменную для хранения аутентифицированного пользователя
    last_activity_time = time.time()  # Время последней активности

    while True:
        # Проверяем длительное бездействие пользователя
        if time.time() - last_activity_time > INACTIVITY_TIMEOUT:
            print("\nПревышено время бездействия. Перевожу в режим блокировки.")
            authenticated_user = None

        # Ввод команды пользователем
        choice = input("\nМеню:\n1. Регистрация пользователя\n2. Вход\n3. Выход\nВведите номер команды: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            authenticated_user = check_authentication()
            if authenticated_user:
                username = authenticated_user[0]
                password = authenticated_user[1]
                permission, ideal_value, deviation = check_user_permission(username, password)
                if permission:
                    print("Пользователь аутентифицирован.")
                    print(f"Идеальное значение: {ideal_value}, Отклонение: {deviation}")
                    last_activity_time = time.time()  # Обновляем время последней активности

                    # После успешного входа, показываем мини-меню для аутентифицированного пользователя
                    while True:
                        last_activity_time = time.time()  # Время последней активности
                        account_choice = input("\nМини-меню:\n1. Запустить программу\n2. Выход из аккаунта\nВведите номер команды: ")
                        if account_choice == "1":
                            print("\nПрограмма запущена...")
                            # Здесь можно добавить вызов вашей программы
                        elif account_choice == "2":
                            print("\nВыход из аккаунта...")
                            authenticated_user = None
                            break
                        else:
                            print("\nНеверный выбор. Пожалуйста, выберите действие из предложенных.")
                            # Проверяем длительное бездействие пользователя
                        if time.time() - last_activity_time > INACTIVITY_TIMEOUT:
                            print("\nПревышено время бездействия. Перевожу в режим блокировки.")
                            authenticated_user = None
                            break
                else:
                    print("\nДоступ запрещен. Пользователь не зарегистрирован или неверный пароль.")
            else:
                print("\nДоступ запрещен. Не удалось аутентифицировать пользователя.")
        elif choice == "3":
            print("Выходим...")
            break
        else:
            print("\nНеверный выбор. Пожалуйста, выберите действие из предложенных.")


if __name__ == "__main__":
    main()
