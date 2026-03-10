import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the contents in a specified file relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of file to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file_path"
            )
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        workdir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(workdir, file_path))
        valid_file = os.path.commonpath([workdir, target_file]) == workdir
        if valid_file is False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        parentdir = os.path.dirname(target_file)
        os.makedirs(parentdir, exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"


