import random

solo_performers = [
    "Ariana Grande", "Ed Sheeran", "Billie Eilish", "Drake", "Taylor Swift",
    "Justin Bieber", "Dua Lipa", "The Weeknd", "Sam Smith", "Harry Styles",
    "Lady Gaga", "Bruno Mars", "Adele", "Post Malone", "Shawn Mendes",
    "Sia", "Khalid", "Halsey", "Travis Scott", "Lizzo"
]

djs = [
    "Calvin Harris", "David Guetta", "Tiësto", "Martin Garrix", "Marshmello",
    "Zedd", "Deadmau5", "Avicii", "Steve Aoki", "Armin van Buuren",
    "Diplo", "Skrillex", "Kygo", "Alesso", "Hardwell"
]

bands = [
    "Coldplay", "Imagine Dragons", "Maroon 5", "OneRepublic", "The Killers",
    "Arctic Monkeys", "Red Hot Chili Peppers", "Foo Fighters", "Muse", "Green Day",
    "Linkin Park", "Panic! At The Disco", "Paramore", "The 1975", "Twenty One Pilots"
]

def generate_random_names(list):

    name=random.choice(list)
    return f"{name} {random_num_gen(1,1000)}"
    

def random_num_gen(lower,upper):
    return random.randint(lower,upper)

