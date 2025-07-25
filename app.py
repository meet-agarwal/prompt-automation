import promptReader
import os

if __name__ == "__main__":
    reader = promptReader.PromptReader()

    # Read the config
    config = reader.read_config()
    print("Config:", config)

   