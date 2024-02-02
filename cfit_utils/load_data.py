import shutil
import os
import time
import json

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






def read_json(source_dir, filename):
    path = f'{source_dir}/{filename}'
    if not os.path.exists(path):
        print(f"Source directory {source_dir} does not exist.")
        return {}
    with open(path, 'r') as f:
        return json.load(f)

def get_main_file(dir = '/resources/outputs'):
    return read_json(dir, 'data.json')


def output_main_file(main_file, dir = '/resources/outputs'):
    with open(f'{dir}/data.json', 'w') as f:
        f.write(json.dumps(main_file, indent=4))

def add_global_scenario(scenario_id, outdir='/resources/outputs'):
    print(f"Adding global scenario {scenario_id}")
    source_directory = f'test_outputs/{scenario_id}'

    files = os.listdir(source_directory)
    print(f"Files in {source_directory}: {files}")

    scenario_file = {}
    key = scenario_id

    scenario_file[key] = {}

    for filename in files:
        if filename == 'data.json':
            continue
        if not filename.endswith('.json'):
            continue
        data_key = filename[:-5]
        scenario_file[key][data_key] = read_json(source_directory, filename)

    with open(f'{outdir}/{scenario_id}.json', 'w') as f:
        f.write(json.dumps(scenario_file, indent=4))
    print(f'Added global scenario {scenario_id} to {outdir}')

def seed_data(outputs_folder = '/resources/outputs'):
    print(f"Seeding data in {outputs_folder}")
    add_global_scenario('99', outputs_folder)
    add_global_scenario('20', outputs_folder)
    add_global_scenario('25', outputs_folder)

def add_user_scenario(user_id, scenario_id, outdir='/resources/outputs'):
    print(f"Adding user scenario_id {user_id} {scenario_id}")
    source_directory = f'test_outputs/{scenario_id}'

    files = os.listdir(source_directory)
    print(f"Files in {source_directory}: {files}")

    main_file = get_main_file(outdir)
    key = f'{user_id}_{scenario_id}'
    if not main_file:
        main_file = {}

    if key not in main_file:
        main_file[key] = {}

    for filename in files:
        if filename == 'data.json':
            continue
        if not filename.endswith('.json'):
            continue
        data_key = filename[:-5]
        main_file[key][data_key] = read_json(source_directory, filename)

    output_main_file(main_file, outdir)


if __name__ == "__main__":
    add_user_scenario('99', '99')
    print("DONE")
