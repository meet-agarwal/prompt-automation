# promptreader.py

import os
import json

class PromptReader:
    def __init__(self, prompt_root='assets'):
        """
        :param prompt_root: path to the folder containing your 6 sub‑folders and section_config.json
        """
        self.prompt_root = prompt_root
        self.config_path = os.path.join(prompt_root, 'section_config.json')

    def read_config(self):
        """
        Reads the JSON at prompt/section_config.json and returns it as a dict.
        """
        if not os.path.isfile(self.config_path):
            raise FileNotFoundError(f"Config file not found at {self.config_path}")
        with open(self.config_path, 'r', encoding='utf‑8') as f:
            return json.load(f)

    def read_files_from_folders(self, selection_map):
        """
        Given a dict mapping each section to a style key,
        reads the corresponding <styleKey>.txt file from each folder.

        :param selection_map: e.g.
            {
                "banner": "style2",
                "footer": "style3",
                "header": "style1",
                "product": "style2",
                "information": "style1",
                "galler": "style1",
            }
        :returns: dict mapping each section to the raw text of its selected file
        :rtype: dict[str, str]
        """
        
        print("inside the read file method")
        result = {}
        for section, style_key in selection_map.items():
            filename = f"{style_key}.txt"
            file_path = os.path.join(self.prompt_root, section, filename)

            if not os.path.isfile(file_path):
                raise FileNotFoundError(
                    f"No file for section '{section}' with key '{style_key}': {file_path}"
                )

            with open(file_path, 'r', encoding='utf‑8') as f:
                result[section] = f.read()

        return result
