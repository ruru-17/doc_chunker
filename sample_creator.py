import requests
from pathlib import Path
import os

url = "http://127.0.0.1:8000/chunk_pdf/"

input_dir = Path("input_files")
output_dir = Path("output_files")

input_files = [str(file) for file in input_dir.iterdir() if file.is_file()]

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
                        print(confignum_current,"out of", confignum, "-- Status Code:", response.status_code)
                        confignum_current+=1