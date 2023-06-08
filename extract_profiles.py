import subprocess
import ctypes
import os.path
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output', type=str, help='Path to text file you want to store passwords for profiles at (if there is no path, it generates randomly)')
args = parser.parse_args()

class ExtractPasswords:
    def __init__(self, file):
        self.system_encoding = 'CP866' # 'Windows-1251' || 'utf-8' || 'ascii' || 'latin1' || 'ISO-8859-1'
        self.profiles = []
        self.successed_profiles = []
        self.passwords = {}
        if not file:
            self.end_path = "passwords"+str(random.randint(5555,9999))+".txt"
        else:
            self.end_path = file

    def start(self):
        output = subprocess.check_output("netsh wlan show profiles").decode(encoding=self.system_encoding, errors='ignore').split()
        self.extract_profiles(output)

    def extract_profiles(self, output):
        a = output.index("All")
        a = output[a:]
        a = ' '.join(a).split('All User Profile')
        for i in a:
            try:
                self.profiles.append(i.strip().split(':')[1].strip())
            except:
                pass
        self.end()

    def end(self):
        with open(self.end_path, 'a') as file:
            for item in self.profiles:
                try:
                    cracked = subprocess.check_output(f'netsh wlan show profile "{item}" key=clear').decode(encoding=self.system_encoding, errors='ignore').split()
                    content = cracked.index("Content")
                    self.successed_profiles.append(item)
                    file.write(f'{item}: {cracked[content + 2]}\n')
                except:
                    pass
        try:
            assert len(self.successed_profiles) != 0, print('No profiles were found')
            print(f'Passwords for {", ".join(self.successed_profiles)} are stored at: {os.path.abspath(self.end_path)}')
            
            response = str(input("Do you want to open it? (y/n):"))

            assert response == "y", exit(0)
            ctypes.windll.shell32.ShellExecuteW(0, "open", os.path.abspath(self.end_path), 0, 0, 1)
        except AssertionError:
            pass

if __name__ == '__main__':
    p = ExtractPasswords(args.output)
    p.start()