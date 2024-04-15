import os
import random

class User:
    def __init__(self, name, level_of_access):
        self.name = name
        self.level_of_access = level_of_access

class FileObject:
    def __init__(self, name, file_path):
        self.name = name
        self.file_path = file_path

def get_permissions(index):
    level_user_list = ["Открытые данные", "Секретно", "Совершенно секретно"]
    return level_user_list[index]

def main():
    level_user_list = ["Открытые данные", "Секретно", "Совершенно секретно"]

    users = [User("Olga", get_permissions(random.randint(0, 2))),
             User("Vova", get_permissions(random.randint(0, 2))),
             User("Oleg", get_permissions(random.randint(0, 2))),
             User("Vanya", get_permissions(random.randint(0, 2))),
             User("Danya", get_permissions(random.randint(0, 2))),
             User("Robert", get_permissions(random.randint(0, 2))),
             User("Slavik", get_permissions(random.randint(0, 2)))]

    files = [FileObject("File1", "files/private1.txt"),
             FileObject("File2", "files/private2.txt"),
             FileObject("File3", "files/private3.txt"),
             FileObject("File4", "files/private4.txt")]

    privacy_level = [["Объект_" + str(i + 1), get_permissions(random.randint(0, 2))] for i in range(len(files))]

    print("\nУровень конфиденциальности информации/файлов [O]\n")
    for item in privacy_level:
        print(*item)

    print("\nУровень доступности пользователей [S]\n")
    for user in users:
        print(f"{user.name}: {user.level_of_access}")

    print("\nДоступные команды:")
    print("1. read - прочитать содержимое файла")
    print("2. write - записать данные в файл")
    print("3. request - запросить доступ к файлу")
    print("4. quit - завершить работу программы")

    while True:
        input_name = input("\nВведите имя пользователя или 'exit' для выхода из программы: ")
        if input_name.lower() == 'exit':
            break

        current_user = next((user for user in users if user.name == input_name), None)

        if current_user:
            print(f"\nПользователь: {current_user.name}")
            print(f"Уровень конфиденциальности: {current_user.level_of_access}")
            index_level_file = 0
            for i in range(len(users)):
                if level_user_list[i] == current_user.level_of_access:
                    index_level_file = i
                    break
            print("Права доступа к файлам:")
            level_object = []
            for i in range(len(privacy_level)):
                if level_user_list.index(privacy_level[i][1]) == index_level_file or level_user_list.index(privacy_level[i][1]) < index_level_file:
                    level_object.append(i)
                    print(privacy_level[i][0], end=" ")
            if not level_object:
                print("Нет доступа к  объектам")
            print()
            command_user = ""
            while command_user != "quit":
                command_user = input("Введите команду: ")
                if command_user == "request":
                    level_object.clear()
                    print("Введите номер файла, доступ к которому хотите получить: ")
                    for i in range(len(privacy_level)):
                        if level_user_list.index(privacy_level[i][1]) == index_level_file or level_user_list.index(privacy_level[i][1]) < index_level_file:
                            level_object.append(i)
                            print(privacy_level[i][0], end=" ")
                    if not level_object:
                        print(f"В доступе отказано. Нет объектов, доступных для пользователя с именем {current_user.name}!")
                    else:
                        index_file = int(input())
                        if index_file - 1 in level_object:
                            print("Операция выполнена")
                        else:
                            print("В доступе отказано. Недостаточно прав.")
                elif command_user == "quit":
                    print(f"Работа для пользователя {current_user.name} окончена.")
                    break
                elif command_user == "write":
                    level_object.clear()
                    for i in range(len(privacy_level)):
                        if level_user_list.index(privacy_level[i][1]) == index_level_file or level_user_list.index(privacy_level[i][1]) > index_level_file:
                            level_object.append(i)
                    print("Введите номер объекта, над которым будет производиться операция: ")
                    index_file = int(input())
                    if index_file - 1 in level_object:
                        current_file = files[index_file - 1]
                        with open(current_file.file_path, "a") as file:
                            user_input = input("Введите желаемый текст: ")
                            file.write(user_input + "\n")
                            print("Операция прошла успешно")
                    else:
                        print("В доступе отказано. Недостаточно прав.")
                elif command_user == "read":
                    level_object.clear()
                    for i in range(len(privacy_level)):
                        if level_user_list.index(privacy_level[i][1]) == index_level_file or level_user_list.index(privacy_level[i][1]) < index_level_file:
                            level_object.append(i)
                    print("Введите номер объекта, над которым будет производиться операция: ")
                    index_file = int(input())
                    if index_file - 1 in level_object:
                        current_file = files[index_file - 1]
                        with open(current_file.file_path, "r") as file:
                            for line in file:
                                print(line.strip())
                            print("Операция прошла успешно")
                    else:
                        print("В доступе отказано. Недостаточно прав.")
                else:
                    print("Ошибка: ввод несуществующей команды.")

        else:
            print("Пользователь не найден. Повторите ввод имени пользователя: ")


if __name__ == "__main__":
    main()
