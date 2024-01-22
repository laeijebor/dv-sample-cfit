import shutil
import os
import time
from cfit_utils.log_slack import send_message

def copy_directory_contents(src_dir, dest_dir):
    # Check if source directory exists
    if not os.path.exists(src_dir):
        print("Source directory does not exist.")
        return

    # Create the destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Copy each file and subdirectory from src_dir to dest_dir
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isdir(src_path):
            # Recursively copy a directory
            shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
        else:
            # Copy a file
            shutil.copy2(src_path, dest_path)

def write_sample_file():
    destination_directory = f'resources/outputs'
    with open(f'{destination_directory}/sample_file.txt', 'w') as f:
        f.write('This is a sample file')

def seed_data(outputs_folder = '/resources/outputs'):
    source_directory = 'test_outputs'
    user_id = 99
    destination_directory = f'{outputs_folder}/{user_id}'
    send_message("Seeding data" + source_directory + " to " + destination_directory)
    print("Seeding data" + source_directory + " to " + destination_directory)
    copy_directory_contents(source_directory, destination_directory)
    print("Finished seeding data")
    local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    write_sample_file()
    send_message("Finished seeding data at time " + local_time)
