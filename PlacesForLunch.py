import pandas as pd
from random import randint

PlacesForLunchFile= pd.read_csv("PlacesLunch-Sheet1.csv")
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
print("-", Suggestion)

for i in range(2):
    NotDifferent=True
    while(NotDifferent):
        Suggestion=ListPlaces[randint(0, len(ListPlaces)-1)]
        if prevSug!=Suggestion:
            print("-", Suggestion)
            prevSug=Suggestion
            NotDifferent=False
        else:
            NotDifferent=True
