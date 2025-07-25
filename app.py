# app.py (updated version)

import sys
import os
from PyQt5.QtWidgets import QApplication, QFileDialog
from shutil import copyfile
from promptReader import PromptReader
from userInterface import PRDGeneratorUI
from PyQt5.QtWidgets import QMessageBox
import pandas as pd


def main():
    # Ensure promptreader finds the 'prompt/' folder
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    reader = PromptReader(prompt_root='prompts')
    try:
        config = reader.read_config()
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    app = QApplication(sys.argv)
    window = PRDGeneratorUI(config=config)
    window.show()
    
    def process_prompts(prompts: dict, excel_file: str = 'links.xlsx') -> tuple[dict, str]:
        """
        Reads:
        - 'banners' sheet (one column where header+cells are all URLs),
        - 'Cross Selling' sheet (columns 'Image Link', 'Item ID'),
        - 'header' sheet (first col header 'Shop Name' with row0='Logo Link', second col header is shop name),
        then builds:
        • banner links block → replaces ${banner links}$
        • image links block  → replaces ${image links}$
        • item links block   → replaces ${item links}$
        • logo link          → replaces ${logo link}$
        • shop name          → replaces ${shop_name}$

        Returns updated_prompts, shop_name
        """
        # 1) Load sheets
        xls        = pd.ExcelFile(excel_file)
        df_banners = pd.read_excel(xls, sheet_name='banners')
        df_cross   = pd.read_excel(xls, sheet_name='Cross Selling')
        df_header  = pd.read_excel(xls, sheet_name='header')
        # (menu bar is read if needed)
        # df_menu = pd.read_excel(xls, sheet_name='menu bar')

        # 2) Extract all banner URLs from the single column (header + cells)
        col0 = df_banners.columns[0]
        urls = []
        # if header itself is a URL, include it
        if isinstance(col0, str) and col0.lower().startswith('http'):
            urls.append(col0.strip())
        # then every non-null cell
        urls += df_banners.iloc[:,0].dropna().astype(str).str.strip().tolist()

        banner_lines = [f"banner{idx+1} → {url} , " for idx, url in enumerate(urls)]
        banner_block = "\n".join(banner_lines)

        # 3) Build image‐links block from 'Image Link' column
        img_urls = df_cross['Image Link'].dropna().astype(str).str.strip().tolist()
        image_block = "\n".join(f"Product {i+1}: {u} , " for i, u in enumerate(img_urls))

        # 4) Build eBay item‐links block from 'Item ID'
        item_ids = df_cross['Item ID'].dropna().astype(str).str.strip().tolist()
        item_block = "\n".join(
            f"Product {i+1}: https://www.ebay.com/itm/{item_id} , "
            for i, item_id in enumerate(item_ids)
        )

        # 5) Parse header sheet for shop name & logo link
        #    Header columns look like ['Shop Name', '<your shop>']
        shop_name_col = [c for c in df_header.columns if c.lower() != 'shop name'][0]
        shop_name     = shop_name_col.strip()
        # row0 under 'Shop Name' == 'Logo Link', so logo is in the second column
        logo_link     = str(df_header.iloc[0, 1]).strip()

        # 6) Replace placeholders in prompts
        updated = prompts.copy()
        updated['banner']    = updated.get('banner', '') \
            .replace('${banner links}$', banner_block)

        updated['gallery']   = updated.get('gallery', '') \
            .replace('${image links}$', image_block)

        updated['gallery']   = updated.get('gallery', '') \
            .replace('${item links}$',  item_block)

        updated['header']    = updated.get('header', '') \
            .replace('${logo link}$',   logo_link) 

        return updated



    
    # Connect the generation signal to our handler
    def handle_generation(selection_map):
        try:
            # 1. Read selected prompts
            prompts_sample = reader.read_files_from_folders(selection_map)
            
            prompts = process_prompts(prompts_sample)
            
            # 2. Load the base template (original on disk remains unchanged)
            base_path = os.path.join(reader.prompt_root, 'base_prompt.txt')
            if not os.path.isfile(base_path):
                raise FileNotFoundError(f"Base prompt not found at {base_path}")

            with open(base_path, 'r', encoding='utf-8') as f:
                base_content = f.read()

            # 3. Work on a COPY in memory
            final_content = base_content[:]   # this makes a shallow copy of the string

            for section, text in prompts.items():
                placeholder = f"${{{section}}}$"
                final_content = final_content.replace(placeholder, text)

            # 4. (Optional) If you want a file copy on disk before writing:
            #    copyfile(base_path, base_path + '.filled.txt')
            #    filled_path = base_path + '.filled.txt'
            #    with open(filled_path, 'w', encoding='utf-8') as f:
            #        f.write(final_content)

            # 5. Let the user save the merged content
            save_path, _ = QFileDialog.getSaveFileName(
                window, "Save Complete PRD", "", "Text Files (*.txt);;All Files (*)"
            )
            if save_path:
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(final_content)
                QMessageBox.information(window, "Success", "PRD saved successfully!")

        except Exception as e:
            QMessageBox.critical(window, "Error", f"Failed to generate PRD:\n{str(e)}")

    window.generationRequested.connect(handle_generation)


    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()