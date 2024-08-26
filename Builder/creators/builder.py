import os
import packages

from logger import Logger, LoggerStatus


# TODO: Implement error handling for package installation

class SystemConfiguration:
    @staticmethod
    def start(options, selected_driver_function):
        start_text = f"[+] Starting assembly. Options: {[(opt, val['state']) for opt, val in options.items()]}"
        Logger.add_record(start_text)

        for option, settings in options.items():
            if settings["state"]:
                function_name = settings["function"]
                getattr(SystemConfiguration, function_name)()

        Logger.add_record("[+] Preparing Multilib")
        os.system(r"sudo sed -i 's/^#\[multilib\]/[multilib]/' /etc/pacman.conf")
        os.system(
            r"sudo sed -i '/^\[multilib\]$/,/^\[/ s/^#\(Include = \/etc\/pacman\.d\/mirrorlist\)/\1/' /etc/pacman.conf")
        os.system("sudo pacman -Sl multilib")
        os.system("sudo pacman -Sy")

        if selected_driver_function:
            getattr(SystemConfiguration, selected_driver_function)()

        Logger.add_record("[+] Assembly completed")

        # TODO: The process should not be repeated when reassembling, important components should only be updated with new ones
        os.system("sudo systemctl enable NetworkManager")
        os.system("sudo systemctl enable bluetooth.service")
        os.system("sudo systemctl start bluetooth.service")
        os.system("sudo ln -sf /usr/bin/alacritty /usr/bin/xterm")
        os.system("chsh -s /usr/bin/fish")
        os.system("sudo chmod -R 700 ~/.config/*")

        Logger.add_record("[+] Done")

    @staticmethod
    def configure_folders():
        Logger.add_record("[+] Creating default directories")
        default_folders = "~/Videos ~/Documents ~/Downloads ~/Music ~/Desktop"
        os.system("mkdir -p ~/.config")
        os.system(f"mkdir -p {default_folders}")
        os.system("cp -r Images/ ~/")
        Logger.add_record("[+] Done")

        Logger.add_record("[+] Copying Dotfiles & GTK")
        SystemConfiguration.fix_configs()
        os.system("cp -r config/* ~/.config/")
        os.system("cp Xresources ~/.Xresources")
        os.system("cp gtkrc-2.0 ~/.gtkrc-2.0")
        os.system("cp -r local ~/.local")
        os.system("cp -r themes ~/.themes")
        os.system("cp xinitrc ~/.xinitrc")
        os.system("cp -r bin/ ~/")
        Logger.add_record("[+] Done")

    @staticmethod
    def fix_configs():
        user_name = os.getenv("USER")
        battery, ac_adapter = SystemConfiguration.get_power_supply_info()

        config_directory = "config"
        for root, dirs, files in os.walk(config_directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                Logger.add_record(f"[+] Updating {file_path} with current user: {user_name}")

                with open(file_path, 'r') as file:
                    config_content = file.read()

                config_content = config_content.replace("change_me_to_username", f"{user_name}")
                if battery:
                    config_content = config_content.replace("change_me_to_battery", battery)
                if ac_adapter:
                    config_content = config_content.replace("change_me_to_ac_adapter", ac_adapter)

                with open(file_path, 'w') as file:
                    file.write(config_content)

        Logger.add_record("[+] Done")

    @staticmethod
    def get_power_supply_info():
        power_supply_path = "/sys/class/power_supply/"
        battery = None
        ac_adapter = None

        for item in os.listdir(power_supply_path):
            item_path = os.path.join(power_supply_path, item)

            if os.path.isdir(item_path):
                if 'BAT' in item:
                    battery = item
                elif 'AC' in item:
                    ac_adapter = item
                elif 'AD' in item:
                    ac_adapter = item

        return battery, ac_adapter

    @staticmethod
    def update_pacman_database():
        Logger.add_record("[+] Updating Pacman DataBase")
        os.system("sudo pacman -Sy")
        Logger.add_record("[+] Done")

    @staticmethod
    def install_base_packages():
        Logger.add_record("[+] Installing BSPWM Dependencies")
        os.system("git -C /tmp clone https://aur.archlinux.org/yay.git")
        os.system("cd /tmp/yay && makepkg -si")
        SystemConfiguration.install_packages(packages.BASE_PACKAGES, "pacman")
        SystemConfiguration.install_packages(packages.AUR_PACKAGES, "aur")
        os.system("timeout 10 firefox --headless")
        os.system("sh firefox/install.sh")
        Logger.add_record(f"[+] Firefox styles installed", status=LoggerStatus.SUCCESS)

    @staticmethod
    def install_dev_packages():
        Logger.add_record("[+] Installing Dev Dependencies")
        SystemConfiguration.install_packages(packages.DEV_PACKAGES)
        SystemConfiguration.install_packages(packages.GNOME_OFFICIAL_TOOLS)
        Logger.add_record("[+] Done")

    @staticmethod
    def install_nvidia_drivers():
        SystemConfiguration.install_drivers("nvidia")

    @staticmethod
    def install_amd_drivers():
        SystemConfiguration.install_drivers("amd")

    @staticmethod
    def install_intel_drivers():
        SystemConfiguration.install_drivers("intel")

    @staticmethod
    def install_drivers(type: str):
        Logger.add_record("[+] Installing " + type + " Drivers")
        if type == "nvidia":
            SystemConfiguration.install_packages(packages.NVIDIA_PACKAGES)
        elif type == "amd":
            SystemConfiguration.install_packages(packages.AMD_PACKAGES)
        elif type == "intel":
            SystemConfiguration.install_packages(packages.INTEL_PACKAGES)
        Logger.add_record("[+] Done")

    @staticmethod
    def install_packages(package_names: list, type: str = "pacman"):
        for package in package_names:
            if type == "pacman":
                os.system(f"sudo pacman -S --noconfirm {package}")
            elif type == "aur":
                os.system(f"yay -S --noconfirm {package}")
            Logger.add_record(f"Installed: {package}")
