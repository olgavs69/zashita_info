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

    users = [User(name, get_permissions(random.randint(0, 2))) for name in
             ["Olga", "Vova", "Oleg", "Vanya", "Danya", "Robert", "Slavik"]]
    files = [FileObject(f"File{i}", f"files/private{i}.txt") for i in range(1, 5)]

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
            index_level_file = level_user_list.index(current_user.level_of_access)

            print("Права доступа к файлам:")
            level_object = [i for i, item in enumerate(privacy_level) if
                            level_user_list.index(item[1]) <= index_level_file]
            if not level_object:
                print("Нет доступа к объектам")
            else:
                for i in level_object:
                    print(privacy_level[i][0], end=" ")
            print()

            while True:
                command_user = input("\nВведите команду: ")
                if command_user == "quit":
                    print(f"\nРабота для пользователя {current_user.name} окончена.")
                    break
                elif command_user in ["request", "write", "read"]:
                    if command_user == "request":
                        print("\nВведите номер файла, доступ к которому хотите получить: ")
                    elif command_user == "write":
                        print("\nВведите номер объекта, над которым будет производиться операция записи: ")
                    elif command_user == "read":
                        print("\nВведите номер объекта, над которым будет производиться операция чтения: ")

                    index_file = int(input())
                    if index_file - 1 in level_object:
                        current_file = files[index_file - 1]
                        if command_user == "request":
                            print("\nОперация выполнена")
                        elif command_user == "write":
                            user_input = input("\nВведите желаемый текст: ")
                            with open(current_file.file_path, "a", encoding="utf-8") as file:
                                file.write(user_input + "\n")
                            print("\nОперация прошла успешно")
                        elif command_user == "read":
                            with open(current_file.file_path, "r", encoding="utf-8") as file:
                                for line in file:
                                    print(line.strip())
                            print("\nОперация прошла успешно")
                    else:
                        print("\nВ доступе отказано. Недостаточно прав.")
                else:
                    print("\nОшибка: ввод несуществующей команды.")
        else:
            print("\nПользователь не найден. Повторите ввод имени пользователя: ")

if __name__ == "__main__":
    main()
