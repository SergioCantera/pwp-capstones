import weakref

class User(object):
    """Class for create a user object in TomeRater.py"""
    
    def __init__(self, name, email):
        self.name = name #will be a string
        self.email = email #will be a string
        self.books = {} #empty dictionary with key = Book object and value = user's rating

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address.email
        print("User's email has been updated")

    def __repr__(self):
        return "User {name}, email: {email}, books read: {books}".format(name = self.name, email = self.email, books = self.books)

    def __eq__(self, other_user):
        if self.name == other_user.name and self.email == other_user.email:
            return True
        else:
            return False

    def read_book(self, book, rating = None):
        self.books[book] = rating

    def get_average_rating(self):
        total_value = 0
        num_values = 0
        for value in self.books.values():
            if value != None:
                total_value += value
                num_values += 1
        return total_value / num_values 

class Book:
    """Class which define a book object in TomeRater.py"""

    _instances = set()

    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = [] #empty list of book's ratings
        self._instances.add(weakref.ref(self))

    @classmethod
    def getinstances(cls):
        book = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                book.add(ref)
        cls._instances -= book

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, isbn):
        self.isbn = isbn
        print("Book's ISBN has been updated")

    def add_rating(self, rating):
        if rating != None:
            self.ratings.append(rating)
        else:
            print("Invalid rating")

    def __eq__(self, other_book):
        if self.title == other_book.title and self.isbn == other_book.isbn:
            return True
        else:
            return False

    def get_average_rating(self):
        total_rating = 0
        for rating in self.ratings:
            total_rating += rating
        return total_rating / len(self.ratings)

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __repr__(self):
        return "{title}, ISBN: {isbn}".format(title = self.title, isbn = self.isbn)

class Fiction(Book):
    """Subclass of Book for creating Fiction book objects"""
    
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title = self.title, author = self.author)

class Non_Fiction(Book):
    """Subclass of Book for creating Non Fiction book objects"""
    
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title = self.title, level = self.level, subject = self.subject)

class TomeRater():
    """Application which store users and books and set interactions between both"""
    
    def __init__(self):
        self.users = {} #map user's email to the corresponding User object
        self.books = {} #map a Book object to the number of Users that have read it

    def create_book(self, title, isbn):
        if self.check_unique_isbn(isbn):
            self.new_book = Book(title, isbn)
            return self.new_book
        else:
            print("This ISBN already exists for a book!")

    def create_novel(self, title, author, isbn):
        if self.check_unique_isbn(isbn):
            self.new_novel = Fiction(title, author, isbn)
            return self.new_novel
        else:
            print("This ISBN already exists for a book!")

    def create_non_fiction(self, title, subject, level, isbn):
        if self.check_unique_isbn(isbn):
            self.new_non_fiction = Non_Fiction(title, subject, level, isbn)
            return self.new_non_fiction
        else:
            print("This ISBN already exists for a book!")

    def check_unique_isbn(self, new_isbn):
        for obj in Book.getinstances():
            if new_isbn == obj.isbn:
                return False
        return True
        
    def add_book_to_user(self, book, email, rating = None):
        user = self.users.get(email)
        if user in self.users.values():
            user.read_book(book, rating)
            book.add_rating(rating)
            if book not in self.books:
                self.books[book] = 1
            else:
                self.books[book] = self.books[book] + 1
        else:
            print("No user with email {email}!".format(email = email))

    def add_user(self, name, email, books = None):
        if email.find("@") != -1 and(email[-4:].find(".com") != -1) or (email[-4:].find(".edu") != -1) or (email[-4:].find(".org") != -1):
            if email in self.users:
                print("This email already exists for a user!")
            else:
                self.users[email] = User(name, email)
                if books != None:
                    for book in books:
                        self.add_book_to_user(book, email)
        else:
            print("Please, introduce a valid email adress")
        
    def print_catalog(self):
        for key in self.books:
            print(key)

    def print_users(self):
        for value in self.users.values():
            print(value)

    def most_read_book(self):
        selected_book = None
        max_num_read = 0
        for key, value in self.books.items():
            if value > max_num_read:
                max_num_read = value
                selected_book = key
        return selected_book

    def highest_rated_book(self):
        selected_book = None
        max_average_rating = 0
        for book in self.books.keys():
            if book.get_average_rating() > max_average_rating:
                max_average_rating = book.get_average_rating()
                selected_book = book
        return selected_book

    def most_positive_user(self):
        selected_user = None
        max_average_rating = 0
        for key, value in self.users.items():
            if value.get_average_rating() > max_average_rating:
                max_average_rating = value.get_average_rating()
                selected_user = key
        return selected_user

    def __eq__(self, other_tome_rater):
        if self.users == other_tome_rater.users and self.books == other_tome_rater.books:
            return True
        else:
            return False

    def __repr__(self):
        return "{users}, {books}".format(users = self.users, books = self.books)
            
            
            
            
        
        


        
