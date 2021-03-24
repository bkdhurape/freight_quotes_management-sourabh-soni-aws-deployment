# Folder Structure

We will have a folder called config that will have the root urls.py and settings.py files

Each app will have the following

- A models directory
    - We will have one file per model inside this directory
- An API directory
    - This will in turn have directories for different versions V1, V2 etc.
    - Iniside this we have one file for each ViewSet
- A services direcotry
    - This will have files with buisness logic
- A query set directory
    - files with queryset managers for our models
- A test directory
    - this will have sub-directories for models, services etc.
    - unit tests files will be inside each sub-directory
- A serializers.py file
    - all the serializers used in our app
