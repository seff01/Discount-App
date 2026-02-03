# How to Download Discount-App

This guide provides step-by-step instructions for downloading the Discount-App to your computer.

## Prerequisites

Before downloading, make sure you have:
- **Python 3.7 or higher** installed on your computer
  - Check by running: `python --version` or `python3 --version`
  - Download Python from: https://www.python.org/downloads/

## Method 1: Download ZIP File (Easiest)

**Best for:** Beginners or those without Git installed

### Step-by-Step Instructions:

1. **Visit the repository**
   - Go to: https://github.com/seff01/Discount-App

2. **Download the ZIP file**
   - Look for the green **"Code"** button (near the top right of the page)
   - Click the **"Code"** button
   - In the dropdown menu, click **"Download ZIP"**
   - Your browser will download a file named `Discount-App-main.zip`

3. **Extract the ZIP file**
   - **Windows:**
     - Right-click the downloaded ZIP file
     - Select "Extract All..."
     - Choose a destination folder (e.g., `C:\Users\YourName\Documents`)
     - Click "Extract"
   
   - **Mac:**
     - Double-click the ZIP file
     - It will automatically extract to the same folder
   
   - **Linux:**
     - Right-click and select "Extract Here"
     - Or use terminal: `unzip Discount-App-main.zip`

4. **Open the folder**
   - Navigate to the extracted folder
   - You should see files like `discount_app.py`, `README.md`, etc.

5. **You're ready!**
   - Open a terminal/command prompt in this folder
   - Run: `python discount_app.py`

## Method 2: Clone with Git

**Best for:** Developers or those familiar with Git

### Step-by-Step Instructions:

1. **Install Git** (if not already installed)
   - Download from: https://git-scm.com/downloads
   - Verify installation: `git --version`

2. **Open Terminal/Command Prompt**
   - **Windows:** Press `Win + R`, type `cmd`, press Enter
   - **Mac:** Press `Cmd + Space`, type "Terminal", press Enter
   - **Linux:** Press `Ctrl + Alt + T`

3. **Navigate to your desired folder**
   ```bash
   cd path/to/your/projects
   # Example: cd C:\Users\YourName\Documents\Projects
   # Example: cd ~/Documents/Projects
   ```

4. **Clone the repository**
   ```bash
   git clone https://github.com/seff01/Discount-App.git
   ```

5. **Enter the folder**
   ```bash
   cd Discount-App
   ```

6. **You're ready!**
   - Run: `python discount_app.py`

## Method 3: GitHub Desktop

**Best for:** Those who prefer a graphical interface

### Step-by-Step Instructions:

1. **Install GitHub Desktop**
   - Download from: https://desktop.github.com/
   - Install and open the application

2. **Sign in to GitHub** (optional but recommended)
   - Click "Sign in to GitHub.com"
   - Follow the authentication process

3. **Clone the repository**
   - Click **File** → **Clone Repository**
   - Select the **URL** tab
   - Enter: `https://github.com/seff01/Discount-App`
   - Choose a local path (where to save the files)
   - Click **Clone**

4. **Open the folder**
   - In GitHub Desktop, click **Repository** → **Show in Explorer/Finder**

5. **You're ready!**
   - Open a terminal in this folder
   - Run: `python discount_app.py`

## Method 4: Download Individual Files

**Best for:** If you only need specific files

### Step-by-Step Instructions:

1. **Navigate to the repository**
   - Go to: https://github.com/seff01/Discount-App

2. **Browse to the file you want**
   - Click on the file name (e.g., `discount_app.py`)

3. **Download the file**
   - Click the **"Raw"** button (top right of the file content)
   - Right-click anywhere on the page
   - Select **"Save Page As..."** or **"Save As..."**
   - Choose your destination folder
   - Make sure to keep the correct file extension (e.g., `.py`, `.txt`, `.md`)

4. **Repeat for other files** as needed

## After Downloading: Running the App

Once you have the files on your computer:

1. **Open Terminal/Command Prompt**
   - Navigate to the Discount-App folder
   - **Windows:** You can also Shift + Right-click in the folder → "Open PowerShell window here"
   - **Mac/Linux:** You can also right-click → "Open Terminal here"

2. **Run the app**
   ```bash
   python discount_app.py
   ```
   
   Or if that doesn't work, try:
   ```bash
   python3 discount_app.py
   ```

3. **View the results**
   - The app will display deals in the terminal
   - A `deals.json` file will be created with all the deals

## Troubleshooting

### "python is not recognized" or "command not found"

**Problem:** Python is not installed or not in your PATH

**Solution:**
1. Install Python from https://www.python.org/downloads/
2. During installation, make sure to check **"Add Python to PATH"**
3. Restart your terminal/command prompt

### "No such file or directory"

**Problem:** You're not in the correct folder

**Solution:**
1. Use `cd` command to navigate to the folder
2. Use `ls` (Mac/Linux) or `dir` (Windows) to list files
3. Make sure you can see `discount_app.py` in the list

### The app runs but shows errors

**Problem:** Missing dependencies or Python version too old

**Solution:**
1. Check Python version: `python --version` (should be 3.7+)
2. The base app doesn't need extra packages
3. If you added web scraping, run: `pip install -r requirements.txt`

## Need More Help?

- Check the main [README.md](README.md) for usage instructions
- Look at [examples.py](examples.py) for code examples
- Create an issue on GitHub if you encounter problems

## What's Next?

After downloading and running the app:
1. Read the [README.md](README.md) for full usage instructions
2. Explore [examples.py](examples.py) to learn how to customize the app
3. Start implementing web scraping to get real deals!
