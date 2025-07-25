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
    
    # def process_prompts(prompts: dict, excel_file: str = 'links.xlsx') -> tuple[dict, str]:
    #     import re

    #     # Load Excel
    #     xls = pd.ExcelFile(excel_file)
    #     df_banners = pd.read_excel(xls, sheet_name='banners')
    #     df_cross = pd.read_excel(xls, sheet_name='Cross Selling')
    #     df_header = pd.read_excel(xls, sheet_name='header')
    #     df_menu = pd.read_excel(xls, sheet_name='menu bar')

    #     # Banner block
    #     col0 = df_banners.columns[0]
    #     urls = []
    #     if isinstance(col0, str) and col0.lower().startswith('http'):
    #         urls.append(col0.strip())
    #     urls += df_banners.iloc[:, 0].dropna().astype(str).str.strip().tolist()
    #     banner_block = "\n".join([f"banner{idx+1} → {url} ," for idx, url in enumerate(urls)])

    #     # Image links and item links
    #     img_urls = df_cross['Image Link'].dropna().astype(str).str.strip().tolist()
    #     image_block = "\n".join(f"Product {i+1}: {u} ," for i, u in enumerate(img_urls))
    #     item_ids = df_cross['Item ID'].dropna().astype(str).str.strip().tolist()
    #     item_block = "\n".join(
    #         f"Product {i+1}: https://www.ebay.com/itm/{item_id} , " for i, item_id in enumerate(item_ids)
    #     )

    #     # Header info
    #     header_map = pd.Series(df_header.iloc[:, 1].values, index=df_header.iloc[:, 0]).to_dict()

    #     shop_name = str(header_map.get('Shop Name', '')).strip()
    #     store_name = str(header_map.get('Store Name', '')).strip()
    #     logo_link  = str(header_map.get('Logo Link', '')).strip()

    #     shop_name = shop_name.strip()
    #     store_name = store_name.strip()
    #     store_name = re.sub(r'\s+', '', store_name).lower()
    #     shop_name = re.sub(r'\s+', '', shop_name).lower()

    #     # Default menu list (normalized)
    #     default_menu_titles = ['about us', 'contact us', 'feedback', 'new arrival', 'on sale']
        # default_menu_links = {
        #     'about us': f'https://www.ebay.com/str/{store_name}?_tab=about',
        #     'on sale': f'https://www.ebay.com/str/{store_name}?_tab=sales',
        #     'feedback': f'https://www.ebay.com/str/{store_name}?_tab=feedback',
        #     'new arrival': f'https://www.ebay.com/sch/i.html?_dkr=1&iconV2Request=true&_blrs=recall_filtering&_ssn={shop_name}&store_name={store_name}&_sop=10&_oac=1',
        #     'contact us': f'https://www.ebay.com/cnt/intermediatedFAQ?requested={shop_name}'
        # }

    #     # MENU STRUCTURE
    #     menu_structure_lines = []
    #     menu_links_lines = []

    #     # Convert menu bar into dict format
    #     menu_dict = {}
    #     for col in df_menu.columns:
    #         parent = col.strip().lower()
    #         children = df_menu[col].dropna().astype(str).str.strip().str.lower().tolist()
    #         if children:
    #             menu_dict[parent] = children
    #         else:
    #             menu_dict[parent] = []

    #     # Flatten keys and children
    #     all_flat_menus = set(menu_dict.keys()).union(*menu_dict.values())
    #     if all_flat_menus == set(default_menu_titles):
    #         # Use default menu
    #         for item in default_menu_titles:
    #             link = default_menu_links[item]
    #             menu_links_lines.append(f"{item.title()} - {link}")
    #         menu_structure_lines = [item.title() for item in default_menu_titles]
    #     else:
    #         # Custom menu
    #         for parent, children in menu_dict.items():
    #             display_parent = parent.title()
    #             # Get link
    #             if parent in default_menu_links:
    #                 link = default_menu_links[parent]
    #             else:
    #                 link = f"https://www.ebay.com/sch/i.html?_dkr=1&iconV2Request=true&_blrs=recall_filtering&store_name={shop_name}&_oac=1&_nkw={parent.replace(' ', '+')}"
    #             menu_links_lines.append(f"{display_parent} - {link}")

    #             if children:
    #                 formatted_children = ", ".join(child.title() for child in children)
    #                 menu_structure_lines.append(f"{display_parent} - {formatted_children}")
    #             else:
    #                 menu_structure_lines.append(display_parent)

    #     menu_links_text = "Menu Links\n" + "\n".join(menu_links_lines)
    #     menu_structure_text = "Menu Structure\n" + "\n".join(menu_structure_lines)

    #     full_menu_block = f"{menu_links_text}\n\n{menu_structure_text}"

    #     # Placeholder Replacement with Error Logging
    #     errors = []
    #     updated = prompts.copy()

    #     def check_replace(key, placeholder, replacement):
    #         text = updated.get(key, '')
    #         if placeholder not in text:
    #             errors.append(f"Missing {placeholder} in prompts['{key}']")
    #         updated[key] = text.replace(placeholder, replacement)

    #     check_replace('banner', '${banner links}$', banner_block)
    #     check_replace('gallery', '${image links}$', image_block)
    #     check_replace('gallery', '${item links}$', item_block)
    #     check_replace('header', '${logo link}$', logo_link)
    #     check_replace('header', '${menu}$', full_menu_block)
        
    #     # Add the new replacements for shop_name and store_name
    #     # check_replace('header', '{shop_name}', shop_name)
    #     # check_replace('header', '{store_name}', store_name)
        
    #     # You might want to check other keys that might contain these placeholders
    #     for key in updated:
    #         if key != 'header':  # We already processed header
    #             updated[key] = updated[key].replace('{shop_name}', shop_name)
    #             updated[key] = updated[key].replace('{store_name}', store_name)

    #     if errors:
    #         raise ValueError("Placeholder replacement errors:\n" + "\n".join(f"  - {e}" for e in errors))

    #     return updated

    def process_prompts(prompts: dict, excel_file: str = 'links.xlsx') -> dict:
        import re
        import pandas as pd

        # Load Excel
        xls = pd.ExcelFile(excel_file)
        df_banners = pd.read_excel(xls, sheet_name='banners')
        df_cross = pd.read_excel(xls, sheet_name='Cross Selling')
        df_header = pd.read_excel(xls, sheet_name='header')
        df_menu = pd.read_excel(xls, sheet_name='menu bar')

        # ------------------ BANNER ------------------
        col0 = df_banners.columns[0]
        urls = []
        if isinstance(col0, str) and col0.lower().startswith('http'):
            urls.append(col0.strip())
        urls += df_banners.iloc[:, 0].dropna().astype(str).str.strip().tolist()
        banner_block = "\n".join([f"banner{idx+1} → {url} ," for idx, url in enumerate(urls)])

        # ------------------ IMAGE LINKS & ITEM LINKS ------------------
        img_urls = df_cross['Image Link'].dropna().astype(str).str.strip().tolist()
        image_block = "\n".join(f"Product {i+1}: {u} ," for i, u in enumerate(img_urls))
        item_ids = df_cross['Item ID'].dropna().astype(str).str.strip().tolist()
        item_block = "\n".join(
            f"Product {i+1}: https://www.ebay.com/itm/{item_id} , " for i, item_id in enumerate(item_ids)
        )

        # ------------------ HEADER INFO ------------------
        header_map = pd.Series(df_header.iloc[:, 1].values, index=df_header.iloc[:, 0]).to_dict()
        shop_name = str(header_map.get('Shop Name', '')).strip()
        store_name = str(header_map.get('Store Name', '')).strip()
        logo_link  = str(header_map.get('Logo Link', '')).strip()

        # Clean versions
        store_name = re.sub(r'\s+', '', store_name).lower()
        shop_name = re.sub(r'\s+', '', shop_name).lower()

        # ------------------ DEFAULT MENU ------------------
        default_menu_titles = ['about us', 'contact us', 'feedback', 'new arrival', 'on sale']
        default_menu_links = {
            'about us': f'https://www.ebay.com/str/{store_name}?_tab=about',
            'on sale': f'https://www.ebay.com/str/{store_name}?_tab=sales',
            'feedback': f'https://www.ebay.com/str/{store_name}?_tab=feedback',
            'new arrival': f'https://www.ebay.com/sch/i.html?_dkr=1&iconV2Request=true&_blrs=recall_filtering&_ssn={shop_name}&store_name={store_name}&_sop=10&_oac=1',
            'contact us': f'https://www.ebay.com/cnt/intermediatedFAQ?requested={shop_name}'
        }

        # ------------------ MENU STRUCTURE ------------------
        menu_structure_lines = []
        menu_links_lines = []

        # Convert menu bar sheet into dict
        menu_dict = {}
        for col in df_menu.columns:
            parent = col.strip().lower()
            children = df_menu[col].dropna().astype(str).str.strip().str.lower().tolist()
            menu_dict[parent] = children if children else []

        # Decide default or custom
        all_flat_menus = set(menu_dict.keys()).union(*menu_dict.values())
        if all_flat_menus == set(default_menu_titles):
            # Use default
            for item in default_menu_titles:
                link = default_menu_links[item]
                menu_links_lines.append(f"{item.title()} - {link}")
                menu_structure_lines.append(item.title())
        else:
            # Custom: generate links for children instead of parent
            for parent, children in menu_dict.items():
                display_parent = parent.title()

                if children:
                    formatted_children = ", ".join(child.title() for child in children)
                    menu_structure_lines.append(f"{display_parent} - {formatted_children}")

                    for child in children:
                        display_child = child.title()
                        if child in default_menu_links:
                            link = default_menu_links[child]
                        else:
                            base_url = "https://www.ebay.com/sch/i.html?_dkr=1&iconV2Request=true&_blrs=recall_filtering"
                            link = f"{base_url}&_ssn={shop_name}&_oac=1&_nkw={child.replace(' ', '%')}"
                        menu_links_lines.append(f"{display_child} - {link}")
                else:
                    menu_structure_lines.append(display_parent)
                    if parent in default_menu_links:
                        link = default_menu_links[parent]
                    else:
                        base_url = "https://www.ebay.com/sch/i.html?_dkr=1&iconV2Request=true&_blrs=recall_filtering"
                        link = f"{base_url}&_ssn={shop_name}&_oac=1&_nkw={parent.replace(' ', '%')}"
                    menu_links_lines.append(f"{display_parent} - {link}")

        menu_links_text = "Menu Links\n" + "\n".join(menu_links_lines)
        menu_structure_text = "Menu Structure\n" + "\n".join(menu_structure_lines)
        full_menu_block = f"{menu_links_text}\n\n{menu_structure_text}"

        # ------------------ PLACEHOLDER REPLACEMENT ------------------
        errors = []
        updated = prompts.copy()

        def check_replace(key, placeholder, replacement):
            text = updated.get(key, '')
            if placeholder not in text:
                errors.append(f"Missing {placeholder} in prompts['{key}']")
            updated[key] = text.replace(placeholder, replacement)

        check_replace('banner', '${banner links}$', banner_block)
        check_replace('gallery', '${image links}$', image_block)
        check_replace('gallery', '${item links}$', item_block)
        check_replace('header', '${logo link}$', logo_link)
        check_replace('header', '${menu}$', full_menu_block)

        # Global shop/store replacements
        for key in updated:
            updated[key] = updated[key].replace('{shop_name}', shop_name)
            updated[key] = updated[key].replace('{store_name}', store_name)

        if errors:
            raise ValueError("Placeholder replacement errors:\n" + "\n".join(f"  - {e}" for e in errors))

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