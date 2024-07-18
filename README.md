# G-Code Processing Tool

Hello to the next Software Engineer that is going to be working with this app! 
Hope that this code will not cause any problems for you and you will develop a better thing out of it! 

This app is built to optimize the printing time of the salmon fillet, but can be used for anything 3D printed with 2 nozzles. 

This is how the algorithm works:

======================================================LOGIC OF THE ALGORITHM======================================================

# File preparation

**Cleaning Process**
    
    - The algorithm cleans the original file by removing all comments and empty lines.
    
    - It deletes all instances of "G92 E0" after every "T0" or "T1" command for improved performance.

    - Additionally, it adds "E0.0" to lines that do not already have it for better performance.

# Group Separation

**Minimizing G-code Length in Separate Files**
    
    - Each group in the G-code file begins with the command "G92 E0", marking the start of a group.
    
    - This algorithm identifies each group by locating the positions of "G92 E0" commands, as they 
      delineate the boundaries of each group.
    
    - Additionally, it examines the surrounding lines within a range of 7 lines above and below each 
      "G92 E0" command to identify associated T values.
    
    - The algorithm stores relevant information for each group, such as X and Y coordinates, Z values, 
      T values, and line numbers, in a temporary file named "1_temp.txt".
    

# Group Optimization

**Optimizing Output of Temporary File**
    
    - The optimization process involves analyzing the contents of the "1_temp.txt" file.
    
    - It calculates the closest part based on the start and end coordinates of X and Y and arranges 
      them accordingly for optimization.
    
    - During optimization, if the algorithm uses the end coordinates as the starting point, it marks 
      that line with an "XY" label before moving on to the next part.
    
    - Then another function traverses through the file and flips the groups marked with "XY", ensuring 
      they are prepared for insertion into a new G-code file.
    
    - Additionally, a function recalculates all extrusion values throughout the entire file to ensure 
      that the flipped groups have the correct extrusion rate, facilitating proper printing.
    
    - Subsequently, the rearranger function extracts line numbers from the temporary file, retrieves 
      the corresponding start and end lines, and copies the content between them.
    
    - This content is then pasted into another file, resulting in the reassembly of the new, optimized G-code.
    
    - After completion, the algorithm ensures that important lines are placed at the beginning and end 
      of the final optimized G-code file.
    
======================================================THE END======================================================

## Features

- **Comment and Empty Line Removal**: Removes comments and empty lines from the input G-code file to 
    reduce file size and improve readability.

- **G92 Command Optimization**: Optimizes the use of G92 commands by removing unnecessary G92 commands 
    after T0 or T1 commands.

- **E-Line Editor**: Adds E0.0 at the end of the line to the coordinate that doesnt have an E

- **G92 Group Counting**: Counts the groups of G-code commands based on G92 commands and extracts 
    relevant information such as line numbers, coordinates, Z levels, and T values.

- **XY Line Extraction**: Finds lines with XY coordinates and extracts them for further processing.

- **XY Line Removal**: Removes XY coordinates from previous lines in the G-code file to prevent overlapping 
    or duplicate commands.

- **Group Reordering**: Reorders groups of G-code commands to ensure alternating T values (T0 and T1) 
    for better printing or machining performance.

- **Group Deletion**: Deletes consecutive groups of the same T value to optimize toolpath and extrusion.

- **Extrusion Rate Recalculation**: Recalculates extrusion rates in the G-code file, so the flipped lines 
    are properly printed.


## Files and their purpose

- **clearence**
  Clearance contains all the functions to clean the gcode file
- **editor**
  Function to add Extrusion rate at the end of the line without extrusion rate
- **temporary**
  Function to create temporary file to work with in the future
- **countingG92**
  First algorithm that collects all the data from the original file and stores it in the 1_temp.txt
- **optimization**
  Big file with lots of functions and BIG functions, it optimizes the groups and makes them logical
- **extrusionrate**
  Recalculating function that fixes the issue with flipped lines, and makes them print in the right way
- **rearranger**
  Function that builds new gcode file from the beginning based on the optimized structure from the optimization file
- **owo_flipper**
  Something that I tried to do, and it looks like it works, but it needs improvements and it will work, so play around with it

## Usage

  **Executable**
  If you want to open the app from the folder, then look for RevoOptimization+.exe, launch it and you 
  should get the app running

  **Terminal**
  Go to the terminal, make sure that its set to the folder where all the scripts are and write this command: 
  
  python main_app.py



======================================================Good Luck!======================================================