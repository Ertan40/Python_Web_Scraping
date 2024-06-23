import subprocess
import sys
import schedule
import time


def install_dependencies():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("All dependencies are installed.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)


def run_scraping_service():
    script_path = 'C:\\Users\\ertan\\PycharmProjects\\python_web_scraping_demos\\automate_deployment\\03-country_population.py'
    process = subprocess.Popen([sys.executable, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(f"Output:\n{stdout.decode()}")
    print(f"Errors:\n{stderr.decode()}")
    if process.returncode != 0:
        print(f"Service crashed with return code {process.returncode}.")
    else:
        print("Service completed successfully.")


if __name__ == "__main__":
    install_dependencies()

    # Schedule the task to run every day at 16:00 (4:00 PM)
    schedule.every().day.at("16:00").do(run_scraping_service)

    print("Scheduled web scraping service to run every day at 16:00 PM.")

    while True:
        schedule.run_pending()
        time.sleep(1)


