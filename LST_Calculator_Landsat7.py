"""
  LST CALCULATOR FOR LANDSAT 7
  
  Updated on: 17 September 2022
  Written by HaKaN OGUZ
  Description: This python script retrieves land surface temperature (LST) from Landsat 7 satellite imagery 
"""

import arcpy
from sys import argv

def CalculateLSTfromLandsat7ETM(band4, band3, band6, Lmax_3=152.9, Lmin_3=-5, QCALMAX_3=255, QCALMIN_3=1, Lmax_4=157.4, Lmin_4=-5.1, QCALMAX_4=255, QCALMIN_4=1, Lmax_6=15.303, Lmin_6=1.2378, QCALMAX_6=255, QCALMIN_6=1, ES_Dist=1.0155, Sun_Elevation=59.81, Dark_Obj_DN_Value_for_Band3=9.5, Dark_Obj_DN_Value_for_Band4=7.3, Atmospheric_Transmissivity=0.79, Upwelling=2.43, Downwelling=3.85, LST="C:\\Landsat_8\\LST"):  # Calculate LST from Landsat 7 ETM

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    # Check out any necessary licenses.
    arcpy.CheckOutExtension("spatial")


    # Process: Convert to Radiance for band6 (Raster Calculator) 
    band6_rad = "C:\\Landsat_5\\lst_calculator.gdb\\band6_rad"
    arcpy.gp.RasterCalculator_sa(expression=[Lmax_6, Lmin_6, QCALMAX_6, QCALMIN_6, band6, QCALMIN_6, Lmin_6], output_raster=band6_rad)

    # Process: Convert to Radiance for band4 (Raster Calculator) 
    band4_rad = "C:\\Landsat_5\\lst_calculator.gdb\\band4_rad"
    arcpy.gp.RasterCalculator_sa(expression=[Lmax_4, Lmin_4, QCALMAX_4, QCALMIN_4, band4, QCALMIN_4, Lmin_4], output_raster=band4_rad)

    # Process: Calculate Value for Lh_4 (Calculate Value) 
    Lh_4 = (float(Lm_4) - float(L1per_4))[0]

    # Process: Convert to Reflectance for band4 (Raster Calculator) 
    band4_ref = "C:\\Landsat_5\\lst_calculator.gdb\\band4_ref"
    arcpy.gp.RasterCalculator_sa(expression=[band4_rad, Lh_4, ES_Dist, ES_Dist, Sun_Elevation], output_raster=band4_ref)

    # Process: Convert to Radiance for band3 (Raster Calculator) 
    band3_rad = "C:\\Landsat_5\\lst_calculator.gdb\\band3_rad"
    arcpy.gp.RasterCalculator_sa(expression=[Lmax_3, Lmin_3, QCALMAX_3, QCALMIN_3, band3, QCALMIN_3, Lmin_3], output_raster=band3_rad)

    # Process: Calculate Value for Lh_3 (Calculate Value) 
    Lh_3 = (float(Lm_3) - float(L1per_3))[0]

    # Process: Convert to Reflectance for band3 (Raster Calculator) 
    band3_ref = "C:\\Landsat_5\\lst_calculator.gdb\\band3_ref"
    arcpy.gp.RasterCalculator_sa(expression=[band3_rad, Lh_3, ES_Dist, ES_Dist, Sun_Elevation], output_raster=band3_ref)

    # Process: Calculate NDVI (Raster Calculator) 
    ndvi = "C:\\Landsat_5\\lst_calculator.gdb\\ndvi"
    arcpy.gp.RasterCalculator_sa(expression=[band4_ref, band3_ref, band4_ref, band3_ref], output_raster=ndvi)

    # Process: Correct ndvi (Raster Calculator) 
    correct_ndvi = "C:\\Landsat_5\\lst_calculator.gdb\\correct_ndvi"
    arcpy.gp.RasterCalculator_sa(expression=[ndvi, ndvi, ndvi, ndvi, ndvi], output_raster=correct_ndvi)

    # Process: Calculate Pv (Raster Calculator) 
    Pv = "C:\\Landsat_5\\lst_calculator.gdb\\Pv"
    arcpy.gp.RasterCalculator_sa(expression=[correct_ndvi], output_raster=Pv)

    # Process: Emissivity Calculation (Raster Calculator) 
    emissivity = "C:\\Landsat_5\\lst_calculator.gdb\\emissivity"
    arcpy.gp.RasterCalculator_sa(expression=[correct_ndvi, correct_ndvi, correct_ndvi, correct_ndvi, Pv], output_raster=emissivity)

    # Process: Calculate Lt (Raster Calculator) 
    Lt = "C:\\Landsat_5\\lst_calculator.gdb\\Lt"
    arcpy.gp.RasterCalculator_sa(expression=[band6_rad, Upwelling, Atmospheric_Transmissivity, emissivity, Downwelling, Atmospheric_Transmissivity, emissivity], output_raster=Lt)

    # Process: Calculate LST (Raster Calculator) 
    lst_calc = "C:\\Landsat_5\\lst_calculator.gdb\\lst_calc"
    arcpy.gp.RasterCalculator_sa(expression=[Lt], output_raster=lst_calc)

    # Process: LST in Degree Celsius (Raster Calculator) 
    lst_celsius = "C:\\Landsat_8\\lst_celsius"
    arcpy.gp.RasterCalculator_sa(expression=[lst_calc], output_raster=lst_celsius)

    # Process: Raster Calculator (Raster Calculator) 
    lst_final = "C:\\Landsat_8\\lst_final"
    arcpy.gp.RasterCalculator_sa(expression=[lst_celsius, lst_celsius], output_raster=lst_final)

    # Process: Remove Cloud (Raster Calculator) 
    arcpy.gp.RasterCalculator_sa(expression=[lst_final, lst_final], output_raster=LST)

    # Process: Calculate Value for Lm_3 (Calculate Value) 
    Lm_3 = (float(Lmin_3) + float(Dark_Obj_DN_Value_for_Band3) * ((float(Lmax_3) - float(Lmin_3)) / float(QCALMAX_3)))[0]

    # Process: Calculate Value for L1per_3 (Calculate Value) 
    L1per_3 = (0.01 * math.cos(90 - float(Sun_Elevation)) * 1551) / (3.1416 * float(ES_Dist) * float(ES_Dist))[0]

    # Process: Calculate Value for Lm_4 (Calculate Value) 
    Lm_4 = (float(Lmin_4) + float(Dark_Obj_DN_Value_for_Band4) * ((float(Lmax_4) - float(Lmin_4)) / float(QCALMAX_4)))[0]

    # Process: Calculate Value for L1per_4 (Calculate Value) 
    L1per_4 = (0.01 * math.cos(90 - float(Sun_Elevation)) * 1044) / (3.1416 * float(ES_Dist) * float(ES_Dist))[0]

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"C:\Users\h_ogu\Documents\ArcGIS\Projects\MyProject5\MyProject5.gdb", workspace=r"C:\Users\h_ogu\Documents\ArcGIS\Projects\MyProject5\MyProject5.gdb"):
        CalculateLSTfromLandsat7ETM(*argv[1:])
