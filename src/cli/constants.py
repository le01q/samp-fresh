from colorama import Fore, Back

NAME = "SA:MP Fresh Command Line Interface"
REPO_URL = "www.github.com/le01q/sampfresh-cli"
DEVS = "le01q and ne0de"
VERSION = "0.0.2"

LOGO = f'''
   _____         __  __ _____    ______             _      
  / ____|  /\   |  \/  |  __ \  |  ____|           | |     
 | (___   /  \  | \  / | |__) | | |__ _ __ ___  ___| |__   
  \___ \ / /\ \ | |\/| |  ___/  |  __| '__/ _ \/ __| '_ \  
  ____) / ____ \| |  | | |      | |  | | |  __/\__ \ | | | 
 |_____/_/    \_\_|  |_|_|      |_|  |_|  \___||___/_| |_|
'''

MAIN = f'''
    {Fore.GREEN}{LOGO}
    {Fore.WHITE}* Welcome to the official {Fore.GREEN}{NAME}

    {Fore.WHITE}- Developers: {Back.GREEN}{Fore.WHITE}{DEVS}{Back.RESET}

    {Fore.WHITE}- Repository URL: {Back.GREEN}{Fore.WHITE}{REPO_URL}{Back.RESET}

    {Fore.WHITE}- Current version of this CLI: {Back.GREEN}{Fore.WHITE}{VERSION}{Back.RESET}
'''
