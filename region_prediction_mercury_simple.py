# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 11:02:28 2024

@author: Kristin
"""
# =============================================================================
# The aim of this programme is to predict the region in which the 
# given coordinates (spacecraft) is located
# 
# Input: - coordinates x, y, z in km in MSO 
#        - r_hel in AU 
#        (- DI (disturbance index): value from 0 (quiet) to 100 (disturbed). default: 50) 
# 
# Output: Region/boundary  
# 
# =============================================================================
# Planet: inside Planet     1
# MAG: Magnetosphere        2
# MP: Magnetopause          3
# MSH: Magnetosheath        4
# BS: Bowshock              5
# SW: Solar Wind            6

# no prediction: 0
# =============================================================================

import numpy as np

def get_region(x_mso_km, y_mso_km, z_mso_km, r_hel_AU, di = 50): 
    print('start region prediction ')
    #check wether input in coorect
    
    #check wether input coordinates have the same length
    if x_mso_km.size != y_mso_km.size: 
        print('The input arrays do not have the same length. Please make sure that x, y and z array do have the same length.')
        return 0
    
    if x_mso_km.size != z_mso_km.size: 
        print('The input arrays do not have the same length. Please make sure that x, y and z array do have the same length.')
        return 0
    

    #check heliocentric distance (Single Input for all coordinates)
    if isinstance(r_hel_AU, float): 
        if r_hel_AU < 0.3: 
            print('Heliocentric Distance r_hel_AU is too small. Should be between 0.3 and 0.47 AU. ')
            return 0
        if r_hel_AU > 0.47: 
            print('Heliocentric Distance r_hel_AU is too high. Should be between 0.3 and 0.47 AU. ')
            return 0
        
        #print('Type of r_hel is float. Changing to numpy array. ')
        r_hel_tmp = np.ones(x_mso_km.size) * r_hel_AU
        r_hel_AU = r_hel_tmp
        
        
    #check heliocentric distance (Array-Input, there should be one value per coordinate)
                
    if isinstance(r_hel_tmp, np.ndarray): 
        #if there are more 
        if x_mso_km.size != r_hel_AU.size: 
            print('Please enter a single heliocentric distance for all coordinates or an array with \
                  one heliocentric distance value for each coordinate. ')
            return 0 
        
    
        
    #define constants
    R_M = 2440 
    mag_thickness = 266 #paper Heyner 2016
    bs_thickness = 266 # no source, so far: just like mag --> find source! 
    
    #calculate radius
        
    r_mso_km = np.sqrt(x_mso_km**2 + y_mso_km**2 + z_mso_km**2)
    r_mso_RM = r_mso_km / 2440
    
    #transform to msm
    x_msm_km = x_mso_km
    y_msm_km = y_mso_km
    z_msm_km = z_mso_km - 479 #value from Anderson 
    
    r_msm_km = np.sqrt(x_msm_km**2 + y_msm_km**2 + z_msm_km**2)
    r_msm_RM = r_msm_km / 2440    
    
    #define outputs
    region = np.zeros(len(x_mso_km))

    
    def shue_mp_calc_r_mp(x, y, z, RMP, alpha):
    	"""
    	This calculates the magnetopause distance after the Shue et al. magnetopause model
    	for the radial extension of an arbitrary point.
    	
    	x,y,z : coordinates - arbitrary units in MSM coordinate system
    	RMP : subsolar standoff distance - arbitrary units --> result will have the same units
    	alpha : mp flaring parameter
    	
    	return : magnetopause distance w.r.t. planetary center 
    	"""
    	#distance to x-axis
    	rho_x = np.sqrt(y.astype(float)**2 + z.astype(float)**2)
    	#angle with x-axis
    	epsilon = np.arctan2(rho_x.astype(float),x.astype(float))	
    	#Shue's formula
    	mp_distance = RMP * np.power((2. / (1. + np.cos(epsilon))),alpha)
    	
    	return mp_distance
     
    
    #calculate shue magnetosphere
    f_a = 2.14
    f_b = -0.00038
    R_SS =  (f_a + f_b * di) * (r_hel_AU ** (1 / 3)) * R_M

    r_mp_shue = shue_mp_calc_r_mp(x_msm_km, y_msm_km, z_msm_km, R_SS, 0.5) 

    #from Winslow 2012:      
    #formula: sqrt((x-x0)**2 + rho**2) = p*epsilon/(1 + epsilon * cos(theta))
    
# =============================================================================
#   parameters from Winslow 2013
# =============================================================================
    # #best fit conic section
    #x0 = 0.5 
    # p = 3.2 
    #epsilon = 0.
    # #best fit mid-point: 
    x0 = 0.5 
    p = 2.75 
    epsilon = 1.04
    L = p* epsilon    

    x_msm_RM = x_msm_km /R_M
    y_msm_RM = y_msm_km /R_M
    z_msm_RM = z_msm_km /R_M
    
    rho = np.sqrt(y_msm_RM**2 + z_msm_RM**2)
    theta = np.arctan2(rho, x_msm_RM)
    
    rhs =L/(1 + epsilon * np.cos(theta))  #right hand side of equation 3 in Winslow 2012
    
    #Solar Wind
    
    r_BS_msm_RM = rhs
    r_bsc_RM = np.sqrt((x_msm_RM - x0)**2 + y_msm_RM**2  + z_msm_RM**2) #bowshock coordinates
    
    indices_SW = np.where((r_bsc_RM > r_BS_msm_RM) )
    
    #print('indices SW: ', indices_SW)
    region[indices_SW] = 6
    
    #Magnetosheath
    indices_MSH = np.where((r_bsc_RM < r_BS_msm_RM) & (r_msm_km > (r_mp_shue + (1/2 * mag_thickness))))
    region[indices_MSH] = 4

    
    indices_bowshock = np.where((r_bsc_RM < r_BS_msm_RM + (1/2 * mag_thickness/R_M)) & (r_bsc_RM > r_BS_msm_RM - (1/2 * mag_thickness/R_M))) 
    
    region[indices_bowshock] = 5
    
    #indices close to MP/ 'in' in MP
    
    indices_mp = np.where(r_msm_km < (r_mp_shue + (1/2 * mag_thickness)))


        
    region[indices_mp] = 3

    
    #indices inside magnetosphere
    
    indices_mag = np.where(r_msm_km < (r_mp_shue - (1/2 * mag_thickness)))

    region[indices_mag] = 2
 
    #inside planet
    indices_inside_planet = np.where(r_mso_km < 2440)
    region[indices_inside_planet] = 1

    
    #in SW 
        
    return region



    
