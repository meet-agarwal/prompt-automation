import sys
import os
from PyQt5.QtWidgets import QApplication

from promptReader import PromptReader
from userInterface import PRDGeneratorUI

def main():
    # Ensure promptreader finds the 'prompt/' folder
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    reader = PromptReader(prompt_root='prompts')
    try:
        config = reader.read_config()
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    # # Optional console‑side preview
    # print("\nAvailable sections and style‑options:\n")
    # for section, styles in config.items():
    #     print(f"{section}:")
    #     for key, desc in styles.items():
    #         print(f"  {key} → {desc}")
    #     print()

    app = QApplication(sys.argv)
    window = PRDGeneratorUI(config=config)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
