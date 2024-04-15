import os
import random

class User:
    def __init__(self, name, role):
        self.name = name
        self.role = role

class FileObject:
    def __init__(self, name, file_object):
        self.name = name
        self.file_object = file_object

def to_binary_string_with_leading_zeros(value):
    binary = bin(value)[2:]
    return binary.zfill(3)

def get_permissions(permission_code):
    permissions = ""
    if permission_code == "000":
        permissions = "полностью запрещен"
    elif permission_code == "001":
        permissions = "передача прав"
    elif permission_code == "010":
        permissions = "запись"
    elif permission_code == "011":
        permissions = "запись, передача прав"
    elif permission_code == "100":
        permissions = "чтение"
    elif permission_code == "101":
        permissions = "чтение, передача прав"
    elif permission_code == "110":
        permissions = "чтение, запись"
    elif permission_code == "111":
        permissions = "полный доступ"
    return permissions

users = [User("Alice", "admin"), User("Lesya", "user"), User("Boby", "user"), User("Dasha", "user"),
         User("Pasha", "user"), User("Dima", "user"), User("Nikita", "user")]

files = [FileObject(f"File{i}", f"files/private{i}.txt") for i in range(1, 5)]

permissions_matrix = [[to_binary_string_with_leading_zeros(random.randint(0, 7)) for _ in range(4)] for _ in range(len(users))]

for i in range(4):
    permissions_matrix[0][i] = "111"  # Установка полных прав доступа для администратора

print("Матрица прав доступа:")
for i, user in enumerate(users):
    print(f"{user.name}:\t", end="")
    for permission in permissions_matrix[i]:
        print(get_permissions(permission), end=" ")
    print()

while True:
    input_name = input("Введите имя пользователя или 'exit' для выхода: ")
    if input_name.lower() == 'exit':
        break

    current_user = None
    for user in users:
        if user.name == input_name:
            current_user = user
            break

    if current_user:
        user_index = users.index(current_user)
        print(f"\nПользователь: {current_user.name}")
        print(f"Роль: {current_user.role}")
        print("Права доступа к файлам:")
        for i, permission_code in enumerate(permissions_matrix[user_index]):
            print(f"\nФайл {i+1}: {get_permissions(permission_code)}")

        while True:
            command_user = input("\nВведите команду (read/write/quit): ")
            if command_user == "quit":
                print(f"Работа пользователя {current_user.name} завершена. До свидания.")
                break
            elif command_user == "read" or command_user == "write":
                print("\nНад каким объектом производится операция?")
                index_file = int(input())
                current_file = files[index_file - 1]
                permission_code = permissions_matrix[user_index][index_file - 1]

                read_bit = permission_code[0]
                if command_user == "read" and read_bit == '1':
                    with open(current_file.file_object, "r", encoding="utf-8") as file:  # Указываем кодировку UTF-8
                        for line in file:
                            print(line.strip())
                    print("Операция прошла успешно")
                elif command_user == "write":
                    write_bit = permission_code[1]
                    if write_bit == '1':
                        user_input = input("Введите текст для записи: ")
                        with open(current_file.file_object, "a", encoding="utf-8") as file:  # Указываем кодировку UTF-8
                            file.write(user_input + "\n")
                        print("\nОперация прошла успешно")
                    else:
                        print("\nОтказ в выполнении операции. У вас нет прав для ее осуществления")
                else:
                    print("\nОтказ в выполнении операции. У вас нет прав для ее осуществления")
            else:
                print("\nВы ввели несуществующую команду!")
    else:
        print("\nПользователь не найден. Пожалуйста, попробуйте снова.")
