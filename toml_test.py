import toml
from os import path

toml_path = path.join(path.dirname(path.realpath(__file__)),"config.toml")
config = toml.load(toml_path)
listings = config['samsung_product']
print(listings)
print()
for listing in listings:
    print(listing)
    print()
    print(type(listing))
    print()
print(type(listings))