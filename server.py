import xmlrpc.server
import os

SERVER_FILES_PATH = "ServerFiles/"

class Server:
    def __init__(self):
        os.makedirs(SERVER_FILES_PATH, exist_ok=True)

    def upload(self, data, filename):
        try:
            with open(os.path.join(SERVER_FILES_PATH, filename), "wb") as file:
                file.write(data.data)
            return f"File '{filename}' uploaded successfully."
        except Exception as e:
            print(f"Exception during upload: {e}")
            return "Upload Failed"

    def download(self, filename):
        try:
            filepath = os.path.join(SERVER_FILES_PATH, filename)
            with open(filepath, "rb") as file:
                data = file.read()
            return xmlrpc.client.Binary(data)
        except Exception as e:
            print(f"Exception during download: {e}")
            return None

    def rename(self, oldfilename, newfilename):
        try:
            old_filepath = os.path.join(SERVER_FILES_PATH, oldfilename)
            new_filepath = os.path.join(SERVER_FILES_PATH, newfilename)
            os.rename(old_filepath, new_filepath)
            return f"File '{oldfilename}' renamed to '{newfilename}' successfully."
        except Exception as e:
            print(f"Exception during rename: {e}")
            return "Failed to rename file."

    def delete(self, filename):
        try:
            filepath = os.path.join(SERVER_FILES_PATH, filename)
            os.remove(filepath)
            return f"File '{filename}' deleted successfully."
        except Exception as e:
            print(f"Exception during delete: {e}")
            return "File deletion failed."

def main():
    server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
    server.register_instance(Server())

    print("Server is running. Press Ctrl+C to exit.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server shutting down.")
        server.shutdown()


if __name__ == "__main__":
    main()
