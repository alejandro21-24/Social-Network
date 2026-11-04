class Person:
    """A person (node) in the social network."""

    def __init__(self, name):
        self.name = name
        self.friends = []  # list of Person objects this person is connected to

    def add_friend(self, friend):
        """Add a Person to this person's friends list (ignores duplicates)."""
        if friend not in self.friends:
            self.friends.append(friend)


class SocialNetwork:
    """A graph of Person objects stored as an adjacency list."""

    def __init__(self):
        self.people = {}  # name -> Person

    def add_person(self, name):
        """Create a Person and store it by name. Duplicates are rejected."""
        if name in self.people:
            print(f"Person not added. {name} already exists!")
            return
        self.people[name] = Person(name)

    def add_friendship(self, person1_name, person2_name):
        """Create a bidirectional friendship between two existing people."""
        if person1_name not in self.people:
            print(f"Friendship not created. {person1_name} doesn't exist!")
            return
        if person2_name not in self.people:
            print(f"Friendship not created. {person2_name} doesn't exist!")
            return
        if person1_name == person2_name:
            print("Friendship not created. A person can't befriend themselves!")
            return

        person1 = self.people[person1_name]
        person2 = self.people[person2_name]
        person1.add_friend(person2)
        person2.add_friend(person1)

    def print_network(self):
        """Print every person and the names of their friends."""
        for name, person in self.people.items():
            friend_names = ", ".join(friend.name for friend in person.friends)
            print(f"{name} is friends with: {friend_names}")


if __name__ == "__main__":
    network = SocialNetwork()

    # Add people (6 people)
    for name in ["Alex", "Jordan", "Morgan", "Taylor", "Casey", "Riley"]:
        network.add_person(name)

    # Edge case: duplicate person
    network.add_person("Alex")  # "Person not added. Alex already exists!"

    # Create friendships (8 valid friendships)
    network.add_friendship("Alex", "Jordan")
    network.add_friendship("Alex", "Morgan")
    network.add_friendship("Jordan", "Taylor")
    network.add_friendship("Morgan", "Casey")
    network.add_friendship("Taylor", "Riley")
    network.add_friendship("Casey", "Riley")
    network.add_friendship("Morgan", "Riley")
    network.add_friendship("Alex", "Taylor")

    # Edge cases
    network.add_friendship("Jordan", "Johnny")  # Johnny doesn't exist
    network.add_friendship("Alex", "Jordan")    # duplicate friendship (ignored)
    network.add_friendship("Casey", "Casey")    # self-friendship

    print()
    network.print_network()


"""
DESIGN MEMO

A graph is the right structure for a social network because friendships are relationships between people, not a hierarchy. Each person is a node and each friendship is an edge that works in both directions: if Alex is friends with Jordan, Jordan is also friends with Alex. A graph lets anyone connect to any number of people, and new connections can be added at any time without restructuring anything.

A list or tree would not work as well. A list only stores items in a line, so it cannot show who is connected to whom. A tree has one root and every node has exactly one parent, so it cannot contain cycles. In my test network, Alex, Jordan and Taylor are all friends with each other, forming a triangle, which a tree cannot represent.

I used an adjacency list: a dictionary maps names to Person objects, and each Person keeps a list of friends. Adding a person and looking up two people are O(1) on average. Checking for an existing friendship is O(k), where k is the number of friends, because it scans a list. Printing is O(V + E), since it visits every person and friendship once. An adjacency matrix would make friend checks O(1) but use O(V^2) memory, which is wasteful because most people are not friends.
"""