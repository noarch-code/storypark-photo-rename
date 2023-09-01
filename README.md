# Storypark Photo Archive Renaming
This program will rapdily rename and change EXIF information from your Storypark archive export. 

**Output:**
- Updated EXIF data for valid JPGs that reflects the story's date
- Updated filenames from "STORYID"-story-name-IDENTIFIER.* to "DATE"-story-name-IDENTIFIER.*

**Limitations:**
- Will only rename "Story" based photos (not "Notes")
- Video files will be renamed, but obviously no EXIF information will be updated


## How to Use
- Export from Storypark using this approach: https://help.storypark.com/en/articles/56109-export-all-your-stories-and-notes
- Put the python file within the root of the exported directory (same directory as **stories_index.html**)
- Execute the script
- The photos within /Files will be updated and renamed

Note: this script can only be run once as it will change the filenames.

## Future Options
Some considerations while writing this initial version that would be helpful additions.
- Include "Notes" as well as stories
- Add the ability to trim whitespace borders on some images
- Programatic upscaling
