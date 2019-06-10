import numpy as np
import xlrd
import sys

# donor_wb = xlrd.open_workbook('Donor.xlsx')
# ngo_wb   = xlrd.open_workbook('NGO.csv')
# me need not be a list
# it is the trigger. It is kept as list for generality of data structures
# me_wb    = xlrd.open_workbook('me.csv')

'''
fetch n,m from the database
fetch x,y for restaurant
fetch x,y for NGO
fetch x,y for 'me
'''

# we actually won't use distance param of donor
# we need distance of ngo and me (which change each time wrt donor x,y)
# update later (IGNORE)
donor = {'phNo': 0, 'unit': 0, 'x': 0, 'y': 0, 'dist':0}
ngo   = {'phNo': 0, 'unit': 0, 'x': 0, 'y': 0, 'dist':0}
me    = {'phNo': 0, 'unit': 0, 'x': 0, 'y': 0, 'dist':0}

# ===================================================================
# retreive from the database
n_donor = 3
n_ngo   = 3
# ===================================================================

l_donor = []
l_ngo   = []
l_me    = []
l_phNo  = []
l_me    = []

def show(msg, _list):
  print(msg, _list, '\n')
  print

#eucledian distance
def getDistance(x1, y1, x2, y2):
  return int(round(((x1-x2)**2) + ((y1-y2)**2))**0.5)


# run for loop to retrieve values from DB
def init():
  print('init function ex... \n')
  #retrieve donor values
  donor_wb  = xlrd.open_workbook('databases/Donor.xlsx')
  worksheet = donor_wb.sheet_by_name('Sheet1')
  col_donor = 5
  
  #(int)value = (int)worksheet.cell(row, cell)
  _dict = {'phNo': 0, 'unit': 0, 'x': 0, 'y': 0, 'dist':0}
  for row in range(n_donor):
    _dict['phNo'] = worksheet.cell_value(row, 0)
    _dict['unit'] = worksheet.cell_value(row, 2)
    _dict['x'] = worksheet.cell_value(row, 3)
    _dict['y'] = worksheet.cell_value(row, 4)
    l_donor.append(_dict.copy())
  show('final list of donors \n', l_donor)

  #retrieve NGO values
  col_ngo    = 5
  ngo_wb     = xlrd.open_workbook('databases/NGO.xlsx')
  _worksheet = ngo_wb.sheet_by_name('Sheet1')
  for _row in range(n_ngo):
    _dict['phNo'] = _worksheet.cell_value(_row, 0)
    _dict['unit'] = _worksheet.cell_value(_row, 2)
    _dict['x'] = _worksheet.cell_value(_row, 3)
    _dict['y'] = _worksheet.cell_value(_row, 4)
    l_ngo.append(_dict.copy())
  show('final list of NGOs \n', l_ngo)

  
  #each time user enters unit, x, y.. the code is triggered
  col_me = 5
  me_wb  = xlrd.open_workbook('databases/me.xlsx')
  _worksheet_ = me_wb.sheet_by_name('Sheet1')
  _dict['phNo'] = _worksheet_.cell_value(row, 0)
  _dict['unit'] = _worksheet_.cell_value(row, 2)
  _dict['x'] = _worksheet_.cell_value(row, 3)
  _dict['y'] = _worksheet_.cell_value(row, 4)
  l_me.append(_dict.copy())
  show('final list of me \n', l_me)
  show('final list of donor \n', l_donor)
# what we have now are lists of dictionaries
# [{'phNo':1, 'unit':100, 'x':30, 'y':10}, {'phNo':2, 'unit':157, 'x':70, 'y':14}]

def minimum(a, n):
  minpos = a.index(min(a))  
  # printing the position
  return minpos
      

def ngo_Allot_units(l_donor, l_ngo):                       
  for each_donor in l_donor:
    _sort_l = []
    contact = []
    x1 = each_donor['x']
    y1 = each_donor['y']
    print(x1, y1, ' ') #works
    l_dist = []
    for each_ngo in l_ngo:
      x2 = each_ngo['x']
      y2 = each_ngo['y']
      print(x2, y2, ' ') #works
      _dist_ = getDistance(x1, y1, x2, y2)
      l_dist.append(_dist_)
    print('l_dist', l_dist, ' ')
    index = minimum(l_dist, len(l_dist))
    print(index, ' ')

    # ==========================================================
    # update database after executing below command
    l_ngo[index]['unit'] += each_donor['unit']
    # ==========================================================
    
    #find_least_dist_index(l_ngo)
    print('each_ngo', l_ngo, ' ')
  show('\n NGOs after allotment \n', l_ngo)


def me_gets_food(units, x, y):
  x_me = x
  y_me = y
  print('me_x: ', x_me, 'me_y:', y_me, '\n')
  for each_ngo in l_ngo:
    x1 = each_ngo['x']
    y1 = each_ngo['y']
    d = getDistance(x1, y1, x_me, y_me)
    each_ngo['dist'] = d
    #print('ngo_x: ', x1, 'ngo_y:', y1, 'dist: ', d, ' ')
  sorted(l_ngo, key = lambda i: i['dist'])
  print('final NGOs: ')
  print(l_ngo)

  # NGOs are now sorted according to distance
  # return the closest NGO phNo that satisfies unit reqd by me
  # update the database also. else successive runs will break
  for i in range(len(l_ngo)):
    u_ngo = l_ngo[i]['unit']
    if units < u_ngo or units == u_ngo:
      l_ngo[i]['unit'] -= units

      # ==========================================================
      # update below into output database for UI
      phNo, _x, _y, _dist = l_ngo[i]['phNo'], l_ngo[i]['x'], l_ngo[i]['y'], l_ngo[i]['dist']
      # ==========================================================
      break #sys.exit()
    else:
      print('None suitable \n')
  # all modified values must be updated in the table/ database    
  print('my units: ', units)
  print('\n', l_ngo)
  print(' ===============================:\n\n', 'Closest NGO details')
  print('phNo: ', phNo, 'x: ', _x, 'y: ', _y, 'dist: ', _dist)

                           
def main():
  init()
  ngo_Allot_units(l_donor, l_ngo)
  # read requirements of me: units, x,y from the DB
  u = 100
  # get me x
  x = l_me[0]['x']
  # get me y
  y = l_me[0]['y']
  me_gets_food(u,x,y)

if __name__ == "__main__":
  main()
                         
                           
                         
        
  














