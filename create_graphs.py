import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.svm import SVR
from sklearn.model_selection import train_test_split

GNI = pd.read_csv("newdata/gni.csv")
GNI = GNI.dropna(axis='index')
def cov(x, y):
    N = x.shape[0]
    meanX = np.mean(x)
    meanY = np.mean(y)
    total = 0
    for i in range(N):
        total += (x[i]-meanX)*(y[i]-meanY)
    return total/N

def corr(x, y):
    covariance = cov(x,y)
    return covariance/(np.std(x) * np.std(y))

def create_graph(x, y, x_label, y_label, show=False, C=200, figsize=(16,9)):
    plt.figure(figsize=figsize)
    model = SVR(kernel='rbf', C=C)
    X = np.array(x).reshape(-1,1)
    y = np.array(y)
    plt.scatter(x, y)
    plt.plot(np.sort(x), model.fit(X, y).predict(np.sort(X, axis=0)), color="black")
    plt.title(x_label + " vs. " + y_label + "\nCorrelation: " + str(corr(np.array(x),y)))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend(["Regression", "Data Points"])
    plt.tight_layout()
    plt.savefig("graphs/"+ x_label + " vs. " + y_label + ".jpg")
    if show:
        plt.show()

# Create Carbon Dioxide graph
owid_df = pd.read_csv("newdata/owid.csv")
owid_df = owid_df.dropna(axis='index')
owid_x = []
owid_y = []
for code in GNI["Country Code"]:
    if any(owid_df["iso_code"] == code):
        owid_x.append(GNI.loc[GNI["Country Code"] == code]["GNI per capita, PPP (current international $)"].item())
        owid_y.append(owid_df.loc[owid_df["iso_code"] == code]["co2_per_capita"].item())
create_graph(owid_x, owid_y, "CO2 per Capita (tonnes)", "GNI per capita, PPP (current international $)",
             C=1000, figsize=(8,5))

# Create Municipal Waste graph
waste_df = pd.read_csv("newdata/waste.csv")
waste_df = waste_df.dropna(axis='index')
pop_df = pd.read_csv("newdata/pop.csv")
pop_df = pop_df.dropna(axis='index')
waste_x = []
waste_y = []
for code in GNI["Country Code"]:
    if any(waste_df["Country Code"] == code) and any(pop_df["Country Code"] == code):
        waste_x.append(GNI.loc[GNI["Country Code"] == code]["GNI per capita, PPP (current international $)"].item())
        waste_y.append(waste_df.loc[waste_df["Country Code"]==code]["Total Waste (tons)"].item() /
                       pop_df.loc[pop_df["Country Code"]==code]["Population"].item())
create_graph(waste_x, waste_y, "Municipal Waste per capita (tons)", "GNI per capita, PPP (current international $)",
             C=.25, figsize=(8,5))