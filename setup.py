import setuptools
import configparser as cfg

TVERSION="thebigselector/__version__.py"

conf= cfg.ConfigParser()
conf.read("setup.cfg")
version= conf.get("metadata", "version", fallback="unknown")
v= input(f"Version number: {version}\n\tgive another or press Enter: ").strip()
if v:
    version=v
    conf["metadata"]["version"]= v
    with open("setup.cfg","w") as ff:
        conf.write(ff)

with open(TVERSION,"w") as ff:
    ff.write(f"__version__ = '{version}'")

setuptools.setup()
