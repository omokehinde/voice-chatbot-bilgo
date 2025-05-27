from faker import Faker
import pandas as pd
import random

fake = Faker()
locations = ['Mayfair', 'Chelsea', 'Soho', 'Notting Hill', 'Camden', 'Greenwich', 'Kensington']

data = []

for _ in range(100):
    name = fake.company() + " Residence"
    location = random.choice(locations)
    description = f"{fake.sentence()} Located in {location}, one of London's popular districts."
    data.append({'Name': name, 'Location': location, 'Description': description})

df = pd.DataFrame(data)
df.to_csv('data/properties.csv', index=False)
