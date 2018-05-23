import binascii
import re
import argparse
import os

class Patcher:
    '''
    ONLY TESTED FOR WINDOWS AND LINUX 64-BIT
    CAN BE PATCHED ON ALL WINDOWS BUILDS >3170 & LINUX BUILD 3176 (INCLUDES BOTH STABLE AND DEV)
    MADE BY: DE YI <https://github.com/deyixtan>
    '''
    INITIAL_LICENSE_CHECK_AOB = {"windows": b"80380074..488d..........48......488d..........48",
                                 "linux": b"80380074..498b..........48........48....74..........48",
                                 "patch": b"800801"}
    PERSISTENT_LICENSE_CHECK_AOB = {"windows": b"00c3488bc455488d68984881ec6001000048c74550fe",
                                    "linux": b"00c390488b07488b38e9aba0030090415653504989f6",
                                    "patch": b"01"}
    UPDATE_CHECK_AOB = {"windows": b"5748......49....41....40....4c8d..........48....4c8d..........488d..........33",
                        "linux": b"5348....31..be........ba........b9........e8........84..74..48....5be9........5b",
                        "patch": b"c3"}

    def __init__(self, file_path):
        self.file_path = file_path

        # get hex dump of input file
        with open(file_path, "rb") as file:
            self.hex_dump = bytearray(binascii.hexlify(file.read()))

    def patch_file(self):
        os_target = self.__get_file_os_target()
        if os_target != None and self.__is_initial_license_check_index_valid(os_target) and self.__is_persistent_license_check_index_valid(os_target) and self.__is_update_check_index_valid(os_target):
            # bypass & patch file with changes
            self.__patch_initial_license_check(os_target)
            self.__patch_persistent_license_check(os_target)
            self.__patch_update_check(os_target)

            try:
                with open(self.file_path, "wb") as file:
                    file.write(binascii.unhexlify(self.hex_dump))
            except PermissionError:
                return False
            return True
        return False

    def __get_file_os_target(self):
        if self.hex_dump.startswith(b"4d5a"):
            return "windows"
        elif self.hex_dump.startswith(b"7f454c4602"):
            return "linux"
        else:
            return None

    def __index_is_valid(self, check_aob):
        return len(re.findall(check_aob, self.hex_dump)) == 1

    def __is_initial_license_check_index_valid(self, os):
        return self.__index_is_valid(Patcher.INITIAL_LICENSE_CHECK_AOB[os])

    def __is_persistent_license_check_index_valid(self, os):
        return self.__index_is_valid(Patcher.PERSISTENT_LICENSE_CHECK_AOB[os])

    def __is_update_check_index_valid(self, os):
        return self.__index_is_valid(Patcher.UPDATE_CHECK_AOB[os])

    def __patch_check(self, check_aob, patch_aob):
        # bypass checks
        check_index = self.hex_dump.index(re.findall(check_aob, self.hex_dump)[0])
        self.hex_dump[check_index:check_index+len(patch_aob)] = patch_aob
        
    def __patch_initial_license_check(self, os):
        # bypass license
        self.__patch_check(Patcher.INITIAL_LICENSE_CHECK_AOB[os], Patcher.INITIAL_LICENSE_CHECK_AOB["patch"])

    def __patch_persistent_license_check(self, os):
        # bypass license
        self.__patch_check(Patcher.PERSISTENT_LICENSE_CHECK_AOB[os], Patcher.PERSISTENT_LICENSE_CHECK_AOB["patch"])

    def __patch_update_check(self, os):
        # bypass update
        self.__patch_check(Patcher.UPDATE_CHECK_AOB[os], Patcher.UPDATE_CHECK_AOB["patch"])

# script logic
def main():
    parser = argparse.ArgumentParser(description="Cracks Sublime Text Editor")
    parser.add_argument("file_path", help="file path to sublime text executable.")
    args = parser.parse_args()

    # check for valid file path
    if (os.path.isfile(args.file_path)):
        # performs patch
        patcher = Patcher(args.file_path)
        result = patcher.patch_file()

        if result:
            print(f"Patcher >> Successfully patched '{args.file_path}'.")
        else:
            print("Patcher >> Could not work on input file.")
    else:
        print("Patcher >> Please input a valid file path.")

# direct execution of the script
if __name__ == "__main__":
    main()