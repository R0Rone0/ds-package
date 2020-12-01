########################################
# Helper Functions for Data Science Tasks
# 
# Various functions to make data scientist's lives easier.
# 
# Author: Nick Green
# Contact: green.nick.01@gmail.com
########################################
def reg_bools(data, col, val):
    """Create new columns in dataframe to convert plaintext data to boolean values for regression."""
    data.loc[data[col] == val, val] = '1'
    data.loc[data[col] != val, val] = '0'


def scrape_uniques(data, col):
    """Pulls unique values from a column in a dataframe and stores in list."""
    return data[col].unique()


def composite_overdue(row, composite_list):
    """Creates composite variable that combines multiple number values in a dataframe together. Implement with lambda function."""
    for item in composite_list:
        composite += row[item]
    return composite


def multivar_eq(data, dependent, remove=None):
    """Perform multivariate regression on full dataset and return linear equation."""
    target = pd.DataFrame(data[dependent], columns=[dependent])
    
    if remove is not None:
        data = data.loc[:, data.columns != remove]
    
    X = data.loc[:, data.columns != dependent]
    y = data.loc[:, data.columns == dependent]

    lm = linear_model.LinearRegression()
    model = lm.fit(X,y)

    r_squared = lm.score(X,y)  # returns R^2 value
    coefs = lm.coef_           # returns coefficients
    intercept = lm.intercept_  # returns intercept

    print("R^2 Value: " + str(r_squared))
    print("Equation: " + str(coefs) + " + " + str(intercept))
    
    
def logi_reg(data, dependent):
    """Perform logistic regression on full dataset and return logistic equation."""
    target = pd.DataFrame(data[dependent], columns=[dependent])
    
    X = data.loc[:, data.columns != dependent]
    y = data.loc[:, data.columns == dependent]
    
    lm = linear_model.LogisticRegression()
    model = lm.fit(X,y)
    
    r_squared = lm.score(X,y)  # returns R^2 value
    #coefs = lm.coef_           # returns coefficients
    #intercept = lm.intercept_  # returns intercept

    print("R^2 Value: " + str(r_squared))
    #print("Equation: " + str(coefs) + " + " + str(intercept))
    

def assignment(df, centroids):
    """Assign centroids to cluster groups for K-means clustering algorithm."""
    for i in centroids.keys():
        # sqrt((x1 - x2)^2 - (y1 - y2)^2)
        df['distance_from_{}'.format(i)] = (
            np.sqrt(
                (df['x'] - centroids[i][0]) ** 2
                + (df['y'] - centroids[i][1]) ** 2
            )
        )
    centroid_distance_cols = ['distance_from_{}'.format(i) for i in centroids.keys()]
    df['closest'] = df.loc[:, centroid_distance_cols].idxmin(axis=1)
    df['closest'] = df['closest'].map(lambda x: int(x.lstrip('distance_from_')))
    df['color'] = df['closest'].map(lambda x: colmap[x])
    return df


def update(k):
    """Update centroid position to converge on solution for K-means clustering algorithm."""
    for i in centroids.keys():
        centroids[i][0] = np.mean(df_cluster[df_cluster['closest'] == i]['x'])
        centroids[i][1] = np.mean(df_cluster[df_cluster['closest'] == i]['y'])
    return k