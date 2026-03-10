import os
import sys
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
#from functions.get_files_info import get_files_info
#from functions.get_file_content import get_files_info
from prompts import system_prompt
from call_function import ( available_functions, call_function )
from config import MAX_ITERS


def main():
    #print("Hello from toyagent!")

    

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Gemini api key not set")
    client = genai.Client(api_key = api_key)

    

    parser = argparse.ArgumentParser(description="Agent")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    for _ in range(MAX_ITERS):
        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print(f"Final response: {final_response}")
                return
        except Exception as e:
            print(f"Error in generating content: {e}")

    print(f"Maximum iterations ({MAX_ITERS}) reached")
    sys.exit(1)
    
def generate_content(client, messages, verbose):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,        
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature=0),
    )

    if not response.usage_metadata:
        raise RuntimeError("No usage metadata available")
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)
    
    if verbose:
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    function_result_list = []

    if response.function_calls != None:
        for call in response.function_calls:
       
            function_call_result = call_function(call, verbose)
            if function_call_result.parts == []:
                raise Exception("Parts is empty")
            if function_call_result.parts[0].function_response == None:
                raise Exception("Function response object is None")
            if function_call_result.parts[0].function_response.response == None:
                raise Exception("Function result is None")
            function_result_list.append(function_call_result.parts[0])
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
                #Calling function: {call.name}({call.args})")
            #else:
             #   print(f"-> Calling function: {call.name}")
        messages.append(types.Content(role="user", parts=function_result_list))

    else:
        return response.text

if __name__ == "__main__":
    main()
