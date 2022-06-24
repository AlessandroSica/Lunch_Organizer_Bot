import pandas as pd
from random import randint

PlacesForLunchFile= pd.read_csv("LunchPlaces-info-Sheet1.csv")
print(PlacesForLunchFile)
print("")

ListPlaces=[]
for i in range(len(PlacesForLunchFile)):
    for j in range(PlacesForLunchFile.loc[i].at["Votes"]):
        ListPlaces+=[PlacesForLunchFile.loc[i].at["Name"]]
print(ListPlaces)
print("")

print("The suggestion of the day:")
Suggestion=ListPlaces[randint(0, len(ListPlaces)-1)]
prevSug=Suggestion
#print(PlacesForLunchFile.iloc[Row])

def PrintInfo():
    for i in range(len(PlacesForLunchFile)):
        if Suggestion==PlacesForLunchFile.loc[i].at["Name"]:
            Row=i
    print(PlacesForLunchFile.loc[Row].at["Name"])
    print(PlacesForLunchFile.loc[Row].at["Rating"], PlacesForLunchFile.loc[Row].at["Stars"], PlacesForLunchFile.loc[Row].at["Reviews"])
    print(PlacesForLunchFile.loc[Row].at["Description"])
    print(PlacesForLunchFile.loc[Row].at["Vegan "], PlacesForLunchFile.loc[Row].at["Vegeterian"])
    print(PlacesForLunchFile.loc[Row].at["Delivery"])
    print(PlacesForLunchFile.loc[Row].at["Take-Away"])
    print(PlacesForLunchFile.loc[Row].at["Distance"])
    print(PlacesForLunchFile.loc[Row].at["Price range"])
    print("")
PrintInfo()

for i in range(2):
    NotDifferent=True
    while(NotDifferent):
        Suggestion=ListPlaces[randint(0, len(ListPlaces)-1)]
        if prevSug!=Suggestion:
            PrintInfo()
            prevSug=Suggestion
            NotDifferent=False
