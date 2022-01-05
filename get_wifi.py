'''
:file: get_wifi.php								 													 
:brief: This is a code that allows to get the passwords of a computer using operating system subprocesses and regular expression pre-builds modules

:author: AlfredoGlz
:date: May 2021
:version: 1.0
'''

import subprocess # import "subprocesses" of a system like commands etc....
import re # Import "regular expressions"

# netsh wlan show profiles              ->  subprocess to show wlan profiles (the networks of a machine)
# netsh wlan show profile "profile"     ->  subprocess to show the information of a wlan profile (an specific network)

# here we run a subprocess using the "run method" of subprocess module to get the "wlan profiles"
show_profiles = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()

# Here we are using a method of regular expressions (re) called "findall" to find info that cointain some text in "command output"
get_profiles = (re.findall("Perfil de todos los usuarios     : (.*)\r", show_profiles))

# apparently you can define lists in python this way.... (inside of this list we can create dictionaries "dict()" )}
wifi_list = list()

# we check "if we find something with the regular expression"
if len(get_profiles) != 0:

    # for every thing found in the "re" we do an iteration
    for name in get_profiles:
        wifi_profile = dict() # a dictionary is made for every iteration
        show_profile = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output=True).stdout.decode("utf-8", "ignore")
        if re.search("Clave de seguridad                         : Ausente", show_profile):
            continue
        else:
            wifi_profile["ssid"] = name
            show_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True).stdout.decode("utf-8", "ignore")
            get_pass = re.search("Contenido de la clave  : (.*)\r", show_pass)
            if get_pass == None:
                wifi_profile["pass"] = None
            else:
                wifi_profile["pass"] = get_pass[1]

        wifi_list.append(wifi_profile) # the append method can add more "items" to the list

# For each dictionary in the list it will print each dictionary with the information
for every in range(len(wifi_list)):
    print(wifi_list[every])