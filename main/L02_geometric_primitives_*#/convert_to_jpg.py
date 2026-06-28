'''
### Features                                                                                                                                                 
  1. Intelligent Scan: Traverses the target directory recursively (by default) to detect
  convertible image formats ( .png ,  .heic ,  .webp ,  .bmp ,  .tiff ,  .tif ,  .gif ,  .
  png.heic ).                                                                           
  2. Skipping Logic: Automatically skips files that are already in  .jpg  or  .jpeg     
  formats.                                                                              
  3. Robust Processing: Uses  Pillow  (PIL) for standard images and automatically falls 
  back to ImageMagick  convert  (which is configured on your system) for formats like  .
  heic .                                                                                
  4. Auto-Cleanup: Deletes the original non-jpg files after successful conversion.      
                                                                                        
  ### Usage                                                                             
           
  Run the program by passing the target dataset directory as an argument:
  
    python3 convert_to_jpg.py <path_to_dataset>
    
  #### Examples:
  
  • Standard conversion and cleanup:
    python3 convert_to_jpg.py main/L02_geometric_primitives/L02_dataset
    
  • Keep original files (do not delete after conversion):
    python3 convert_to_jpg.py main/L02_geometric_primitives/L02_dataset --keep
                                                                                        
  • Non-recursive (process only the top-level folder):
    python3 convert_to_jpg.py main/L02_geometric_primitives/L02_dataset --no-recursive
'''


#!/usr/bin/env python3
import os
import argparse
import subprocess
import shutil
from PIL import Image

# Supported image extensions that we want to convert to JPG (excluding .jpg and .jpeg)
CONVERTIBLE_EXTENSIONS = {
    '.png', '.heic', '.webp', '.bmp', '.tiff', '.tif', '.gif', '.png.heic'
}

def is_imagemagick_available():
    return shutil.which("convert") is not None

def convert_image(src_path, dest_path, use_imagemagick=False):
    """
    Converts src_path to dest_path (JPG).
    Returns True if successful, False otherwise.
    """
    lower_src = src_path.lower()
    
    # HEIC files require ImageMagick if pillow-heif is not installed
    if lower_src.endswith('.heic') or lower_src.endswith('.png.heic'):
        if use_imagemagick:
            try:
                subprocess.run(
                    ["convert", src_path, dest_path], 
                    check=True, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE
                )
                return True
            except subprocess.CalledProcessError as e:
                print(f"Error converting {src_path} using ImageMagick: {e.stderr.decode().strip()}")
                return False
        else:
            print(f"Cannot convert HEIC file {src_path}: ImageMagick 'convert' is not installed.")
            return False
            
    # For other formats, try Pillow first
    try:
        with Image.open(src_path) as img:
            # Convert to RGB if it has an alpha channel or palette to avoid save errors
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                # Create a white background
                bg = Image.new('RGB', img.size, (255, 255, 255))
                bg.paste(img, (0, 0), img.convert('RGBA'))
                bg.save(dest_path, 'JPEG')
            else:
                img.convert('RGB').save(dest_path, 'JPEG')
        return True
    except Exception as pillow_err:
        # Fallback to ImageMagick if available
        if use_imagemagick:
            try:
                subprocess.run(
                    ["convert", src_path, dest_path], 
                    check=True, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE
                )
                return True
            except subprocess.CalledProcessError as e:
                print(f"Error converting {src_path} with Pillow and ImageMagick: {e.stderr.decode().strip()}")
                return False
        else:
            print(f"Error converting {src_path} with Pillow: {pillow_err}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Convert dataset images to .jpg format.")
    parser.add_argument("dataset_dir", help="Path to the dataset directory to scan.")
    parser.add_argument("--keep", action="store_true", help="Keep the original files after successful conversion (default: delete original).")
    parser.add_argument("--no-recursive", action="store_true", help="Do not scan subdirectories recursively.")
    
    args = parser.parse_args()
    
    dataset_dir = os.path.abspath(args.dataset_dir)
    if not os.path.isdir(dataset_dir):
        print(f"Error: {dataset_dir} is not a valid directory.")
        return
        
    has_im = is_imagemagick_available()
    if not has_im:
        print("Warning: ImageMagick 'convert' tool is not found. HEIC conversions might fail.")
        
    recursive = not args.no_recursive
    keep_original = args.keep
    
    converted_count = 0
    skipped_count = 0
    failed_count = 0
    
    print(f"Scanning directory: {dataset_dir}")
    print(f"Recursive: {recursive}")
    print(f"Delete original: {not keep_original}\n")
    
    # Collect files to process
    files_to_process = []
    
    if recursive:
        for root, _, files in os.walk(dataset_dir):
            for file in files:
                files_to_process.append(os.path.join(root, file))
    else:
        for file in os.listdir(dataset_dir):
            full_path = os.path.join(dataset_dir, file)
            if os.path.isfile(full_path):
                files_to_process.append(full_path)
                
    for filepath in sorted(files_to_process):
        lower_path = filepath.lower()
        
        # Check if already a JPG/JPEG
        if lower_path.endswith('.jpg') or lower_path.endswith('.jpeg'):
            skipped_count += 1
            continue
            
        # Check if it has a convertible extension
        is_convertible = False
        for ext in CONVERTIBLE_EXTENSIONS:
            if lower_path.endswith(ext):
                is_convertible = True
                break
                
        if not is_convertible:
            continue
            
        # Determine destination path
        if lower_path.endswith('.png.heic'):
            dest_path = filepath[:-9] + ".jpg"
        else:
            base, _ = os.path.splitext(filepath)
            dest_path = base + ".jpg"
            
        print(f"Converting: {os.path.basename(filepath)} -> {os.path.basename(dest_path)}")
        
        if convert_image(filepath, dest_path, use_imagemagick=has_im):
            converted_count += 1
            if not keep_original:
                try:
                    os.remove(filepath)
                except Exception as e:
                    print(f"Warning: Could not remove original file {filepath}: {e}")
        else:
            failed_count += 1
            
    print("\n=== Conversion Summary ===")
    print(f"Successfully converted: {converted_count}")
    print(f"Skipped (already JPG/JPEG): {skipped_count}")
    print(f"Failed conversions: {failed_count}")

if __name__ == "__main__":
    main()
