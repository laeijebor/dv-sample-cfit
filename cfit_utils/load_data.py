import shutil
import os
import time
# from cfit_utils.log_slack import send_message

def copy_directory_contents(src_dir, dest_dir, prefix=''):
    # Ensure the source directory exists
    if not os.path.exists(src_dir):
        print(f"Source directory {src_dir} does not exist.")
        return

    # Ensure the destination directory exists, if not, create it
    os.makedirs(dest_dir, exist_ok=True)

    # Iterate over all files in the source directory
    for filename in os.listdir(src_dir):
        file_path = os.path.join(src_dir, filename)

        # Check if it's a file and not a directory
        if os.path.isfile(file_path):
            # Create new filename with prefix
            new_filename = prefix + filename
            new_file_path = os.path.join(dest_dir, new_filename)

            # Copy file with new name to destination directory
            shutil.copyfile(file_path, new_file_path)
            print(f"Copied {file_path} to {new_file_path}")

def write_sample_file():
    destination_directory = f'resources/outputs'
    with open(f'{destination_directory}/sample_file.txt', 'w') as f:
        f.write('This is a sample file')

def seed_data(outputs_folder = '/resources/outputs', prefix='99_99_'):
    source_directory = 'test_outputs/99'
    user_id = 99
    destination_directory = f'{outputs_folder}'
#     send_message("Seeding data" + source_directory + " to " + destination_directory)
    print("Seeding data" + source_directory + " to " + destination_directory + " with prefix " + prefix)
    copy_directory_contents(source_directory, destination_directory, prefix)
    local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    write_sample_file()
#     send_message("Finished seeding data at time " + local_time)
