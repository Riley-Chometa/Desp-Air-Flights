import pandas as pd
from datetime import datetime

import sys
import os

sys.path.append(os.path.abspath("./scraping/"))
# import harvest_flights as harv
import test as harv

import connect_gdb as conGDB




def update_airport_departures(airport_code, gdb=None):
    """Updates the flights departing from the given airport

    Scrapes flights departing from the airport and adds them to the gdb as relationships

    Args:
        airport_code: String
            airport code of the airport we are adding
        gdb: py2neo Graph
            connection to the neo4j database
    """
    try:
        airport_dept_df = harv.harvest_data_departures(airport_code, None)
    except:
        print("failed to get data for:", airport_code)
        return

    if gdb==None:
        gdb = conGDB.connect_gdb()

    airport_cypher = """MATCH (a:Airport {Code: $Code})-[f:Flight]-(:Airport)
                        DELETE f"""
    gdb.run(airport_cypher, parameters={"Code": airport_code})
    
    flight_Nums = airport_dept_df["Flight"].unique().tolist()

    for flight_Num in flight_Nums:
        flight_df = airport_dept_df[airport_dept_df["Flight"] == flight_Num]
        
        destination_AP = flight_df["Airport Code"].values[0]
        status = flight_df["Status"].values[0]
        carrier = flight_df["Carrier"].values[0]
        # gate = flight_df["Gate"].values[0]
        departTime = flight_df["Departure"].values[0]

        # update destination to airport code instead of city
        parameters = {
            "DepartFrom": str(airport_code),
            "Destination_AP": str(destination_AP),
            "FlightNum": str(flight_Num),
            "Status": str(status),
            "Carrier": str(carrier),
            "DepartTime": departTime
        }
        # "Gate": str(gate)
        print(parameters)

        flight_cypher = """
                        With $flt as flt
                        MATCH (a1:Airport {Code: flt["DepartFrom"]})
                        MATCH (a2:Airport {Code: flt["Destination_AP"]})
                        MERGE (a1)-[f:Flight {FlightNum: flt["FlightNum"]}]->(a2)
                        SET f.Status = flt["Status"]
                        SET f.DepartTime = flt["DepartTime"]
                        SET f.Carrier = flt["Carrier"]
                        SET a1.depUpdated = date()
                        """
        gdb.run(flight_cypher, parameters={"flt": parameters})

    print("Finished added departing flights from", airport_code)

def update_departures():
    """Updates all flights from airports that have not been updated today"""
    
    gdb = conGDB.connect_gdb()

    cypher = """
             MATCH (a:Airport)
             WHERE EXISTS(a.Code) AND
             NOT EXISTS(a.depUpdated) OR 
             a.depUpdated < date() 
             RETURN a.Code as Code
             """

    airport_codes = gdb.run(cypher).to_ndarray()

    # converts the array of airport_codes to a list
    airport_codes = [x[0] for x in airport_codes]

    numOfAirport=len(airport_codes)
    count=0
    for code in airport_codes:
        print(code)
        update_airport_departures(airport_code= str(code), gdb=gdb)
        count+=1
        print(count,"/", numOfAirport)

if __name__ == "__main__":
    # dep_airport = "YEG"
    # update_airport_departures(dep_airport)
    update_departures()
