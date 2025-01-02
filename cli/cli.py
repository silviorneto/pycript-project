import argparse
import random
import string
from pathlib import Path
from cryptography.fernet import Fernet

class PycryptCli:
    def __init__(self):
        self.file_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))

    def start(self):
        parser = argparse.ArgumentParser(
            prog="pycrypt",
            description="This program encrypt/decrypt selected file",
            usage='%(prog)s [options]'
        )

        subparsers = parser.add_subparsers(dest="command", description="command", help="Choose command (encrypt or decrypt)")
        self.generate_parsers(subparsers)

        args = parser.parse_args()
        if args.command == "encrypt":
            self.encrypt_file(file_path=args.file_path, key_path=args.key_path)

        elif args.command == "decrypt":
            self.decrypt_file(file_path=args.file_path, key_path=args.key_path)

        elif args.command == "generate_key":
            self.generate_key(directory=args.dir)

    def encrypt_file(self, file_path: str, key_path: str) -> None:
        file_path = Path(file_path)
        key_path = Path(key_path)

        if not file_path.exists():
            print("File not found!")
            return

        if not key_path.exists():
            print("Key path not found!")
            return

        with key_path.open("rb") as f:
            key = f.read()

        cipher = Fernet(key)
        with file_path.open("rb") as f:
            plaintext = f.read()

        ciphertext = cipher.encrypt(plaintext)
        file_path = file_path.rename(f"{file_path.name}.enc-{self.file_code}")
        with file_path.open(mode="wb") as f:
            f.write(ciphertext)

        print(f"Arquivo {file_path.name} criptografado com sucesso!")

    def decrypt_file(self, file_path: str, key_path: str) -> None:
        try:
            file_path = Path(file_path)
            key_path = Path(key_path)

            if not file_path.exists():
                print("File not found!")
                return

            if not key_path.exists():
                print("Key path not found!")
                return

            with key_path.open("rb") as f:
                key = f.read()

            cipher = Fernet(key)
            with file_path.open("rb") as f:
                ciphertext = f.read()

            plaintext = cipher.decrypt(ciphertext)
            file_path = file_path.rename(file_path.name.split(".enc-")[0])
            with file_path.open(mode="wb") as f:
                f.write(plaintext)

            print(f"Arquivo {file_path.name} descriptografado com sucesso!")

        except Exception as e:
            print("Não foi possível descriptografar o arquivo. Verifique os dados informados e tente novamente!")

    def generate_key(self, directory: str) -> None:
        key = Fernet.generate_key()
        key_path = Path(f"{directory}/key-{self.file_code}")

        with open(key_path, mode="wb") as f:
            f.write(key)

        print(f"Chave gerada e salva no arquivo key-{self.file_code}")

    def generate_parsers(self, subparsers) -> None:
        self.build_subparser(
            subparsers=subparsers,
            subparse_name="encrypt",
            subparse_description="Encrypt file",
            subparse_help="Encrypt file",
            args=[
                {
                    "argument": "file_path",
                    "help": "File path from file to crypt"
                },
                {
                    "argument": "key_path",
                    "help": "Key to crypt file"
                },
            ])

        self.build_subparser(
            subparsers=subparsers,
            subparse_name="decrypt",
            subparse_description="Decrypt file",
            subparse_help="Decrypt file",
            args=[
                {
                    "argument": "file_path",
                    "help": "File path from file to decrypt"
                },
                {
                    "argument": "key_path",
                    "help": "Key to decrypt file"
                },
            ])
        self.build_subparser(
            subparsers=subparsers,
            subparse_name="generate_key",
            subparse_description="Generate key to crypt file",
            subparse_help="Generate key to crypt file",
            args=[
                {
                    "argument": "dir",
                    "help": "Directory where key file will be generated"
                },
            ]
        )


    @staticmethod
    def build_subparser(subparsers, subparse_name: str, subparse_description: str, subparse_help: str, args: list[dict] = None) -> None:
        subparse = subparsers.add_parser(name=subparse_name, description=subparse_description, help=subparse_help)
        if args:
            for arg in args:
                subparse.add_argument(arg.get("argument"), help=arg.get("help"))