from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree

'''
team  jmeno
hrac  jmeno typ_treningu hodin_treningu pozice

'''
def create_xml_file(team_data,path):
    # input ma tvar : [team_name,5x [pl_name,pl_details1,pl_details1,pl_details1]]

    root = Element("team")
    tree = ElementTree(root)

    team_name = Element("team_name")
    root.append(team_name)
    team_name.text = team_data[0]

    for loop in range (1,len(team_data)): # 1 protoze vstup ma prvni clen jmeno teamu
        root2 = Element("player")
        tree2 = ElementTree(root2)
        root.append(root2)

        plr_name = Element("plr_name")
        trening_type = Element("trening_type")
        trening_time = Element("trening_time")
        player_type = Element("player_type")

        root2.append(plr_name)
        plr_name.text = team_data[loop][0]
        root2.append(trening_type)
        trening_type.text = team_data[loop][1]
        root2.append(trening_time)
        trening_time.text= team_data[loop][2]
        root2.append(player_type)
        player_type.text= team_data[loop][3]

    tree.write(open( path + "\\"+ team_data[0] + '.xml','wb'))


# vystup:  [team_name,5x [pl_name,pl_details1,pl_details1,pl_details1]]
def read_from_xml(file):
    team_details = [ "team_details","pl1","pl2","pl3","pl4","pl5"]
    mytree = etree.parse(file)
    myroot = mytree.getroot()
    team_details[0] = myroot[0].text
    for player_loop in range(1,len(team_details)):
        team_details[player_loop] = [myroot[player_loop ][0].text, \
                                     myroot[player_loop ][1].text, \
                                     myroot[player_loop ][2].text]
    #print (team_details)
    return team_details

#-------------------------------------------------------------------------------------------------


#read_from_xml('dfault.xml')
