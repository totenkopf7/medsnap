import os

def collect_dart_files(main_folder, output_file="all_dart_files.txt"):
    with open(output_file, "w", encoding="utf-8") as out:
        for root, _, files in os.walk(main_folder):
            for file in files:
                if file.endswith(".dart"):
                    file_path = os.path.join(root, file)
                    
                    out.write(f"{file}:\n")
                    out.write("// " + "-" * 50 + "\n")
                    
                    with open(file_path, "r", encoding="utf-8") as f:
                        out.write(f.read())
                    
                    out.write("\n\n")  # spacing between files
    
    print(f"✅ All Dart files have been combined into {output_file}")

# Example usage:
# Replace "D:\Send To HardDisk\med_snap\lib" with your main folder path
collect_dart_files(r"D:\Send To HardDisk\med_snap\lib")
