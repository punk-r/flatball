from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree
import os.path                                  #oprait import
from os import path
import neural_network
from neural_network import *

# vytvori xml file z dat teamu/hrace
def create_xml_file(team_data,path):
    # input ma tvar :
    # [[team_name,data1,data2],5x [pl_name, pl_ID,pl_position,trening_type,trening_time]]
    # data1 a data2 jou pouze pro beh hry neukladaji ses

    root = Element("team")
    tree = ElementTree(root)

    team_name = Element("team_name")
    root.append(team_name)
    team_name.text = team_data[0][0]
                                                                                # pridat data pro statistiku?asi na konec
    # 1 protoze vstup ma prvni clen jmeno teamu
    for loop in range (1,len(team_data)):
        root2 = Element("player")
        tree2 = ElementTree(root2)
        root.append(root2)
                                                                                # pak pridat osobnost hrace
        plr_name = Element("plr_name")
        player_ID = Element("player_ID")
        player_type = Element("player_position")
        trening_type = Element("trening_type")
        trening_time = Element("trening_time")

        root2.append(plr_name)
        plr_name.text = team_data[loop][0]
        root2.append(player_ID)
        player_ID.text = team_data[loop][1]
        root2.append(player_type)
        player_type.text= team_data[loop][2]
        root2.append(trening_type)
        trening_type.text= team_data[loop][3]
        root2.append(trening_time)
        trening_time.text= team_data[loop][4]

    tree.write(open( path + team_data[0][0] + '.xml','wb'))

# funkce vrati list hodnot ctenych z xml pro team
# vystup:
# [[team_name,data1,data2],5x [pl_name, pl_ID,pl_position,trening_type,trening_time]]
# data1 a data2 jsou generovane informace, ne ctene z xml
def f_read_from_xml(file):
    team_details = [ ["team_details","original","notselected"],"pl1","pl2","pl3","pl4","pl5"]
    mytree = etree.parse(file)
    myroot = mytree.getroot()
    team_details[0][0] = myroot[0].text
    for player_loop in range(1,len(team_details)):
        team_details[player_loop] = [myroot[player_loop ][0].text, \
                                     myroot[player_loop ][1].text, \
                                     myroot[player_loop ][2].text, \
                                     myroot[player_loop ][3].text, \
                                     myroot[player_loop ][4].text]

    return team_details


# zkontroluje teams folder a popripade jej vytvori
# pri prvnim spusteni vytvori default hodnoty pro Tensorflow model
def f_teams_folders_check():
                                                                                #rozdel na dve funkce volane az pozdeji nacist data , vykresli data!!!!!!
    if path.exists("Teams"):
        pass
    else:
        os.mkdir("Teams")
        os.chdir("Teams")
        os.mkdir("Home")
        os.mkdir("Away")
        os.mkdir("Archive")

        # ukazkovy team, ulozen pri prvnim spusteni hry
        # input ma tvar : [team_name,5x [pl_name, pl_ID,pl_position,trening_type,trening_time]]
        default_team = [["A","original","notselected"],["andy","1","gk","3","trening_time"], \
                                                      ["tom","2","pl_position","3","trening_time"], \
                                                      ["john","3","pl_position","3","trening_time"], \
                                                      ["gary","4","pl_position","3","trening_time"], \
                                                      ["tony","5","pl_position","3","trening_time"]]


        create_xml_file (default_team, get_path_home_folder())


        # defaults models
        for players_loop in range (1,len(default_team)):           #zacina 1, prvni prvek je jmeno teamu
            model_inputs = default_team[players_loop][3]
            model = create_model( model_inputs  )                                                                                     # nebude konstanta
            model.save(get_path_home_folder() + default_team[players_loop][1]  + ".h5")
