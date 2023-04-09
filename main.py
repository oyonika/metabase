import time
import logging
# from datetime import datetime

from database import create_table, bulk_insert, bulk_read, update_one
from Classes.ValidationException import ValidationException
from Classes.FileMetadata import FileMetadata
from Classes.MetaBase import MetaBase


def show_menu():
    print("\nPress 1 to add a new metadata entry. \nPress 2 to delete a metadata entry. \nPress 3 to update an existing metadata entry. \nPress 4 to find the number of entries by type. \nPress 5 to view an entry, if it exists. \nPress 6 to delete all entries from MetaBase cache. \nPress 7 to compare. \nPress 0 to exit this menu. \n")

def create_metadata(mb):
    file_type = input("File type: ") 
    file_name = input("File name: ") 
    if mb.check_key(file_type, file_name):
        file_size = input("File size: ")
        file_fingerprint = input("File fingerprint: ")
        file_modified = input("File modified: ")
        metadata = FileMetadata(file_type, file_name, file_size, file_fingerprint, file_modified)
        mb.insert(metadata)
        print("Successfully inserted a new entry!\n")
    else:
        print("This key already exists, please try again!\n")
        

def delete_metadata(mb):
    file_type = input("File type: ") 
    file_name = input("Name: ") 
    if mb.delete(file_type, file_name):
        print("Successfully deleted entry!\n")
    else:
        print("The record doesn't exist!\n")

def update_metadata(mb):
    file_type = input("File type: ") 
    file_name = input("File name: ")
    metadata = mb.get(file_type, file_name)
    metadata_from_db = mb.get_from_db(file_type, file_name)
    if metadata:
        file_size = input("File size: ")
        file_fingerprint = input("File fingerprint: ")
        metadata.update(file_size, file_fingerprint)
        print("Successfully updated!\n")
    elif metadata_from_db:
        file_size = input("File size: ")
        file_fingerprint = input("File fingerprint: ")
        metadata_from_db.update(file_size, file_fingerprint)
        update_one(metadata_from_db) # Should update the single entry if it is in the database and not the cache

    else:
        print("Record not found, please try again!\n")

def get_entries_by_type(mb):
    file_type = input("File type: ")
    print(str(len(mb.get_all_by_type(file_type))) + " metadata of type " + file_type)

def find_metadata(mb):
    file_type = input("File type: ") 
    file_name = input("File name: ")
    metadata = mb.get(file_type, file_name)
    metadata_from_db = mb.get_from_db(file_type, file_name)
    if metadata:
        print("File size: " + str(metadata.size) + "\nFingerprint: " + metadata.fingerprint + "\nTime modified: " + metadata.modified + "\nTime updated: " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(float(metadata.updated))) + "\n")
    elif metadata_from_db:
        print("File size: " + str(metadata_from_db.size) + "\nFingerprint: " + metadata_from_db.fingerprint + "\nTime modified: " + metadata_from_db.modified + "\nTime updated: " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(float(metadata_from_db.updated))) + "\n")
    else:
        print("Record not found, please try again!\n")

def compare_metadata(mb):
    file_type = input("File type: ") 
    file_name = input("File name: ") 
    file_size = input("File size: ")
    file_fingerprint = input("File fingerprint: ")
    file_modified = input("File modified: ")
    metadata = FileMetadata(file_type, file_name, file_size, file_fingerprint, file_modified)
    print(mb.compare(metadata))

def move_to_db_cache(mb):
    for key, meta in mb.metadata_by_name_and_type.items():
        key = (meta.name, meta.file_type)
        mb.metadata_in_db[key] = meta
        if meta.file_type not in mb.metadata_by_type:
            mb.metadata_by_type[meta.file_type] = []
        mb.metadata_by_type[meta.file_type].append(meta)


def delete_all_metadata(mb):
    user_input = input("Would you like to export data to database before clearing cache? Y/N: ")
    if user_input.lower() == 'y':
            move_to_db_cache(mb)
            export_to_database(mb)
            print("Export to database complete. ")

    mb.delete_all()
    print("All records deleted from cache!\n")

def export_to_database(mb):
    bulk_insert(mb)
    mb.delete_all()

def import_from_database(mb):
    bulk_read(mb)

def main():
    mb = MetaBase()
    import_from_database(mb)
    print("Welcome to MetaBase, your one-stop solution for storing metadata!")

    # create_table()

    while True:
        show_menu()
        user_input = int(input("Enter here: "))

        match user_input:
            case 1:
                create_metadata(mb)
            case 2:
                delete_metadata(mb)
            case 3:
                update_metadata(mb)
            case 4:
                get_entries_by_type(mb)
            case 5:
                find_metadata(mb)
            case 6:
                delete_all_metadata(mb)
            case 7: 
                compare_metadata(mb)
            # case 8:
                # show_menu()
            case 0:
                export_to_database(mb)
                break


if __name__ == '__main__':
    try:
        main()
    except ValidationException as e:
        logging.error(e)
    except Exception as e:
        logging.exception(e)

    