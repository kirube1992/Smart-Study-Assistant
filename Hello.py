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
    def Add_document(self, file_path):
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
        data = [doc.__dict__ for doc in self.documents]

        if os.path.exists(file_name):
            with open(file_name,"r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        for doc in self.documents:
            data.append(doc.__dict__)
        with open(file_name,"w") as f:
            json.dump(data,f,indent=4)
        print(f"Saved {len(self.documents)} document(s) to {file_name}")

    def load_from_json(self, file_name):
        if  not os.path.exists(file_name):
            print('No json file found')
            return
        try:
            with open(file_name, "r") as f:
                data = json.load(f)
                for entry in data:
                    doc = Document(
                        title=entry["title"],
                        content=entry["content"],
                        file_path=entry["file_path"],
                        ingestion_date=entry["ingestion_date"]
                    )
                    self.documents.append(doc)
        except Exception as e:
            print(f"Error loading json {e}")

# manager = DocumentManager()
# doc1 = Document("Test1", "Content 1", "file1.txt", datetime.now().isoformat())
# doc2 = Document("Test2", "Content 2", "file2.txt", datetime.now().isoformat())
# manager.documents.extend([doc1, doc2])
# manager.save_to_json("documents.json")


# print("\n--- Fresh Start ---")
# new_manager = DocumentManager()
# new_manager.load_from_json("documents.json")
# new_manager.list_documents()