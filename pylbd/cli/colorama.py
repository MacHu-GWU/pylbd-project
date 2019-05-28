# -*- coding: utf-8 -*-

try:
    from ..pkg.colorama import init, Fore, Back, Style
except:  # pragma: no cover
    from pylbd.pkg.colorama import init, Fore, Back, Style

print(Fore.RED + 'some red text' + Fore.BLUE + ' other text')
print("adsf")
