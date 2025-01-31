import os 
import shutil 
import pandas as pd 

def is_empty(file_path):
    """Check if a file is empty."""
    return os.path.getsize(file_path) == 0

def is_temp_file(filename):
    """Check if a file is a temporary file."""
    temp_extensions = ['.bak', '.temp', '.swp']
    return filename.startswith('~$') or any(filename.endswith(ext) for ext in temp_extensions)



def file_management(source_dir):
    file_types = ['csv', 'txt', 'pdf', 'docx', 'jpg', 'png', 'mp3', 'wav', 'mp4', 'avi', 'mkv']
    #define folder for each file type
    for file_type in file_types: 
        folder= os.path.join(source_dir, f"{file_type}_files") #loc/pathway to create folder
        if not os.path.exists(folder): #checks if that folder exist
            os.makedirs(folder) #makes folder in that path
     # Step 2: Create a folder for empty files
    empty_folder = os.path.join(source_dir, "empty_files")
    if not os.path.exists(empty_folder):
        os.makedirs(empty_folder)
    
    # Step 3: Traverse the directory structure
    for dirpath, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)

            # Skip directories or hidden files
            if os.path.isdir(file_path) or filename.startswith('.'):
                continue

            # Step 4: Delete temporary files
            if is_temp_file(filename):
                print(f"Deleting temporary file: {file_path}")
                os.remove(file_path)
                continue

            # Step 5: Move empty files to the "empty_files" folder
            if is_empty(file_path):
                print(f"Moving empty file to: {empty_folder}")
                shutil.move(file_path, os.path.join(empty_folder, filename))
                continue

            # Step 6: Organize files into folders based on their type
            file_extension = filename.split('.')[-1].lower()
            if file_extension in file_types:
                target_folder = os.path.join(source_dir, f"{file_extension}_files")
                print(f"Moving {filename} to {target_folder}")
                shutil.move(file_path, os.path.join(target_folder, filename))
            
    print("File management and cleanup complete.")


def clean_csv_file(csv_path):
    """Clean a CSV file: remove duplicates, handle missing values, normalize data."""
    try:
        df = pd.read_csv(csv_path)         # Step 1: Load the CSV file into a DataFrame using panda
        print(f"Cleaning CSV file: {csv_path}")
        
        # Step 2: Remove duplicate rows
        initial_rows = len(df)
        df = df.drop_duplicates()
        print(f"Removed {initial_rows - len(df)} duplicate rows.")

        # Step 3: Handle missing values (fill with 'N/A' or drop rows if necessary)
        missing_values = df.isnull().sum().sum()
        print(f"Found {missing_values} missing values.")
        df = df.fillna("N/A")  # Replace missing values with "N/A"

        # Step 4: Normalize column names (lowercase and replace spaces with underscores)
        df.columns = df.columns.str.lower().str.replace(' ', '_')

        # Step 5: Save the cleaned data back to the same file
        df.to_csv(csv_path, index=False)
        print(f"Cleaned data saved to: {csv_path}")

    except Exception as e:
        print(f"Error cleaning file {csv_path}:{e}")
      



def main():
    from pathlib import Path 
    # Step 1: Get the source directory path
    source_dir = input("Enter the source directory path for file management: ")
    source_dir =Path(source_dir)

    # Step 2: Perform file management
    file_management(source_dir)
    
    # Step 3: Clean all CSV files in the CSV folder
    csv_folder = os.path.join(source_dir, "csv_files")
    if os.path.exists(csv_folder):
        for csv_file in os.listdir(csv_folder):
            csv_path = os.path.join(csv_folder, csv_file)
            if os.path.isfile(csv_path) and csv_file.endswith('.csv'):
                clean_csv_file(csv_path)
    
    print("All tasks complete!")

if __name__ == "__main__":
    main()