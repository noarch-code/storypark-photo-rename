from bs4 import BeautifulSoup
import os
from datetime import datetime, timedelta
import piexif

with open("stories_index.html") as fp:
    
	## this section will load the stories HTML and parse all of the stories within
	## the HTML content
    soup = BeautifulSoup(fp, "html.parser")
    stories = soup.findAll("div", class_="story")
    dateDictionary = {}
    
    for story in stories:
		
		## pull the story title block, which contains the name and date
        storyTitle = story.find('h1')
        strStoryTitle = str(storyTitle)
        
		##find the title (start/end and then extract), dependent on storyparks current formatting
        titleStart = strStoryTitle.find('<h1>')+5
        titleEnd = strStoryTitle.find('<small>')-1
        strTitle = strStoryTitle[titleStart:titleEnd]
        
		##pull the date 
        dateStart = strStoryTitle.find('time=')+6
        dateEnd = dateStart + 10
        storyDate = strStoryTitle[dateStart:dateEnd]
		
		## this section gets the image names for this story by finding the first image listed in the story
		## we extract the story/image ID from here
        storyImage = story.find('img')
        strImage = str(storyImage)
        imgStart = strImage.find('Files/')
        imgEnd = imgStart+14
        imgName = strImage[(imgStart+6):imgEnd]
        
        ## taking the story/image ID we can create keypairs for the imageID and the date 
		## the date will be used in the filename instead of the story ID
        dateDictionary[imgName] = storyDate
        

	## this section will process the image files by loading all of the files withing the "/Files" subdirector
    folder = str(os.getcwd())+'/Files/'
    for file_name in os.listdir(folder):
        
		## using the dictionary see if the file matches a known story
        if file_name[0:8] in dateDictionary:
                        
			## Establish the new name for the file
			## We're converting from storypark storyID to date YYYY-MM-DD, the remaining filename is the same
            oldName = os.path.join(folder,file_name)
            tempNewName = dateDictionary[file_name[0:8]]+file_name[8:]
            newName = os.path.join(folder,tempNewName)
            
			## format the datetime for the EXIF data
            tempExifDate = datetime.strptime(dateDictionary[file_name[0:8]]+'T00:00:00', '%Y-%m-%dT%H:%M:%S')
            newExifDate = tempExifDate.strftime('%Y:%m:%d %H:%M:%S')
            
            ## process jpgs only for EXIF updates            
            if (oldName[-3:] == 'jpg'):
                ##if malformed JPG error out
                try:
                    ## change the EXIF information, including file dates
                    exif_dict = piexif.load(oldName)
                    exif_dict['0th'][piexif.ImageIFD.DateTime] = newExifDate
                    exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = newExifDate
                    exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = newExifDate
                    exif_bytes = piexif.dump(exif_dict)
                    piexif.insert(exif_bytes, oldName)
                except:
                    print('ERROR - NO EXIF: ' + oldName)
            else:## exif updates
                print('ERROR - NOT A JPG FILE: ' + oldName)
            ## Execute the rename (can only be run once with a rename) comment out for a dry run
            ##os.rename(oldName, newName)

