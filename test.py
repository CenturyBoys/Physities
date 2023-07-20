
if __name__ == "__main__":
    import definitions
    print(definitions.meters)
    m2 = definitions.meters*definitions.meters
    print(m2)
    table_area = m2*2
    print(table_area)
    table_height = definitions.meters*0.5
    print(table_height)
    table_volume = table_height * table_area
    print(table_volume)
    tables_values = table_volume*3
    print(tables_values)
