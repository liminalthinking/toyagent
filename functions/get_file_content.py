import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Prints file contents in a specified file relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of file to print, relative to the working directory",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        workdir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(workdir, file_path))
        valid_dir = os.path.commonpath([target_dir, workdir]) == workdir
        if valid_dir is False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_dir) is False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_dir, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
    except Exception as e:
        return f"Error: {e}"



