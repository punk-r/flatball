
import support_functions
from support_functions import *



# mini field testing-----------------------------------------------
if True:
    test_data = [ [[True,False,False],[True,False,False]], \
                  [[True,True,False],[True,True,False]], \
                  [[False,True,True],[False,True,True]], \
                  [[False,False,True],[False,False,True]], \
                  [[True,True,True],[True,True,True]]   ]

    test_results= [  [0  , 0  , 0.3 , 0.3] , \
                     [0  , 0  , 0.6 , 0.6] , \
                     [0.3, 0.3, 1   , 1] , \
                     [0.6, 0.6, 1   , 1] , \
                     [0  , 0  , 1   , 1]  ]

    for test_loops in range (2, 3): #len(test_data)):
        ratio = calculate_trening_area_ratio ( test_data[test_loops] )
        print ("        ")
        print (" test_data[test_loops]    ",test_data[test_loops])
        print ("  ratio calculated        ",   ratio    )
        print ("  test_results            ",   test_results[test_loops]    )
        #print ("  coordinates data        [100,100,90,30] "  )
        print ("  coordinates doonehr     ", calculate_trening_area_coordinates ( ratio ,   [  100,100,90,30 ]   ,"horisontal"))
        print ("  coordinates dooneVr     ", calculate_trening_area_coordinates ( ratio ,   [  100,100,30,90 ]   ,"vertical"))
