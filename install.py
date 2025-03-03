import subprocess

def install_packages():
    packages = ["libpangoft2-1.0-0", "libglib2.0-0"]
    try:
        # Update package lists
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        
        # Install packages
        for pkg in packages:
            subprocess.run(["sudo", "apt-get", "install", "-y", pkg], check=True)
        print("Packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing packages: {e}")

if __name__ == "__main__":
    install_packages()