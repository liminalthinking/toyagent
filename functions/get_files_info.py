import os
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        workdir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(workdir, directory))
        valid_target_dir = os.path.commonpath([workdir, target_dir]) == workdir
        if valid_target_dir is False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory' 
        if os.path.isdir(target_dir) is False:
            return f'Error: "{directory}" is not a directory'
        
        #print(f"{workdir} and {target_dir}")

        listdir = os.listdir(target_dir)
        listfiles = []
        for item in listdir:
            newitem = os.path.join(target_dir, item)
            size = os.path.getsize(newitem)
            is_dir = os.path.isdir(newitem)
            #if os.path.isfile(newdir):
            listfiles.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")
            #if os.path.isdir(newdir):
                #listfiles.append(f"\t- {dir}: file_size={os.path.getsize(newdir)} bytes, is_dir=True")
            

        return "\n".join(listfiles)
    except Exception as e:
        return f"Error: {e}"
