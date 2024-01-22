import xmlrpc.client
import os

SERVER_URL = "http://localhost:8000/"

def option():
    print("Choose operation:")
    print("1. Upload File")
    print("2. Download File")
    print("3. Rename File")
    print("4. Delete File")
    print("5. Exit")

def main():
    while True:
        try:
            os.makedirs("ClientFiles", exist_ok=True)
            client = Client()

            option()
            choice = int(input("Enter your choice: "))

            if choice == 1:
                filename = input("Enter the file path for the upload: ")
                print(client.upload(filename))

            elif choice == 2:
                filename_to_download = input("Enter the file name for the download: ")
                print(client.download(filename_to_download))

            elif choice == 3:
                old_filename = input("Existing file name: ")
                new_filename = input("New file name: ")
                print(client.rename(old_filename, new_filename))

            elif choice == 4:
                file_to_delete = input("Enter the file name to delete: ")
                print(client.delete(file_to_delete))

            elif choice == 5:
                break

            else:
                print("Invalid choice. Please try again.")

        except Exception as e:
            print("Enter numerical only\n")

class Client:
    def __init__(self):
        self.server = xmlrpc.client.ServerProxy(SERVER_URL, allow_none = True)

    def upload(self, filename):
        try:
            with open(filename, "rb") as file:
                data = xmlrpc.client.Binary(file.read())
                return self.server.upload(data, os.path.basename(filename))
        except FileNotFoundError:
            return "Please provide a valid file path-File missing"
        except Exception as e:
            print(e)
            return "Upload failed."

    def download(self, filename):
        try:
            data = self.server.download(filename)
            if data is not None:
                with open(os.path.join("ClientFiles", filename), "wb") as file:
                    file.write(data.data)
                return f"File '{filename}' download successfully."
            else:
                return f"File '{filename}' not found."
        except Exception as e:
            print(f"Download Failed: {e}")

    def rename(self, oldfilename, newfilename):
        return self.server.rename(oldfilename, newfilename)

    def delete(self, filename):
        return self.server.delete(filename)

if __name__ == "__main__":
    main()