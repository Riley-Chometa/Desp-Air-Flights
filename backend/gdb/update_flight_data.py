import pandas as pd

import sys
import os

sys.path.append(os.path.abspath("./scraping/"))
import harvest_flights as harv

import connect_gdb as conGDB


def update_departing_flights(airport):
    airport_dept_df = harv.harvest_data_departures(airport)

    gdb = conGDB.connect_gdb()

    airport_cypher = f"""MERGE (:Airport {{City: "{airport}"}})"""
    gdb.run(airport_cypher)
    
    flight_Nums = airport_dept_df["Flight"].unique().tolist()

    for flight_Num in flight_Nums:
        flight_df = airport_dept_df[airport_dept_df["Flight"] == flight_Num]
        
        destination = flight_df["Destination"].values[0]
        status = flight_df["Status"].values[0]
        carrier = flight_df["Carrier"].values[0]
        gate = flight_df["Gate"].values[0]

        props = {
            "Destination":destination,
            "FlightNum": flight_Num,
            "Status": status,
            "Carrier": carrier,
            "Gate": gate
        }

        flight_cypher = f"""
                        With $flt as flt
                        MATCH (a1:Airport {{City: "{airport}"}})
                        MERGE (a2:Airport {{City: flt["Destination"]}})
                        MERGE (a1)-[f:Flight {{FlightNum: flt["FlightNum"]}}]->(a2)
                        SET f = flt
                        """
        gdb.run(flight_cypher, parameters={"flt": props})

    print("Finished added departing flights from", airport)

if __name__ == "__main__":
    dep_airport = "Calgary"
    update_departing_flights(dep_airport)
