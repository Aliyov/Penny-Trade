import subprocess
import time

# Paths to your scripts and executable
py_news_logger = "news_logger.py"
py_telegram_sender = "telegramSender.py"
c_news_analyzer = "./analyzer"
c_news_country_finder = "./countries"

while True:
    try:
        # 1 Run news logger
#        print("Logging the recent news...")
        subprocess.run(["python3", py_news_logger], check=True)

        # 2 Run C program to check relativity and positivity
#        print("Analyzing the news...")
        subprocess.run([c_news_analyzer], check=True)
    
        # 3 Run C code to check mentioned countries
#        print("Trying to find source country...")
        subprocess.run([c_news_country_finder], check=True)
        
        # Step 3: Run the second Python script
#        print("Sending to the telegram...")
        subprocess.run(["python3", py_telegram_sender], check=True)
        
        print("Done.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running a script or program: {e}")

    # Wait for 30 min before the next iteration
#    print("Waiting for 30 minutes before the next run...")
    time.sleep(30 * 60)
