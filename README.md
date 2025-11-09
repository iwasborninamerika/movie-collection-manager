# 🎬 Movie Collection Manager

A Python command-line application for managing your personal movie collection with persistent storage, search functionality, and detailed statistics.

## ✨ Features

- ➕ **Add movies** with title, genre, year, rating, director, and review
- 🎥 **View collection** with formatted display
- 📈 **Comprehensive statistics** - average rating, genre distribution, rating distribution
- 🔍 **Advanced search** by title, genre, director, year range, or minimum rating
- ✏️ **Edit movies** - modify existing entries without deletion
- 📊 **Sort collection** by title, year, rating, or genre (ascending/descending)
- 🗑️ **Delete movies** from your collection
- 💾 **Automatic persistence** with JSON storage
- 🔄 **Automatic backups** before each save
- ✅ **Input validation** and comprehensive error handling

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher

### Installation

1. Clone the repository:
```bash
git clone https://github.com/iwasborninamerika/movie-collection-manager.git
cd movie-collection-manager
```

2. Run the application:
```bash
python3 movie-collection-manager.py
```

## 💻 Usage

Run the program and follow the interactive menu:
```
📋 MAIN MENU
1. ➕ Add new movie
2. 🎥 View collection
3. 📈 Statistics
4. 🔍 Search movies
5. ✏️ Edit movie
6. 📊 Sort collection
7. 🗑️ Delete movie
8. 🚪 Exit
```

### Example: Adding a Movie
```
🎬 ADD NEW MOVIE
Movie title: The Shawshank Redemption
Genre: Drama
Release year: 1994
Your rating (1-10): 10
Director: Frank Darabont
Your review: An absolute masterpiece about hope and friendship.

✅ Movie 'The Shawshank Redemption' added successfully!
```

## 🛠️ Technical Details

- **Language**: Python 3
- **Data Storage**: JSON file format with automatic backups
- **Architecture**: Object-oriented design with single class structure
- **Design Patterns**: 
  - Input validation with generic validator method
  - Constants for magic numbers
  - Type hints for improved readability
- **Error Handling**: Comprehensive try-catch blocks for file I/O and user input

## 📝 Code Highlights

- **Type hints** throughout for better code documentation
- **Constants** for all magic numbers and repeated strings
- **Modular design** with single-responsibility methods
- **Data validation** for loaded JSON files
- **Automatic backup system** (`.json.bak` files)
- **pathlib** for modern path handling
- **Generic input validator** to reduce code duplication

## 🔮 Future Enhancements

- [ ] Export collection to CSV/Excel
- [ ] Import movies from IMDB/TMDB API
- [ ] Rating visualization with charts
- [ ] Multiple collection support
- [ ] Web interface using Flask
- [ ] Movie poster downloads
- [ ] Watch date tracking
- [ ] Favorite movies marking

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built as a learning project to practice Python OOP and file handling
- Inspired by the need to organize my personal movie collection