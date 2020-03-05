from pathlib import Path
from app import remove_null_byte_characters


def test_remove_null_byte_characters():
    file1 = Path("/var/lib/docker/containers/container1/container1.log")
    file2 = Path("/var/lib/docker/containers/container2/container2.log")
    # Create a file with null byte characters and text
    with open(file1, "w+") as null_byte_file:
        x = 0
        y = 0
        while x < 10:
            null_byte_file.write("\x00")
            x += 1
        while y < 10:
            null_byte_file.write("I am text\n")
            y += 1
        assert(null_byte_file.read().find("\x00"))
        assert(null_byte_file.read().find("I am text"))
    # Create a file with just text
    with open(file2, "w+") as standard_file:
        x = 0
        while x < 10:
            standard_file.write("Don't change me bro\n")
            x += 1
        assert(standard_file.read().find("Don't change me bro"))
    # Load file contents into variables for test
    file1_contents = file1.read_text()
    file2_contents = file2.read_text()
    remove_null_byte_characters("/var/lib/docker/containers/", "**/*.log*")
    new_file1 = Path("/var/lib/docker/containers/container1/container1.log")
    new_file2 = Path("/var/lib/docker/containers/container2/container2.log")
    new_file1_contents = new_file1.read_text()
    new_file2_contents = new_file2.read_text()
    # Assert that the path for file1 no longer contains null bytes and still contains the text, and they are not the same
    with new_file1.open("r") as changed_file:
        assert("I am text\n" in changed_file.readlines())
        assert(str(file1_contents) != str(new_file1_contents))
    # Assert that the path and contents for file2 is unchanged
    with new_file2.open("r") as unchanged_file:
        assert("Don't change me bro\n" in unchanged_file.readlines())
        assert(str(new_file2_contents) == str(file2_contents))