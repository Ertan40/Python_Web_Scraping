import requests
"""
Get book and author data from https://openlibrary.org

ISBN: https://en.wikipedia.org/wiki/International_Standard_Book_Number or

You can search at https://openlibrary.org and after pulled up the book, then check at details for an ISBN. 
"""


def fetch_openlibrary_data(isbn):
    """
    Fetch book data from Open Library API.
    Given an 'books/OL5087087M', return book data from Open Library as a Python dict.
    Given an '/authors/OL4356578A', return authors data as a Python dict.
    """
    url = f'https://openlibrary.org/books/{isbn}.json'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f"Failed to fetch isbn data due to an error: {str(error)} ")
        return None


def get_book_authors(author_isbn):
    authors = ''
    for a in author_isbn:
        authors += a.get('key')
    author = authors.split('/')[2]
    # author = author_isbn[0]['key'].split('/')[2]  # or for one liners :)
    # Fetch authors data
    author_url = f'https://openlibrary.org/authors/{author}.json'
    try:
        response = requests.get(author_url, timeout=10)
        response.raise_for_status()
        author_data = response.json()
        return author_data.get('name')
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch autor data due to an error: {e}")
        return None


def display_book_details(book_info):
    if not book_info:
        print("No book data available")
        return

    title = book_info.get('title')
    authors = book_info.get('authors')
    publish_date = book_info.get('publish_date')
    publishers = book_info.get('publishers')
    subject_place = book_info.get('subject_place')
    subjects = book_info.get('subjects')
    pagination = book_info.get('pagination')

    print(f"Book Details:")
    print(f"Book title: {title}")
    # [{'key': '/authors/OL4356578A'}]
    if authors:
        author = get_book_authors(authors)
        print(f"Book author: {author if author else 'Unknown'}")
    else:
        print("Author not found")

    print(f"Publish date: {publish_date}" if publish_date else "Publish date: Not available")
    print(f"Publishers: {', '.join(publishers)}" if publishers else "Publishers: Not available")
    print(f"Subject place: {', '.join(subject_place)}" if subject_place else "Subject place: Not available")
    print(f"Subjects: {', '.join(subjects)}" if subjects else "Subjects: Not available")
    print(f"Number of pages: {pagination}")


def main():
    while True:
        isbn_input = input(f"\nPlease enter the ISBN code to search or 'quit' to stop: ").strip()
        if isbn_input.lower() in ("", "q", "quit", "exit", "stop"):
            print("\nThanks for using my app and have a lovely day!")
            break
        print(f"\nSearching Open Library for ISBN: {isbn_input}...\n")
        # print(fetch_openlibrary_data(isbn_input))
        book_data = fetch_openlibrary_data(isbn_input)
        display_book_details(book_data)


# test: OL5087087M  or OL47677922M  or OL799592M
if __name__ == "__main__":
    main()


# Output:
# Please enter the ISBN code to search or 'quit' to stop: OL47677922M
#
# Searching Open Library for ISBN: OL47677922M...
#
# Book Details:
# Book title: Great expectations
# Book author: Charles Dickens
# Publish date: 1894
# Publishers: Houghton, Mifflin and Co.
# Subject place: Not available
# Subjects: Not available
# Number of pages: xx, 482 pages
#
# Please enter the ISBN code to search or 'quit' to stop: q
#
# Thanks for using my app and have a lovely day!