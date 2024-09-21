from utils.logger import Logger
import tkinter as tk
import ttkbootstrap as ttk


def main():
    logger = Logger(log_file="app.log")

    root = tk.Tk()
    root.title(" ScrapeGoat Tool")
    # Set the initial window size
    window_width = 1260
    window_height = 915
    root.geometry(f"{window_width}x{window_height}")
    root.resizable(False, False)


    # Create a notebook
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)

    # Create dummy tabs
    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    tab3 = ttk.Frame(notebook)

    # Add tabs to the notebook
    notebook.add(tab1, text="Tab 1")
    notebook.add(tab2, text="Tab 2")
    notebook.add(tab3, text="Tab 3")
    # Import BrowserClient
    from driver.selenium import BrowserClient

    # Create a BrowserClient instance
    browser_client = BrowserClient(timeout_after=30, max_retries=3, browser_headless=False)

    # Initialize the driver
    browser_client.initialize_driver()

    # Function to open a URL in a new tab
    def open_url():
        url = "https://www.example.com"  # Replace with your desired URL
        browser_client.open_page_in_same_tab(url)

    # Add a button to Tab 1 to open a new tab
    open_tab_button = ttk.Button(tab1, text="Open New Tab", command=open_url)
    open_tab_button.pack(padx=20, pady=20)

    # Ensure the browser is closed when the application exits
    root.protocol("WM_DELETE_WINDOW", lambda: [browser_client.close_driver(), root.destroy()])

    # Add some dummy content to each tab
    ttk.Label(tab1, text="This is Tab 1 content").pack(padx=20, pady=20)
    ttk.Label(tab2, text="This is Tab 2 content").pack(padx=20, pady=20)
    ttk.Label(tab3, text="This is Tab 3 content").pack(padx=20, pady=20)
    root.mainloop()

if __name__ == "__main__":
    main()
    
