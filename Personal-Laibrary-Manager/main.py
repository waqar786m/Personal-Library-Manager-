import json  # JSON library import ki gai hai taake data ko store aur retrieve kiya ja sake
import streamlit as st  # Streamlit ko import kiya gaya hai GUI banane ke liye

class BookCollection:
    """Ek class jo book collection ko manage karne ke liye hai, taake users apni kitaabein store aur organize kar sakein."""

    def __init__(self):
        """Book collection initialize karta hai ek empty list ke sath aur file storage set karta hai."""
        self.book_list = []  # Book collection ko store karne ke liye empty list banai gai hai
        self.storage_file = "books_data.json"  # Data store karne ke liye JSON file ka naam set kiya
        self.read_from_file()  # Pehle se existing data ko load karne ke liye function call kiya

    def read_from_file(self):
        """JSON file se saved books ko memory mein load karta hai. Agar file na mile ya corrupt ho, to empty collection start karta hai."""
        try:
            with open(self.storage_file, "r", encoding="utf-8") as file:  # File ko read mode mein open kiya
                self.book_list = json.load(file)  # File se data load karke list mein store kiya
        except (FileNotFoundError, json.JSONDecodeError):  # Agar file na mile ya JSON corrupt ho to
            self.book_list = []  # Empty list set kar di

    def save_to_file(self):
        """Current book collection ko JSON file mein store karta hai permanent storage ke liye."""
        with open(self.storage_file, "w", encoding="utf-8") as file:  # File ko write mode mein open kiya
            json.dump(self.book_list, file, indent=4, ensure_ascii=False)  # JSON format mein data save kiya

    def create_new_book(self, book_title, book_author, publication_years, book_genre, is_book_read):
        """Naya book collection mein add karta hai."""
        new_book = {  # Naye book ke details ek dictionary mein store kiye gaye
            "title": book_title,
            "author": book_author,
            "years": publication_years,
            "genre": book_genre,
            "read": is_book_read
        }
        self.book_list.append(new_book)  # Book ko list mein add kiya
        self.save_to_file()  # List ko JSON file mein save kiya

    def delete_book(self, book_title):
        """Book collection se ek kitaab delete karta hai title ke zariye."""
        self.book_list = [book for book in self.book_list if book["title"].lower() != book_title.lower()]  # List comprehension se book remove kiya
        self.save_to_file()  # Updated list ko file mein save kiya

    def find_book(self, search_text):
        """Title ya author name se books ko search karta hai."""
        return [
            book for book in self.book_list
            if search_text.lower() in book["title"].lower() or search_text.lower() in book["author"].lower()
        ]  # Agar search text kisi book ke title ya author mein ho to return karega

    def get_all_books(self):
        """Puri book collection return karta hai."""
        return self.book_list

    def get_reading_progress(self):
        """Reading progress ke statistics calculate karke return karta hai."""
        total_books = len(self.book_list)  # Total books ka count nikalta hai
        completed_books = sum(1 for book in self.book_list if book["read"])  # Read books ka count karta hai
        completion_rate = (completed_books / total_books * 100) if total_books > 0 else 0  # Percentage calculate karta hai
        return total_books, completion_rate

book_manager = BookCollection()  # BookCollection class ka ek instance banaya

st.title("📚 Book Collection Manager")  # Streamlit ka title set kiya
menu = st.sidebar.selectbox("Menu", ["Add Book", "Remove Book", "Search Book", "View All Books", "Reading Progress"])  # Sidebar menu set kiya

if menu == "Add Book":
    title = st.text_input("Book Title")  # Book title ke liye input field
    author = st.text_input("Author")  # Author ke liye input field
    years = st.text_input("Publication years")  # Publication year input field
    genre = st.text_input("Genre")  # Genre input field
    read = st.checkbox("Have you read this book?")  # Checkbox for book read status
    if st.button("Add Book"):  # Jab button press ho to book add ho jaye
        book_manager.create_new_book(title, author, years, genre, read)  # Book add karne ka function call kiya
        st.success("Book added successfully!")  # Success message display kiya

elif menu == "Remove Book":
    title = st.text_input("Enter the title of the book to remove")  # Remove book ke liye input field
    if st.button("Remove Book"):  # Jab button press ho
        book_manager.delete_book(title)  # Book delete function call kiya
        st.success("Book removed successfully!")  # Success message show kiya

elif menu == "Search Book":
    search_text = st.text_input("Enter title or author name")  # Search input field
    if st.button("Search"):  # Jab search button click ho
        results = book_manager.find_book(search_text)  # Search function call kiya
        if results:
            for book in results:
                st.write(f"**{book['title']}** by {book['author']} ({book['years']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")  # Search results display kiya
        else:
            st.warning("No matching books found.")  # Agar koi book na mile to warning show kare

elif menu == "View All Books":
    books = book_manager.get_all_books()  # Puri book collection fetch ki
    if books:
        for book in books:
            st.write(f"**{book['title']}** by {book['author']} ({book['years']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")  # Books display ki
    else:
        st.warning("Your book collection is empty.")  # Agar koi book na ho to message show kare

elif menu == "Reading Progress":
    total_books, progress = book_manager.get_reading_progress()  # Reading progress fetch kiya
    st.write(f"Total books in collection: {total_books}")  # Total books display kiya
    st.write(f"Reading Progress: {progress:.2f}%")  # Reading progress percentage show kiya
