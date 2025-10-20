
my_dictionary = {}

def add_document(file_path):
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            my_dictionary[file_path] = content
            print(f"Succesfully added '{file_path}'.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred while adding '{file_path}': {e}")
def list_documents():
    if len(my_dictionary) > 0:
        for file_path in my_dictionary:
            print(file_path)
        print('end of the list')
    else:
        print('There is no file in the dictionary')

while True:
    command = input(">>>").strip()
    part = command.split()

    if len(part) == 0:
        continue
    if part[0] == 'add_document':
        if len(part) < 2:
          file_path = input('please enter the file Path').strip()
        else:
            file_path = " ".join(part[1:])
            file_path = part[1]
            add_document(file_path)
            print(f"Attempted to add '{file_path}'. Check console for errors.")
    elif part[0] == 'list_documents':
        list_documents()
    elif part[0] == 'exit':
        print('good bye')
        break
    else:
        print('You enter wrong input')
