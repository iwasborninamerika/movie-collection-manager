"""
Movie Collection Manager
A comprehensive Python application for managing personal movie collections.
Features include persistent storage, search, statistics, and more.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Callable, Any


class MovieCollection:
    """
    A class to manage a personal movie collection with various features.
    
    Attributes:
        filename (Path): JSON file for data storage
        movies (List[Dict]): List of movie dictionaries
    """
    
    MIN_RATING = 1
    MAX_RATING = 10
    FIRST_FILM_YEAR = 1888
    SEPARATOR = "=" * 50
    SEPARATOR_SHORT = "=" * 30
    REQUIRED_FIELDS = ['title', 'genre', 'year', 'rating', 'director', 'review', 'added_date']
    
    def __init__(self, filename: str = "movie_collection.json") -> None:
        """
        Initialize MovieCollection manager.
        
        Args:
            filename (str): Path to storage file. Defaults to "movie_collection.json"
        """
        self.filename = Path(filename)
        self.movies = self.load_collection()
    
    def load_collection(self) -> List[Dict]:
        """
        Load movie collection from JSON file with validation.
        
        Returns:
            List[Dict]: List of movies or empty list if file doesn't exist
        """
        if not self.filename.exists():
            return []
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                movies = json.load(f)
                
                valid_movies = [m for m in movies if self._validate_movie_data(m)]
                if len(valid_movies) < len(movies):
                    print(f"⚠️  Warning: {len(movies) - len(valid_movies)} invalid movie(s) skipped")
                return valid_movies
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️  Warning: Could not load collection: {e}")
            print("Starting with empty collection.")
            return []
    
    def _validate_movie_data(self, movie: Dict) -> bool:
        """
        Validate movie has all required fields.
        
        Args:
            movie (Dict): Movie data to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        return all(field in movie for field in self.REQUIRED_FIELDS)
    
    def save_collection(self) -> bool:
        """
        Save movie collection to JSON file with backup.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if self.filename.exists():
                backup_path = self.filename.with_suffix('.json.bak')
                self.filename.replace(backup_path)
            
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.movies, f, ensure_ascii=False, indent=2)
            return True
        except IOError as e:
            print(f"❌ Error saving collection: {e}")
            return False
    
    def _get_validated_input(self, prompt: str, validator: Callable[[str], Any], 
                            error_msg: str, allow_back: bool = False) -> Optional[Any]:
        """
        Generic input validation helper.
        
        Args:
            prompt (str): Input prompt to display
            validator (Callable): Function to validate/convert input
            error_msg (str): Error message to display on invalid input
            allow_back (bool): Allow 'back' to cancel operation
            
        Returns:
            Optional[Any]: Validated value or None if cancelled
        """
        while True:
            value = input(prompt).strip()
            
            if allow_back and value.lower() == 'back':
                return None
            
            try:
                result = validator(value)
                if result is not None:
                    return result
                print(f"❌ {error_msg}")
            except (ValueError, TypeError):
                print(f"❌ {error_msg}")
    
    def add_movie(self) -> None:
        """Add a new movie to the collection with validation."""
        print(f"\n{self.SEPARATOR}")
        print("🎬 ADD NEW MOVIE")
        print(self.SEPARATOR)
        
        title = self._get_validated_title()
        if title is None:
            return
        
        genre = input("Genre: ").strip() or "Unknown"
        year = self._get_validated_year()
        rating = self._get_validated_rating()
        director = input("Director (optional): ").strip() or "Unknown"
        review = input("Your review (optional): ").strip()
        
        movie = {
            'title': title,
            'genre': genre,
            'year': year,
            'rating': rating,
            'director': director,
            'review': review,
            'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.movies.append(movie)
        if self.save_collection():
            print(f"✅ Movie '{title}' added successfully!")
        else:
            print("❌ Failed to save movie to collection")
    
    def _get_validated_title(self) -> Optional[str]:
        """Get and validate movie title."""
        def validate_title(title: str) -> Optional[str]:
            if not title:
                return None
            if any(movie['title'].lower() == title.lower() for movie in self.movies):
                print("❌ This movie is already in your collection!")
                return None
            return title
        
        return self._get_validated_input(
            "\n🎭 Movie title (or 'back' to return): ",
            validate_title,
            "Please enter a valid title",
            allow_back=True
        )
    
    def _get_validated_year(self) -> int:
        """Get and validate release year."""
        current_year = datetime.now().year
        
        def validate_year(year_str: str) -> Optional[int]:
            if not year_str.isdigit():
                return None
            year = int(year_str)
            if self.FIRST_FILM_YEAR <= year <= current_year:
                return year
            return None
        
        return self._get_validated_input(
            "📅 Release year: ",
            validate_year,
            f"Please enter a valid year ({self.FIRST_FILM_YEAR}-{current_year})"
        )
    
    def _get_validated_rating(self) -> int:
        """Get and validate rating."""
        def validate_rating(rating_str: str) -> Optional[int]:
            rating = int(rating_str)
            if self.MIN_RATING <= rating <= self.MAX_RATING:
                return rating
            return None
        
        return self._get_validated_input(
            f"⭐ Your rating ({self.MIN_RATING}-{self.MAX_RATING}): ",
            validate_rating,
            f"Please enter a number between {self.MIN_RATING}-{self.MAX_RATING}"
        )
    
    def show_collection(self, movies_list: Optional[List[Dict]] = None) -> None:
        """
        Display movies in a formatted way.
        
        Args:
            movies_list (Optional[List[Dict]]): Specific list of movies to display. 
                                                Defaults to all movies.
        """
        movies_to_show = movies_list if movies_list is not None else self.movies
        
        if not movies_to_show:
            print("\n📭 Your collection is empty. Add some movies!")
            return
        
        print(f"\n{self.SEPARATOR}")
        print("🎥 YOUR MOVIE COLLECTION")
        print(self.SEPARATOR)
        
        for i, movie in enumerate(movies_to_show, 1):
            print(f"\n{i}. {movie['title']} ({movie['year']})")
            print(f"   🎭 Genre: {movie['genre']} | ⭐ Rating: {movie['rating']}/{self.MAX_RATING}")
            print(f"   👨‍💼 Director: {movie['director']}")
            if movie['review']:
                print(f"   💬 Review: {movie['review']}")
            print(f"   📅 Added: {movie['added_date']}")
    
    def show_statistics(self) -> None:
        """Display comprehensive collection statistics."""
        if not self.movies:
            print("\n📊 No statistics available - collection is empty")
            return
        
        total_movies = len(self.movies)
        avg_rating = sum(movie['rating'] for movie in self.movies) / total_movies
        
        genres = [movie['genre'] for movie in self.movies]
        most_common_genre = max(set(genres), key=genres.count)
        
        years = [movie['year'] for movie in self.movies]
        oldest = min(years)
        newest = max(years)
        
        best_movie = max(self.movies, key=lambda x: x['rating'])
        worst_movie = min(self.movies, key=lambda x: x['rating'])
        
        print(f"\n{self.SEPARATOR}")
        print("📈 COLLECTION STATISTICS")
        print(self.SEPARATOR)
        print(f"🎬 Total movies: {total_movies}")
        print(f"⭐ Average rating: {avg_rating:.1f}/{self.MAX_RATING}")
        print(f"🎭 Most common genre: {most_common_genre}")
        print(f"📅 Year range: {oldest} - {newest}")
        print(f"🏆 Best rated: {best_movie['title']} ({best_movie['rating']}/{self.MAX_RATING})")
        print(f"💩 Worst rated: {worst_movie['title']} ({worst_movie['rating']}/{self.MAX_RATING})")
        
        print("\n📊 Rating Distribution:")
        for i in range(self.MIN_RATING, self.MAX_RATING + 1):
            count = sum(1 for movie in self.movies if movie['rating'] == i)
            if count > 0:
                print(f"   {i}/{self.MAX_RATING}: {count} movie(s)")
    
    def sort_movies(self) -> None:
        """Sort movies by various criteria."""
        if not self.movies:
            print("\n📭 No movies to sort")
            return
        
        print("\n📊 Sort by:")
        print("1. Title (A-Z)")
        print("2. Title (Z-A)")
        print("3. Year (Oldest first)")
        print("4. Year (Newest first)")
        print("5. Rating (Lowest first)")
        print("6. Rating (Highest first)")
        print("7. Genre (A-Z)")
        
        choice = input("\nChoose sort option (1-7): ").strip()
        
        sort_options = {
            '1': ('title', False),
            '2': ('title', True),
            '3': ('year', False),
            '4': ('year', True),
            '5': ('rating', False),
            '6': ('rating', True),
            '7': ('genre', False)
        }
        
        if choice in sort_options:
            sort_key, reverse = sort_options[choice]
            self.movies.sort(key=lambda x: x[sort_key], reverse=reverse)
            self.save_collection()
            print(f"✅ Collection sorted by {sort_key}")
            self.show_collection()
        else:
            print("❌ Invalid choice")
    
    def search_movies(self) -> None:
        """Search movies by various criteria."""
        if not self.movies:
            print("\n🔍 No movies to search")
            return
        
        print("\n🔍 Search by:")
        print("1. Title")
        print("2. Genre") 
        print("3. Director")
        print("4. Year range")
        print("5. Minimum rating")
        
        choice = input("\nChoose search type (1-5): ").strip()
        
        search_methods = {
            '1': self._search_by_title,
            '2': self._search_by_genre,
            '3': self._search_by_director,
            '4': self._search_by_year_range,
            '5': self._search_by_min_rating
        }
        
        if choice in search_methods:
            search_methods[choice]()
        else:
            print("❌ Invalid choice")
    
    def _search_by_title(self) -> None:
        """Search movies by title."""
        search_term = input("Enter title to search: ").lower().strip()
        results = [m for m in self.movies if search_term in m['title'].lower()]
        self._display_search_results(results, f"Title containing '{search_term}'")
    
    def _search_by_genre(self) -> None:
        """Search movies by genre."""
        search_term = input("Enter genre to search: ").lower().strip()
        results = [m for m in self.movies if search_term in m['genre'].lower()]
        self._display_search_results(results, f"Genre containing '{search_term}'")
    
    def _search_by_director(self) -> None:
        """Search movies by director."""
        search_term = input("Enter director to search: ").lower().strip()
        results = [m for m in self.movies if search_term in m['director'].lower()]
        self._display_search_results(results, f"Director containing '{search_term}'")
    
    def _search_by_year_range(self) -> None:
        """Search movies by year range."""
        try:
            start_year = int(input("Start year: "))
            end_year = int(input("End year: "))
            results = [m for m in self.movies if start_year <= m['year'] <= end_year]
            self._display_search_results(results, f"Years {start_year}-{end_year}")
        except ValueError:
            print("❌ Please enter valid years")
    
    def _search_by_min_rating(self) -> None:
        """Search movies by minimum rating."""
        try:
            min_rating = int(input(f"Minimum rating ({self.MIN_RATING}-{self.MAX_RATING}): "))
            if self.MIN_RATING <= min_rating <= self.MAX_RATING:
                results = [m for m in self.movies if m['rating'] >= min_rating]
                self._display_search_results(results, f"Rating ≥ {min_rating}")
            else:
                print(f"❌ Rating must be between {self.MIN_RATING}-{self.MAX_RATING}")
        except ValueError:
            print("❌ Please enter a valid number")
    
    def _display_search_results(self, results: List[Dict], search_description: str) -> None:
        """Display search results."""
        if not results:
            print(f"\n🔍 No movies found for {search_description}")
            return
        
        print(f"\n🎬 Found {len(results)} movie(s) for {search_description}:")
        self.show_collection(results)
    
    def edit_movie(self) -> None:
        """Edit an existing movie's details."""
        if not self.movies:
            print("\n📭 No movies to edit")
            return
        
        self.show_collection()
        
        try:
            choice = int(input("\nEnter movie number to edit (0 to cancel): "))
            if choice == 0:
                return
            if 1 <= choice <= len(self.movies):
                movie = self.movies[choice - 1]
                print(f"\n✏️  Editing: {movie['title']}")
                print("(Press Enter to keep current value)")
                
                new_title = input(f"Title [{movie['title']}]: ").strip()
                if new_title:
                    movie['title'] = new_title
                
                new_genre = input(f"Genre [{movie['genre']}]: ").strip()
                if new_genre:
                    movie['genre'] = new_genre
                
                new_year_str = input(f"Year [{movie['year']}]: ").strip()
                if new_year_str and new_year_str.isdigit():
                    movie['year'] = int(new_year_str)
                
                new_rating_str = input(f"Rating [{movie['rating']}]: ").strip()
                if new_rating_str and new_rating_str.isdigit():
                    new_rating = int(new_rating_str)
                    if self.MIN_RATING <= new_rating <= self.MAX_RATING:
                        movie['rating'] = new_rating
                
                new_director = input(f"Director [{movie['director']}]: ").strip()
                if new_director:
                    movie['director'] = new_director
                
                new_review = input(f"Review [{movie['review']}]: ").strip()
                if new_review:
                    movie['review'] = new_review
                
                self.save_collection()
                print(f"✅ Movie '{movie['title']}' updated successfully!")
            else:
                print("❌ Invalid movie number")
        except ValueError:
            print("❌ Please enter a valid number")
    
    def delete_movie(self) -> None:
        """Delete a movie from collection."""
        if not self.movies:
            print("\n📭 No movies to delete")
            return
        
        self.show_collection()
        
        try:
            choice = int(input("\nEnter movie number to delete (0 to cancel): "))
            if choice == 0:
                return
            if 1 <= choice <= len(self.movies):
                deleted_movie = self.movies.pop(choice - 1)
                self.save_collection()
                print(f"🗑️  Deleted: {deleted_movie['title']}")
            else:
                print("❌ Invalid movie number")
        except ValueError:
            print("❌ Please enter a valid number")
    
    def run(self) -> None:
        """Main application loop."""
        print(f"\n{self.SEPARATOR}")
        print("🎬 MOVIE COLLECTION MANAGER")
        print(self.SEPARATOR)
        print(f"📊 Loaded {len(self.movies)} movies from collection")
        
        while True:
            print(f"\n{self.SEPARATOR_SHORT}")
            print("📋 MAIN MENU")
            print(self.SEPARATOR_SHORT)
            print("1. ➕ Add new movie")
            print("2. 🎥 View collection") 
            print("3. 📈 Statistics")
            print("4. 🔍 Search movies")
            print("5. ✏️  Edit movie")
            print("6. 📊 Sort collection")
            print("7. 🗑️  Delete movie")
            print("8. 🚪 Exit")
            
            choice = input("\nChoose option (1-8): ").strip()
            
            if choice == '1':
                self.add_movie()
            elif choice == '2':
                self.show_collection()
            elif choice == '3':
                self.show_statistics()
            elif choice == '4':
                self.search_movies()
            elif choice == '5':
                self.edit_movie()
            elif choice == '6':
                self.sort_movies()
            elif choice == '7':
                self.delete_movie()
            elif choice == '8':
                print("\n🎉 Thank you for using Movie Collection Manager!")
                print("👋 Goodbye!")
                break
            else:
                print("❌ Please choose a valid option (1-8)")
    
    # Testing/utility methods
    def clear_collection(self) -> None:
        """Clear all movies from collection (for testing)."""
        self.movies.clear()
        self.save_collection()
    
    def get_movie_count(self) -> int:
        """Get total number of movies (for testing)."""
        return len(self.movies)
    
    def add_movie_directly(self, movie_data: Dict) -> None:
        """
        Add movie directly without user input (for testing).
        
        Args:
            movie_data (Dict): Movie data dictionary
        """
        if self._validate_movie_data(movie_data):
            self.movies.append(movie_data)
            self.save_collection()
        else:
            print("❌ Invalid movie data")
    
    def find_movie_by_title(self, title: str) -> Optional[Dict]:
        """
        Find movie by exact title match (for testing).
        
        Args:
            title (str): Movie title to find
            
        Returns:
            Optional[Dict]: Movie data or None if not found
        """
        for movie in self.movies:
            if movie['title'].lower() == title.lower():
                return movie
        return None


def main():
    """Main entry point for the application."""
    try:
        app = MovieCollection()
        app.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Program interrupted by user")
        print("👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please report this issue if it persists.")


if __name__ == "__main__":
    main()
