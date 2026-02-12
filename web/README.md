# 📱 Web Interface for Interview Prep System

A mobile-friendly web application to access your interview prep system from anywhere - perfect for studying on your phone!

## 🌟 Features

- **📱 Mobile-First Design** - Optimized for phone screens with responsive layout
- **🎴 Interactive Flashcards** - Study with spaced repetition on the go
- **📊 Progress Dashboard** - Track your progress with visual charts
- **📝 Exercise Browser** - Browse SQL and Python exercises
- **📚 Resources & Cheat Sheets** - Access all learning materials
- **🎨 Beautiful UI** - Clean, modern interface with Tailwind CSS

## 🚀 Quick Start

### Option 1: Local Network (Access from Phone)

1. **Start the server on your computer:**
   ```bash
   cd web
   python app.py
   ```

2. **Find your computer's IP address:**
   ```bash
   # On Linux/Mac
   ifconfig | grep "inet " | grep -v 127.0.0.1

   # On Windows
   ipconfig | findstr IPv4
   ```

3. **Access from your phone:**
   - Make sure your phone is on the same WiFi network
   - Open browser and go to: `http://YOUR_IP:5000`
   - Example: `http://192.168.1.100:5000`

### Option 2: Deploy to Cloud (Free)

#### Deploy to Render (Recommended)

1. **Create `render.yaml` in project root** (already provided)

2. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add web interface"
   git push
   ```

3. **Deploy on Render:**
   - Go to [render.com](https://render.com)
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`
   - Click "Apply" and your app will be live in minutes!
   - You'll get a URL like: `https://interview-prep-XXXX.onrender.com`

#### Deploy to Railway

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy:**
   ```bash
   cd interview-prep-system
   railway init
   railway up
   ```

3. **Get your URL:**
   ```bash
   railway domain
   ```

## 📖 How to Use

### Study Flashcards on Your Phone

1. Open the web app
2. Tap "🎴 Flashcards"
3. Select a category (or "All Categories")
4. Review cards and rate yourself (😞 Forgot → 😄 Perfect!)
5. System automatically schedules next review

### Check Your Progress

1. Tap "📊 Progress Dashboard"
2. See visual progress bars for:
   - SQL exercises
   - Python exercises
   - Flashcard reviews
   - Time invested

### Browse Exercises

1. Tap "📝 SQL Exercises" or "🐍 Python Exercises"
2. Browse by difficulty or category
3. Read problem statements
4. View schemas and sample data
5. Solve on your computer using the CLI

### Access Resources

1. Tap "📚 Resources"
2. Browse 100+ curated learning links
3. Access SQL and Python cheat sheets
4. All formatted for easy mobile reading

## 🎯 Pages Available

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Dashboard with quick stats |
| Flashcards | `/flashcards` | Interactive study session |
| SQL Exercises | `/exercises/sql` | Browse SQL problems |
| Python Exercises | `/exercises/python` | Browse Python challenges |
| Progress | `/progress` | Detailed analytics |
| Resources | `/resources` | Learning links |
| SQL Cheat Sheet | `/cheatsheet/sql` | Quick SQL reference |
| Python Cheat Sheet | `/cheatsheet/python` | Quick Python reference |

## 🛠️ Technical Stack

- **Backend**: Flask (Python web framework)
- **Frontend**:
  - Tailwind CSS (responsive design)
  - Alpine.js (lightweight interactivity)
  - Marked.js (Markdown rendering)
  - Highlight.js (code syntax highlighting)
- **Data**: JSON files (same as CLI)
- **Deployment**: Render, Railway, or local network

## 📂 Project Structure

```
web/
├── app.py                 # Flask application
├── templates/             # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Home page
│   ├── flashcards.html   # Interactive flashcard study
│   ├── progress.html     # Progress dashboard
│   ├── sql_exercises.html
│   ├── python_exercises.html
│   └── ...
├── static/               # Static assets (CSS, JS)
│   ├── css/
│   └── js/
└── README.md             # This file
```

## 🔧 Development

### Run in Debug Mode

```bash
cd web
export FLASK_DEBUG=1  # On Windows: set FLASK_DEBUG=1
python app.py
```

### Customize Styles

The app uses Tailwind CSS via CDN. To customize:

1. Edit templates in `web/templates/`
2. Modify Tailwind classes directly in HTML
3. Changes are instant (reload browser)

### Add New Pages

1. Create new template in `templates/`
2. Add route in `app.py`:
   ```python
   @app.route('/my-page')
   def my_page():
       return render_template('my_page.html')
   ```

## 🌐 Deployment Options Comparison

| Option | Pros | Cons | Cost |
|--------|------|------|------|
| **Local Network** | Free, instant, full control | Only on same WiFi, computer must be on | Free |
| **Render** | Free tier, auto-deploy from Git, HTTPS | Spins down after inactivity (15min to wake) | Free |
| **Railway** | Fast, generous free tier, easy CLI | May require payment after trial | Free/$5/mo |
| **Vercel** | Fast CDN, great for static | Harder for Python apps | Free |

**Recommendation**: Start with **Local Network** for immediate use, then deploy to **Render** for 24/7 access.

## 💡 Tips for Mobile Studying

### Best Practices

1. **Use Progressive Web App (PWA)**:
   - In Chrome mobile: Menu → "Add to Home Screen"
   - App will open full-screen like a native app

2. **Enable Dark Mode**:
   - Use your browser's dark mode for night studying
   - Saves battery on OLED screens

3. **Offline Support** (future enhancement):
   - Currently requires internet connection
   - Cache common pages in browser for faster load

4. **Study Sessions**:
   - 10-15 minute flashcard sessions
   - Perfect for commute, breaks, waiting time
   - Review exercises on mobile, solve on computer

### Keyboard Shortcuts (Desktop)

- Number keys `0-5`: Rate flashcard
- `Space`: Show answer / Next card
- `Esc`: Back to menu

## 🔒 Security Notes

- **Local Network**: Safe for home WiFi, don't expose to public internet
- **Cloud Deployment**: Use environment variables for any sensitive data
- **No Authentication**: Add login if deploying publicly with sensitive data

## 🐛 Troubleshooting

### Can't Access from Phone

1. Verify computer and phone on same WiFi
2. Check firewall isn't blocking port 5000
3. Try `0.0.0.0:5000` in server, not `127.0.0.1`

### Flashcards Not Saving

1. Check file permissions on `concepts/flashcards/cards.json`
2. Verify server has write access to directory

### Styles Not Loading

1. Check internet connection (Tailwind CDN)
2. Clear browser cache
3. Check browser console for errors

## 📱 Progressive Web App (PWA)

To install as an app on your phone:

### iOS (iPhone/iPad)

1. Open in Safari
2. Tap Share button
3. Tap "Add to Home Screen"
4. Name it "Interview Prep"
5. Tap "Add"

### Android

1. Open in Chrome
2. Tap menu (3 dots)
3. Tap "Add to Home screen"
4. Name it "Interview Prep"
5. Tap "Add"

## 🚀 What's Next?

Future enhancements:

- [ ] Offline mode with service workers
- [ ] Push notifications for study reminders
- [ ] Voice input for flashcard answers
- [ ] Timer for practice sessions
- [ ] Compete with friends (leaderboard)
- [ ] Dark mode toggle
- [ ] Export progress as PDF

## 📞 Support

If you encounter issues:

1. Check this README
2. Review the main project [README](../README.md)
3. Check server logs in terminal
4. Open an issue on GitHub

---

**Happy studying on the go! 📱🚀**

*Built with ❤️ for flexible, anywhere learning*
