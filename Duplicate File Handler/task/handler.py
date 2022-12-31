import sys
import os
import hashlib

if len(sys.argv) != 2:
    print("Directory is not specified")
    sys.exit(1)

user_dir = sys.argv[1]


def search_for_files(file_type):
    file_list = {}
    for root, dirs, files in os.walk(user_dir):
        for file in files:
            if file.endswith(file_type):
                file_path = os.path.join(root, file)
                size = os.path.getsize(file_path)
                if size not in file_list:
                    file_list[size] = []
                file_list[size].append(file_path)
    return file_list


def print_sorted_files(files_found, form):
    for size in sorted(files_found, reverse=True if form == 1 else False):
        print(f"{size} bytes")
        for file in files_found[size]:
            print(file)


def get_hash(file_path):
    with open(file_path, "rb") as file:
        return hashlib.md5(file.read()).hexdigest()


def print_duplicates(files_found, form):
    count = 1
    for size in sorted(files_found, reverse=True if form == 1 else False):
        if len(files_found[size]) > 1:
            hash_list = {}
            for file in files_found[size]:
                hashed_file = get_hash(file)
                if hashed_file not in hash_list:
                    hash_list[hashed_file] = []
                hash_list[hashed_file].append(file)
            print(f"{size} bytes")
            for hashed in hash_list:
                if len(hash_list[hashed]) > 1:
                    print(f"Hash: {hashed}")
                    for file in hash_list[hashed]:
                        print(f"{count}. {file}")
                        count += 1


def delete_duplicates(files_found, file_to_del, form):
    count = 1
    del_size = 0
    for size in sorted(files_found, reverse=True if form == 1 else False):
        if len(files_found[size]) > 1:
            hash_list = {}
            for file in files_found[size]:
                hashed_file = get_hash(file)
                if hashed_file not in hash_list:
                    hash_list[hashed_file] = []
                hash_list[hashed_file].append(file)
            for hashed in hash_list:
                if len(hash_list[hashed]) > 1:
                    for file in hash_list[hashed]:
                        if count in file_to_del:
                            size = os.path.getsize(file)
                            os.remove(file)
                            del_size += size
                        count += 1
    return del_size


file_format = input("Enter file format: ")
print("Size sorting options:")
print("1. Descending")
print("2. Ascending")

sorting_options = int(input("Enter a sorting options: "))
while sorting_options not in (1, 2):
    print("Wrong option")
    sorting_options = int(input("Enter a sorting options: "))

found_files = search_for_files(file_format)
print_sorted_files(found_files, sorting_options)

print("Check for duplicates?")
duplicate_check = input()
while duplicate_check not in ("yes", "no"):
    print("Wrong option")
    duplicate_check = input("Check for duplicates?")

if duplicate_check == "yes":
    print_duplicates(found_files, sorting_options)
else:
    sys.exit(0)

del_files = input("Delete files?\n")
while del_files not in ("yes", "no"):
    print("Wrong option")
    del_files = input("Delete files?\n")

if del_files == "yes":
    files_to_del = input("Enter file numbers to delete:\n")
    while not files_to_del or any(not i.isdigit() for i in files_to_del.split()):
        print("Wrong option")
        files_to_del = input("Enter file numbers to delete:\n")
    files_to_del = [int(i) for i in files_to_del.split()]
    del_size = delete_duplicates(found_files, files_to_del, sorting_options)
    print("Total freed up space: {} bytes".format(del_size))
else:
    sys.exit(0)
