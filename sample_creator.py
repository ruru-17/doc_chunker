import requests
from pathlib import Path
import os
import time

url = "http://127.0.0.1:8000/chunk_pdf/"

input_dir = Path("input_files")
output_dir = Path("output_files")

# input_files = [str(file) for file in input_dir.iterdir() if file.is_file()]
input_files = [
    # 'input_files\\646559812-Agreement-Scanned.pdf', #done
    'input_files\\795397007-CONTRACT.pdf', 
    # 'input_files\\sv600_c_automatic.pdf' #done
    ]

param_grid = {
    "max_characters": [250, 500, 750, 1000],
    "new_after_n_chars": [250, 500, 750, 1000],
    "overlap": [0, 100, 200, 300],
    "overlap_all": [True, False],
    "combine_text_under_n_chars": [0, 100, 250, 500, 750]
}

confignum = 0

for max_characters in param_grid["max_characters"]:
    for new_after_n_chars in param_grid["new_after_n_chars"]:
        if new_after_n_chars > max_characters:
            continue
        for overlap in param_grid["overlap"]:
            if overlap > new_after_n_chars:
                continue
            for overlap_all in param_grid["overlap_all"]:
                for combine_text_under_n_chars in param_grid["combine_text_under_n_chars"]:
                    if combine_text_under_n_chars > new_after_n_chars:
                        continue
                    for file in input_files:
                        confignum +=1

print("Total number of outputs to be created:", confignum)

confignum_current = 1

last_n_times = []  # Store time for last n iterations
n = len(input_files)

for max_characters in param_grid["max_characters"]:
    for new_after_n_chars in param_grid["new_after_n_chars"]:
        if new_after_n_chars > max_characters:
            continue
        for overlap in param_grid["overlap"]:
            if overlap > new_after_n_chars:
                continue
            for overlap_all in param_grid["overlap_all"]:
                for combine_text_under_n_chars in param_grid["combine_text_under_n_chars"]:
                    if combine_text_under_n_chars > new_after_n_chars:
                        continue
                    for file in input_files:

                        start_time = time.time()

                        form_data = {
                            "max_characters": str(max_characters),
                            "new_after_n_chars": str(new_after_n_chars),
                            "overlap": str(overlap),
                            "overlap_all": str(overlap_all),
                            "combine_text_under_n_chars": str(combine_text_under_n_chars),
                            "output_dir": f"{str(output_dir)}/max_characters_{max_characters}/new_after_n_chars_{new_after_n_chars}/overlap_{overlap}/overlap_all_{overlap_all}/combine_text_under_n_chars_{combine_text_under_n_chars}"
                        }
                        file_to_upload = {"file": (os.path.basename(file), open(file, "rb"), "application/pdf")}
                        response = requests.post(url, headers=form_data, files=file_to_upload)

                        elapsed_time = time.time() - start_time
                        last_n_times.append(elapsed_time)
                        if len(last_n_times) > n:
                            last_n_times.pop(0)  # Keep only the last n times

                        # Estimate time remaining
                        avg_time_per_iter = sum(last_n_times) / len(last_n_times)
                        iterations_left = confignum - confignum_current
                        estimated_time_remaining = iterations_left * avg_time_per_iter

                        # Print progress
                        print(
                            f"{confignum_current} out of {confignum} -- Status Code: {response.status_code} -- "
                            f"Time Taken: {elapsed_time:.2f}s -- Estimated Time Remaining: {estimated_time_remaining / 60:.2f} minutes"
                        )
                        confignum_current+=1