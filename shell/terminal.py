import os

#Rich is a Python library for rich text and beautiful formatting in the terminal
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text

#prompt_toolkit library for building powerful interactive command line applications in Python.
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import PathCompleter

import importlib #Dynamically imports plugins/modules at runtime (for extensibility)
import subprocess #Runs real system commands (like npx, git, npm, etc.)


console = Console() #Create a Console object which acts like a fancier version of sys.stdout/print that can handle colors, layout, and animations.
session = PromptSession(completer = PathCompleter(expanduser=True)) #We can use session.prompt() to act as replacement 'input()' and allow cutomisation 



def startShell():
    startingMSG = Text("Welcome to ", style="cyan") + Text("CustomShell", style="bold magenta") + Text(" - Type 'help' to start!", style="cyan")
    console.print(startingMSG)

    while True:
        try:
            cwd = os.getcwd() # Stores the current dir
            
            console.print(f"[bold green]{cwd}> [/]", end="")
            cmd = session.prompt()
            
            handleCommand(cmd)
        except (KeyboardInterrupt, EOFError):
            console.print("\n[red]Session terminated[/]")
            break

def handleCommand(cmd):
    if not cmd.strip():
        return

    partsArray = cmd.strip().split()
    name = partsArray[0]
    args = partsArray[1:]

    if name == "help":
        console.print("Available commands: help, cd, exit")
    elif name == "exit":
        exit()
    elif name == "cd":
        if args:
            target_dir = os.path.abspath(args[0])
            try:
                os.chdir(target_dir)
            except Exception as e:
                console.print(f"[red]cd failed:[/] {e}")
        else:
            console.print("[yellow]Usage:[/] cd <directory>")
    else:
        try:
            subprocess.run([name] + args, check=True)
        except FileNotFoundError:
            console.print(f"[red]Command not found:[/] {name}")
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Command failed:[/] {e}")
