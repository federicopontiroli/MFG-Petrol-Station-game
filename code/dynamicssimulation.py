from scipy.optimize import root_scalar
from scipy.stats import norm
import pandas as pd
import numpy as np

def bestreply(p_1, p0, sigma, alpha, beta, e, delta):

    sigma = max(sigma, 1e-6)

    def equazione(p):
        return (
            -alpha * (1-norm.cdf((p - p0) / sigma))
            + beta * norm.cdf((p - p0) / sigma)
            + e * (p - p_1)
            +delta*p
        )

    sol = root_scalar(
    equazione,
    #bracket=[0, 20],
    x0=p0,
    method='newton'
)

    if sol.converged:
        return sol.root
    else:
        return np.nan



def simulate_model_with_real_data(alpha, beta, eps, delta, sigma_series, df_agents, T, return_all=False):
    """
    Simulates the game starting from the REAL historical prices of individual petrol stations. (Homogeneus players)
    
    Parameters:
    - alpha, beta, eps, delta: Calibrated MFG behavioral parameters.
    - sigma_series: Pandas Series containing the sigma parameter for each station ID.
    - df_agents: Pivot table dataframe (Dates as index, station IDs as columns).
    - T: Total number of time steps (days) to simulate.
    - return_all: If True, returns both the aggregate mean price and individual price trajectories.
    """
    N = df_agents.shape[1]  # Number of petrol stations in the dataset
    
    # Initialize the array for the mean model price (the aggregate price trend)
    model_price = np.zeros(T)
    station_ids = df_agents.columns
    
    # Calculate the observed real mean price for the first 13 days (pre-decree phase)
    real_mean_prices = df_agents.mean(axis=1).values
    model_price[:13] = real_mean_prices[:13]
    
    # Matrix to store individual prices for all players across time
    individual_prices = np.zeros((T, N))
    
    # INITIALIZATION: Set the real prices at day 12 (the 13th day) as the starting point
    # .iloc[12, :] extracts row 12 for all stations
    individual_prices[12, :] = df_agents.iloc[12, :].values

    # Time loop starting from the 14th day (index 13)
    for i in range(13, T):
        prev_mean_price = model_price[i-1]
        
        for j, station_id in enumerate(station_ids):
            sigma = sigma_series.loc[station_id]
            prev_individual_price = individual_prices[i-1, j]
            
            # Each player reacts to the previous regional mean price 
            # and to their own individual price from the previous day
            individual_prices[i, j] = bestreply(
                p_1=prev_individual_price, 
                p0=prev_mean_price, 
                sigma=sigma, 
                alpha=alpha, 
                beta=beta, 
                e=eps, 
                delta=delta
            )
        
        # The new regional mean is the average of the best replies for that day
        model_price[i] = np.nanmean(individual_prices[i, :])
        
    if return_all:
        return model_price, individual_prices

    return model_price

def residui_cluster(params, sigma_series, labels_series, df_agents, T, prezzi_reali, subsample=1):
    """Defines the objective function for optimization, calculating the residuals between the simulated mean price 
    and the real mean price at specific time points."""
    alphas = [params[0], params[4], params[8]]
    betas  = [params[1], params[5], params[9]]
    gammas = [params[2], params[6], params[10]]
    deltas = [params[3], params[7], params[11]]
    
    # Chiamata alla tua funzione di simulazione completa
    y_pred = simulate_cluster_game_complete(
        alphas=alphas, 
        betas=betas, 
        gamma=gammas, # Assicurati che si chiami 'gamma' o 'gammas' coerentemente
        deltas=deltas, 
        sigma_series=sigma_series, 
        labels_series=labels_series, 
        df_agents=df_agents, 
        T=T
    )
    
    return y_pred[13:T:subsample] - prezzi_reali[13:T:subsample]


start_params = [
   3.912, 5.186, 2.021, 2.210,  # Cluster 0
   10.144, 0.562, 7.192, 1.701,  # Cluster 1
   11.191, 0.357, 0.574, 1.654   # Cluster 2
]

res = least_squares(
    residui_cluster, 
    start_params, 
    bounds=([0.1]*12, [100.0]*12),
    #loss='soft_l1',
    #f_scale=0.01,
    args=(sigma_series, labels_series_fixed, df_clean, 70, avg_prices_tr, 4), #you can play freely with different loss functions, number of observations, subsampling of the real time series
    max_nfev=25, 
    verbose=2,
    method='trf'
)