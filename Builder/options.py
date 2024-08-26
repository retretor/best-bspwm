import os
from creators.builder import SystemConfiguration

OPTIONS = {
    "Configure folders?": {"state": False, "function": "configure_folders"},
    "Update Pacman DataBase?": {"state": False, "function": "update_pacman_database"},
    "Install base packages?": {"state": False, "function": "install_base_packages"},
    "Install dev packages?": {"state": False, "function": "install_dev_packages"},
}

DRIVER_OPTIONS = {
    "1": {"name": "Nvidia Drivers", "function": "install_nvidia_drivers"},
    "2": {"name": "AMD Drivers", "function": "build_amd_drivers"},
    "3": {"name": "Intel Drivers", "function": "build_intel_drivers"},
    "4": {"name": "None", "function": None}
}


class UserInterface:
    @staticmethod
    def start():
        UserInterface.welcome_banner()
        install_params = UserInterface.get_params()
        selected_driver = UserInterface.get_driver_choice()
        SystemConfiguration.start(install_params, selected_driver)

    @staticmethod
    def welcome_banner():
        os.system("sh Builder/assets/startup.sh")

    @staticmethod
    def is_verify_response(text) -> bool:
        return text.lower() in ["y", "yes"]

    @staticmethod
    def get_params():
        options = OPTIONS
        for idx, option in enumerate(options.keys(), 1):
            print(f"{idx}) {option} [Y/n]: ", end="")
            response = input()
            options[option]["state"] = UserInterface.is_verify_response(response)
        return options

    @staticmethod
    def get_driver_choice():
        print("\nChoose the video driver to install:")
        for idx, driver in DRIVER_OPTIONS.items():
            print(f"{idx}) {driver['name']}")

        choice = input("\nEnter the number of your choice: ")
        return DRIVER_OPTIONS.get(choice, {"function": None})["function"]
