This is a region prediction tool for Mercury's (magnetic) environment. 

Planetary radius: 2440 km 

Magnetopause: Shue-Model, depends on r_hel and di, parameters like in Pump et al. (2024) 

Bow Shock: conic section from Winslow et al. (2013). Does NOT depend on r_hel or di (yet).

# Input: 
coordinates in MSO in km (x, y, z) 

heliocentric distance r_hel in AU 

(optional: Disturbance Index di (value between 0 and 100)) 

# output: 
number for each coordinate 

1: Mercury (inside planet) 

2: Magnetosphere

3: Magnetopause

4: Magnetosheath

5: Bow Shock

6: Solar Wind 



0: no detection possible 

# Example

example file: example_region_prediction_mercury_simple.py 

 

If you have any questions, do not hesitate to contact me: k.pump@tu-bs.de 
