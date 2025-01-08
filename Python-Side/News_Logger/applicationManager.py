import subprocess
import time

# Paths to your scripts and executable
python_script1 = "news_logger.py"
python_script2 = "telegramSender.py"
c_program = "./analyzer"

while True:
    try:
        # Step 1: Run the first Python script
        print("Running the first Python script...")
        subprocess.run(["python3", python_script1], check=True)
        print("First Python script finished.")

        # Step 2: Run the C program
        print("Running the C program...")
        subprocess.run([c_program], check=True)
        print("C program finished.")

        # Step 3: Run the second Python script
        print("Running the second Python script...")
        subprocess.run(["python3", python_script2], check=True)
        print("Second Python script finished.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running a script or program: {e}")

    # Wait for 1 hour (30 secs) before the next iteration
    print("Waiting for 1 hour before the next run...")
    time.sleep(30 * 60)
