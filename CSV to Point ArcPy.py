import arcpy
import os
from csv import reader


def main():

    # Get user inputs
    sr = arcpy.GetParameterAsText(0)
    infile = arcpy.GetParameterAsText(1)
    gdb_location = arcpy.GetParameterAsText(2)
    fc = arcpy.GetParameterAsText(3)

    # Set workspace
    arcpy.env.workspace = gdb_location

    # Create feature class
    arcpy.management.CreateFeatureclass(gdb_location, fc, 'POINT', "", "", "", sr)

    # Declare fields
    fields = ['SHAPE@XY', 'SCHOOLNAME', 'ADDRESS', 'CITY', 'STATE']

    # Add fields
    arcpy.management.AddField(fc, 'SCHOOLNAME', 'TEXT', "", "", 50)
    arcpy.management.AddField(fc, 'ADDRESS', 'TEXT', "", "", 35)
    arcpy.management.AddField(fc, 'CITY', 'TEXT', "", "", 17)
    arcpy.management.AddField(fc, 'STATE', 'TEXT', "", "", 2)

    # Declare cursor
    cursor = arcpy.da.InsertCursor(os.path.join(gdb_location, fc), fields)

    # Read from CSV file
    with open(infile, 'r') as read_obj:
        csv_reader = reader(read_obj)
        # Skip first line
        next(csv_reader)
        # Make list from csv
        list_rows = list(csv_reader)
        # Iterate through each row and add those that don't start with a '#' to the feature class
        for row in list_rows:
            g = row[0]
            if g.startswith("#"):
                continue
            else:
                feature = arcpy.Point(float(row[2]), float(row[1]))
                pnt_geometry = arcpy.PointGeometry(feature, sr)
                f = (pnt_geometry, row[3], row[4], row[5], row[6])
                cursor.insertRow(f)


if __name__ == '__main__':
   main()
