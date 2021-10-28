'''
TASKS:
using REST API
    - show 5 images from given library, year. planet is on the picture
    - number of records for given planet and year and direct user to video
'''

import requests
import json

class images_viever ():
    API_ROOT_nasa = "https://images-api.nasa.gov/"
    No_of_images = 5

    def get_images(self,year_from,year_to,planet_name):
        list_of_images = []
        end_point = self.API_ROOT_nasa + "search?" + "&media_type=image" + "&keywords=" + planet_name + "&year_start=" + str(year_from) + "&year_end=" + str(year_to)
        #print(end_point)
        query = requests.get(end_point)
        if query.status_code == 200:
            query_py_format = query.json()
            for save_loop  in range (0,self.No_of_images):
                list_of_images.append(query_py_format["collection"]["items"][save_loop]["href"] )

        return list_of_images

class videos_counter():
    API_ROOT_nasa = "https://images-api.nasa.gov/"

    def  get_videos(self,year_from,year_to,planet_name):
        number_of_videos = 0
        end_point = self.API_ROOT_nasa + "search?" + "&media_type=video" + "&keywords=" + planet_name + "&year_start=" + str(year_from) + "&year_end=" + str(year_to)
        #print("original end point",end_point)
        query = requests.get(end_point)
        # protection for invalid link
        if query.status_code == 200:
            query_py_format = query.json()
            for item in query_py_format["collection"]["items"]:
                link = item["href"]
                #print ( "link", link)
                new_query = requests.get(link)
                if new_query.status_code == 200:
                    new_query_py_format = new_query.json()
                    for new_link in new_query_py_format:
                        new_link_lenght = len(new_link)
                        # video ends .mp4
                        if new_link[new_link_lenght-1] == "4":
                            #print ("new_link", new_link)
                            number_of_videos = number_of_videos + 1

        return number_of_videos

#---------------------------------------------------------------------------------
The_images_viever = images_viever()
The_videos_counter = videos_counter()

images = The_images_viever.get_images(2018,2018,"Mars")

for print_loop in range (0,5):
    print ("image per criteria :" , images[print_loop])

print("")
print ("Videos calculating started, might take a few seconds for large datasets")

number_videos = The_videos_counter.get_videos(2018,2018,"Mars")

print ("number of videos per criteria :" , number_videos)
