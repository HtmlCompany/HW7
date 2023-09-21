from setuptools import setup



setup(name="clean_folders",
      version="0.1.4",
      description="Script sorted files by categories and deleted empty folders",
      entry_points = {"console_scripts": ['clean-folder = clean_folder.clean:main']})