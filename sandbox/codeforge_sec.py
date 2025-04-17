#codeforge security 

import ast
import signal

#Blocking dangerous imports
def check_dangerous_imports(user_code):
    dangerous_imports = {"os", "sys", "subprocess", "shutil", "socket", "psutil",
                         "ctypes", "multiprocessing", "threading", "pickle", "marshal", "shelve",
                         "resource", "pwd", "grp", "crypt", "asyncio", "selectors", "queue",
                         "importlib", "__future__", "__import__", "builtins", "runpy", "traceback", "inspect",
                         "tempfile", "glob", "pathlib", "stat", "urllib", "requests", "http", "ftplib", "smtplib",
    }
    for node in ast.walk(ast.parse(user_code)):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in dangerous_imports:
                    return f"Error: Import of {alias.name} not allowed!"
        elif isinstance(node, ast.ImportFrom):
            if node.module in dangerous_imports:
                return f"Error: Import of {node.module} not allowed!"
            
    return None

#Blocking dangerous functions
safe_functions = __builtins__.__dict__.copy()
forbidden_functions = {
     "exec", "eval", "open", "compile", "input", "globals", "locals", "dir", "vars",
     "getattr", "setattr", "delattr", "__import__", "importlib"
}

for forbidden in forbidden_functions:
    safe_functions.pop(forbidden, None)
    
#Setting a time limit on execution
def timeout_handler(signum, frame):
    raise TimeoutError("Took too long!")


def run_safe(user_code):
    error = check_dangerous_imports(user_code)
    if error:
        return error
    
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(3)
    
    try:
        exec(user_code, {"__builtins__": safe_functions})
    except TimeoutError:
        return "Code took too long to execute!"
    except Exception as e:
        return "An error occurred:", e
    else:
        return "Code executed successfully!"    
    finally:
        signal.alarm(0)    
        
    







    