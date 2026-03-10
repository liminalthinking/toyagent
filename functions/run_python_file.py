import os
import subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the python file on the file path relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of python file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="The arguments to pass into the python file to run"
            )
        },
    ),
)


def run_python_file(working_directory, file_path, args=None):
    try:    
        workdir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(workdir, file_path))
        valid_file = os.path.commonpath([workdir, target_file]) == workdir
        if valid_file is False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_file]
        if args:
            command.extend(args)
        result = subprocess.run(
            command,
            cwd = workdir,
            capture_output = True,
            text=True,
            timeout=30,
        )
        
        output = []

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        if result.stdout:
            output.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            output.append(f"STDERR: {result.stderr}")

        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"



