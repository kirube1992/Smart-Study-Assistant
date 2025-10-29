
# my_dictionary = {}

# def add_document(file_path):
#     try:
#         with open(file_path, 'r') as f:
#             content = f.read()
#             my_dictionary[file_path] = content
#             print(f"Succesfully added '{file_path}'.")
#     except FileNotFoundError:
#         print(f"Error: File '{file_path}' does not exist.")
#     except Exception as e:
#         print(f"An unexpected error occurred while adding '{file_path}': {e}")
# def list_documents():
#     if len(my_dictionary) > 0:
#         for file_path in my_dictionary:
#             print(file_path)
#         print('end of the list')
#     else:
#         print('There is no file in the dictionary')

# while True:
#     command = input(">>>").strip()
#     part = command.split()

#     if len(part) == 0:
#         continue
#     if part[0] == 'add_document':
#         if len(part) < 2:
#           file_path = input('please enter the file Path').strip()
#         else:
#             file_path = " ".join(part[1:])
#             file_path = part[1]
#             add_document(file_path)
#             print(f"Attempted to add '{file_path}'. Check console for errors.")
#     elif part[0] == 'list_documents':
#         list_documents()
#     elif part[0] == 'exit':
#         print('good bye')
#         break
#     else:
#         print('You enter wrong input')
    
from datetime import datetime, date
import json
import os

class Document:
    def __init__(self,title,content,file_path,ingestion_date):
        self.title = title
        self.content = content
        self.file_path = file_path
        self.ingestion_date = ingestion_date
    def __str__(self):
        return f"Document title: {self.title}, document filePath: {self.file_path}, date of ingestion: {self.ingestion_date}"
    def __repr__(self):
        return f"{self.title} {self.file_path} {self.ingestion_date}"
    
class DocumentManager:
    def __init__(self):
        self.documents = []
    def add_document(self, file_path):
        if not os.path.exists(file_path):
            print("File not found!")
            return 
        with open(file_path, 'r') as f:
            content = f.read()
        title = os.path.basename(file_path)
        ingestion_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        document = Document(title, content, file_path, ingestion_date)
        self.documents.append(document)
        print(f"Added: {title}")
        # ingestion_date = date.today()
    def list_documents(self):
        if not self.documents:
            print('No documents is found')
        else:
            for doc in self.documents:
                print(doc)
    def save_to_json(self,file_name):
        data = []

        if os.path.exists(file_name):
            with open(file_name,"r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        for doc in self.documents:
            data.append(doc.__dict__)

    def load_from_json(self, file_name):
        pass
# if __name__ == "__main__":
#     manager = DocumentManager()
#     manager.add_document("Test.txt")
# print(manager.list_documents)
manager = DocumentManager()
manager.add_document("Test.txt")   # make sure this file exists
manager.list_documents()

