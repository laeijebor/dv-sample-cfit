from cfit_utils.load_data import seed_data
# import os
# import json
# import subprocess
# import builtins
# from typing import Any
#
# # Save a reference to the original built-in print function
# original_print = print
#
# def custom_print(*args, **kwargs) -> None:
#     # Call the original print function to log locally
#     original_print(*args, **kwargs)
#
#     # Convert the print arguments to a string
#     message = ' '.join(map(str, args))
#
#     # Slack webhook URL
#     webhook_url = 'https://hooks.slack.com/services/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'
#
#     # Prepare the payload
#     payload = {'text': message}
#     data = json.dumps(payload)
#
#     # Execute the curl command
#     command = f"curl -X POST -H 'Content-type: application/json' --data '{data}' {webhook_url}"
#     subprocess.run(command, shell=True)
#
# # Monkey patch the built-in print function
# print = custom_print
# builtins.print = custom_print

if __name__ == "__main__":
    seed_data()
    print("DONE")
