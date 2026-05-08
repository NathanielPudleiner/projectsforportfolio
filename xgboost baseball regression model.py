# Necessary Package Imports
import warnings
import pandas as pd
import numpy as np
from pybaseball import statcast
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor

def create_stuff_plus_model(start_date='2022-03-01', end_date='2022-10-01', pitch_type='FF'):

    #Checkpoint 1: Data acquisition
    print("Acquiring Statcast data")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        data = statcast(start_dt=start_date, end_dt=end_date)

    numeric_features = [
        'release_speed', 'release_pos_x', 'release_pos_z',
        'pfx_x', 'pfx_z', 'release_extension', 'release_spin_rate',
        'plate_x', 'plate_z', 'spin_axis',
        'vx0', 'vz0', 'ax', 'az',
        'outs_when_up', 'balls', 'strikes',
    ]
    metadata_features = [
        'game_pk', 'pitch_type', 'batter', 'pitcher', 'home_team', 'away_team',
        'stand', 'p_throws', 'game_date', 'inning', 'events',
        'on_1b', 'on_2b', 'on_3b'

    ]
    target = 'delta_run_exp'

    data = data.dropna(subset=numeric_features + [target])


    
    #Checkpoint 2: Data Organization, Preperation, and Scaling
    print("Scaling and Prepping Data")

    X_numeric = data[numeric_features]
    y = data[target]
    X_metadata = data[metadata_features] if all(col in data.columns for col in metadata_features) else None

    X_train, X_test, y_train, y_test = train_test_split(X_numeric, y, test_size=0.2, random_state=42)
    X_train_meta, X_test_meta = train_test_split(X_metadata, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    #Checkpoint 3: Model Training
    print("Training Regression Model")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
        model = XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
        model.fit(X_train_scaled, y_train)

    #Checkpoint 4: Acquisition of mean and std dev for scaling
    print("Acquiring mean and std dev for scaling")
    y_pred_train = model.predict(X_train_scaled)
    mean_pred = np.mean(y_pred_train)
    std_pred = np.std(y_pred_train)

    return model, scaler, mean_pred, std_pred, X_test, X_test_meta
def get_stuff_plus(model, scaler, mean_pred, std_pred, pitch_data):

    #Checkpoint 5: Stuff+ Prep Information
    print("Prepping stuff+ input data")
    scaled_data = scaler.transform(pitch_data)
    predicted_run_values = model.predict(scaled_data)
    stuff_plus_scores = 100 + ((predicted_run_values - mean_pred) / std_pred) * 10
    return stuff_plus_scores

if __name__ == '__main__':
    #Checkpoint 6: Model Building
    print("Building Model")
    trained_model, data_scaler, train_mean_pred, train_std_pred, test_data, test_metadata = create_stuff_plus_model(
        start_date='2022-03-01',
        end_date='2022-10-01',
        pitch_type='FF',
    )

    #Checkpoint 7: Main Calculation Stage
    print("Reached main calculation stage")
    stuff_plus_results = get_stuff_plus(
        trained_model,
        data_scaler,
        train_mean_pred,
        train_std_pred,
        test_data,
    )

    #Checkpoint 8: Post Calculation Stage and Data Output
    print("Reached post calculation stage")
    test_data = test_data.copy()
    test_data['stuff_plus'] = stuff_plus_results
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 0)  # makes columns wrap instead of cutting off
    
    if not test_metadata.empty:
        test_data = pd.concat([test_metadata.reset_index(drop=True), test_data.reset_index(drop=True)], axis=1)

    print("\nStuff+ analysis complete. Here are the top 300 pitches by Stuff+ in the test set:")
    print(test_data.sort_values('stuff_plus', ascending=False).head(300))

    test_data.sort_values('stuff_plus', ascending=False).head(300).to_csv('top_300_stuff_plus.csv', index=False)
    print("Saved top 300 Stuff+ pitches to 'top_300_stuff_plus.csv'")

