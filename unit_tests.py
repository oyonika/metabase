from time import time

from Classes.MetaBase import MetaBase
from Classes.FileMetadata import FileMetadata
from main import import_from_database, export_to_database


if __name__ == '__main__':
    mb = MetaBase()
    import_from_database(mb)
    print("Welcome to MetaBase, your one-stop solution for storing metadata! Running unit tests...")

    # Inserting into MetaBase
    metadata = FileMetadata("audio", "QUZSMYDK", 167, "ec4a99b7152e471bbf36e13911b6062e", "2023-03-12T21:55:41.158894+00:00")
    mb.insert(metadata) # Success

    metadata = FileMetadata("report", "YENTHZZR", 96, "a7ca1d79d6574206889a71e7efa63b68", "2023-03-12T22:14:15.158900+00:00")
    mb.insert(metadata) # Success

    metadata = FileMetadata("memory_dump", "UQXDSARY", 1094, "5282c3b7803f48a5923caa5600aef958", "2023-03-12T20:50:57.158907+00:00")
    mb.insert(metadata) # Success

    metadata = FileMetadata("memory_dump", "PFWMBTLB", 1098, "9377c3a4beda4ad6b08312e6be118c61", "2023-03-12T21:40:24.158913+00:00")
    mb.insert(metadata) # Success

    metadata = FileMetadata("audio", "GNSJRBYP", 1141, "1e9b1c905cb841bc808bc3f999acced2", "2023-03-12T20:55:44.158919+00:00")
    mb.insert(metadata) # Success

    metadata = FileMetadata("audio", "GNSJRBYP", 1141, "1e9b1c905cb841bc808bc3f999acced2", "2023-03-12T20:55:44.158919+00:00")
    mb.insert(metadata) # Fails since the key exists in MetaBase


    # Deleting from MetaBase
    mb.delete("audio", "GNSJRBYP") # Success
    mb.delete("memory_dump", "GNSJRBYP") # Fails
    mb.delete("audio", "GNSKKBYP") # Fails

    # Number of entries for each file type
    print(str(len(mb.get_all_by_type("audio"))) + " metadata of type audio") 
    print(str(len(mb.get_all_by_type("video"))) + " metadata of type video") #0

    # Comparison
    metadata = FileMetadata("report", "YENTHZZR", 96, "a7ca1d79d6574206889a71e7efa63b68", "2023-03-12T22:14:15.158900+00:00")
    print(mb.compare(metadata)) # Success

    metadata = FileMetadata("report", "YENTHZZR", 96, "a7ca1d79d2222206889a71e7efa63b68", "2023-03-12T22:14:15.158900+00:00") 
    print(mb.compare(metadata)) # Warning

    metadata = FileMetadata("report", "YENTHZZR", 961, "a7ca1d79d6574206889a71e7efa63b68", "2022-03-12T22:14:15.158900+00:00") 
    print(mb.compare(metadata)) # Failed

    metadata = FileMetadata("audio", "YENTHZZR", 96, "a7ca1d79d6574206889a71e7efa63b68", "2023-03-12T22:14:15.158900+00:00") 
    print(mb.compare(metadata)) # Not found

    # Export all to database
    export_to_database(mb)

    metadata = FileMetadata("audio", "GNSJRBYP", 1141, "1e9b1c905cb841bc808bc3f999acced2", "2023-03-12T20:55:44.158919+00:00")
    mb.insert(metadata) # Fails since the key exists in database

    metadata = FileMetadata("debug", "NWPOEQJJ", 1028, "8752ffdabf644ca0b6aa1dc0f63f53db", "2023-03-12T21:39:16.158925+00:00")
    mb.insert(metadata) # Fails since the key exists in MetaBase
  