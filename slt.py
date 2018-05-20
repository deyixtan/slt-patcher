import binascii
import re
import argparse
import os

class Patcher:
    '''
    ONLY FOR WINDOWS 64-BIT OS
    CAN BE PATCHED ON MOST SUBLIME TEXT BUILDS (BOTH STABLE AND DEV)
    MADE BY: DE YI <https://github.com/deyixtan>
    '''
    LICENSE_CHECK_AOB = b"80380074..488d..........48......488d..........48"
    LICENSE_PATCH_AOB = b"800801"
    UPDATE_CHECK_AOB = b"5748......49....41....40....4c8d..........48....4c8d..........488d..........33"
    UPDATE_PATCH_AOB = b"c3"

    TITLEBAR_UNREGISTERED_CHECK_AOB = b"74..41b8........488d..........488d....e8........488d..........be........8a"
    TITLEBAR_UNREGISTERED_PATCH_AOB = b"eb"
    TITLEBAR_UPGRADE_REQUIRED_CHECK_AOB = b"74..41b8........488d..........488d....e8........488d....48........48........49......ff"
    TITLEBAR_UPGRADE_REQUIRED_PATCH_AOB = b"eb"
    SAVEDIALOG_POPUP_CHECK_AOB = b"e8........84..74..488d..........e8........4883....c3cccccc4883....48"
    SAVEDIALOG_POPUP_PATCH_AOB = b"9090909090"
    SAVEDIALOG_WEBPAGE_CALL_CHECK_AOB = b"74..488d..........e8........4883....c3cccccc4883....48"
    SAVEDIALOG_WEBPAGE_CALL_PATCH_AOB = b"eb"
    ABOUTDIALOG_LICENSE_CHECK_AOB = b"0f84........4889..........48c7..................488d..........4889..........48"
    ABOUTDIALOG_LICENSE_PATCH_AOB = b"0f85"

    def __init__(self, file_path):
        self.file_path = file_path

        # get hex dump of input file
        with open(file_path, "rb") as file:
            self.hex_dump = bytearray(binascii.hexlify(file.read()))

    def patch_file(self):
        if self.__is_license_index_valid() and self.__is_update_index_valid() and self.__is_temp_index_valid():
            # bypass & patch file with changes
            self.__patch_license()
            self.__patch_update()
            self.__patch_temp()

            try: 
                with open(self.file_path, "wb") as file:
                    file.write(binascii.unhexlify(self.hex_dump))
            except PermissionError:
                return False
            return True
        else:
            return False

    def __index_is_valid(self, check_aob):
        return len(re.findall(check_aob, self.hex_dump)) == 1

    def __is_license_index_valid(self):
        return self.__index_is_valid(Patcher.LICENSE_CHECK_AOB)

    def __is_update_index_valid(self):
        return self.__index_is_valid(Patcher.UPDATE_CHECK_AOB)

    def __is_temp_index_valid(self):
        return (self.__index_is_valid(Patcher.TITLEBAR_UNREGISTERED_CHECK_AOB) and
                self.__index_is_valid(Patcher.TITLEBAR_UPGRADE_REQUIRED_CHECK_AOB) and
                self.__index_is_valid(Patcher.SAVEDIALOG_POPUP_CHECK_AOB) and
                self.__index_is_valid(Patcher.SAVEDIALOG_WEBPAGE_CALL_CHECK_AOB) and
                self.__index_is_valid(Patcher.ABOUTDIALOG_LICENSE_CHECK_AOB))

    def __patch_check(self, check_aob, patch_aob):
        # bypass checks
        check_index = self.hex_dump.index(re.findall(check_aob, self.hex_dump)[0])
        self.hex_dump[check_index:check_index+len(patch_aob)] = patch_aob

    def __patch_license(self):
        # bypass license
        self.__patch_check(Patcher.LICENSE_CHECK_AOB, Patcher.LICENSE_PATCH_AOB)

    def __patch_update(self):
        # bypass update
        self.__patch_check(Patcher.UPDATE_CHECK_AOB, Patcher.UPDATE_PATCH_AOB)

    def __patch_temp(self):
        # bypass some checks temp
        self.__patch_check(Patcher.TITLEBAR_UNREGISTERED_CHECK_AOB, Patcher.TITLEBAR_UNREGISTERED_PATCH_AOB)
        self.__patch_check(Patcher.TITLEBAR_UPGRADE_REQUIRED_CHECK_AOB, Patcher.TITLEBAR_UPGRADE_REQUIRED_PATCH_AOB)
        self.__patch_check(Patcher.SAVEDIALOG_POPUP_CHECK_AOB, Patcher.SAVEDIALOG_POPUP_PATCH_AOB)
        self.__patch_check(Patcher.SAVEDIALOG_WEBPAGE_CALL_CHECK_AOB, Patcher.SAVEDIALOG_WEBPAGE_CALL_PATCH_AOB)
        self.__patch_check(Patcher.ABOUTDIALOG_LICENSE_CHECK_AOB, Patcher.ABOUTDIALOG_LICENSE_PATCH_AOB)

# script logic
def main():
    parser = argparse.ArgumentParser(description="Cracks Sublime Text Editor")
    parser.add_argument("file_path", help="file path to sublime_text.exe")
    args = parser.parse_args()

    # check for valid "sublime_text.exe" file path
    if (os.path.isfile(args.file_path)) and ("sublime_text.exe" in args.file_path):
        # performs patch
        patcher = Patcher(args.file_path)
        result = patcher.patch_file()

        if result:
            print(f"Patcher >> Successfully patched '{args.file_path}'.")
        else:
            print("Patcher >> Could not work on input file.")
    else:
        print("Patcher >> Please input a valid file.")

# direct execution of the script
if __name__ == "__main__":
    main()