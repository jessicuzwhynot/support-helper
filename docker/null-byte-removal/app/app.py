from os import environ, remove
from pathlib import Path
from shutil import copyfile
from subprocess import check_output


# Function to search input directory/files for binary encoded files with null bytes and remove the null bytes
def remove_null_byte_characters(base_directory, file_match):
    p = Path(base_directory).glob(file_match)
    for log in p:
        output = check_output(["file", "-i", f"{log}"])
        if "charset=binary" or "charset=us-ascii" in str(output):
            old_file = open(f"{log}", "rt")
            new_file = open("/tmp/tmp.log", "wt")
            for line in old_file:
                new_file.write(line.replace("\x00", ''))
            old_file.close()
            new_file.close()
            remove(f"{log}")
            copyfile("/tmp/tmp.log", f"{log}")
            remove("/tmp/tmp.log")


if __name__ == '__main__':
    base_directory = environ['BASE_DIRECTORY']
    file_match = environ['FILE_MATCH']

    remove_null_byte_characters(base_directory, file_match)