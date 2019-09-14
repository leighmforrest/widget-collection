import os
from django.core.management.base import BaseCommand

MODULE = 'djangox_project'


class Command(BaseCommand):
    """
    Command to rename a project.
    Works Cited:
    Just Django 'Creating a Django boilerplate - 4 //
        how to create custom Django commands' https://youtu.be/qrsq8g6bqbE
        Oct 22, 2018. Accessed August 5, 2019.
    """
    help = 'Renames a Django project'

    def add_arguments(self, parser):
        parser.add_argument('new_project_name', type=str, help='The new Django project name')

    def handle(self, *args, **kwargs):
        new_project_name = kwargs['new_project_name']

        # logic for renaming the files

        files_to_rename = [f'{MODULE}/settings.py', f'{MODULE}/wsgi.py', 'manage.py']
        folder_to_rename = MODULE

        for f in files_to_rename:
            with open(f, 'r') as file:
                filedata = file.read()

            filedata = filedata.replace(MODULE, new_project_name)

            with open(f, 'w') as file:
                file.write(filedata)

        os.rename(folder_to_rename, new_project_name)

        self.stdout.write(self.style.SUCCESS(
            f'Project has been renamed to {new_project_name}'))
