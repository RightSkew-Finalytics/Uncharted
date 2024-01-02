import csv
import yfinance as yf
import datetime as dt
import pandas_ta as ta




input_file = "fo090623.csv"
output_file = "CPR_MACD.csv"

threshold = input("Do you want to change the default threshold of 0.25(press enter to skip) : ")

if threshold == '' :
    #Default threshold
    threshold = 0.25
else:
    threshold = float(threshold)

def calculate_cpr(row):
    try:
        high = float(row["HIGH_PRICE"])
    except :
        high = 0
    try:
        low = float(row["LOW_PRICE"])
    except :
        low = 0
    try:
        close = float(row["CLOSE_PRIC"])
    except :
        close = 0
    
    pivot = (high + low + close) / 3
    bottom_cpr = (high + low) / 2
    top_cpr = (pivot - bottom_cpr) + pivot

    if (top_cpr<=bottom_cpr) :
        bottom_cpr,top_cpr = top_cpr,bottom_cpr
    
    momentum_of_stock = "High" if abs(bottom_cpr - top_cpr) < threshold else "Low"
    
    return round(pivot,2), round(bottom_cpr,2), round(top_cpr,2), momentum_of_stock

def calculate_macd(symbol):
    # Request historic pricing data via finance.yahoo.com API
    df = yf.Ticker(symbol).history(period='3y')[['Close', 'Open', 'High', 'Volume', 'Low']]
    # Calculate MACD values using the pandas_ta library
    df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)
    macd = (round(df['MACD_12_26_9'].iloc[-2],2),round(df['MACDs_12_26_9'].iloc[-2],2),round(df['MACDh_12_26_9'].iloc[-2],2),round(df['MACDh_12_26_9'].iloc[-3],2))
    print (macd)
    return macd



def get_sector(stock_symbol):
    stock_info = yf.Ticker(stock_symbol).info
    return stock_info.get("sector", "Unknown")

with open(input_file, "r") as input_csv:
    csv_reader = csv.DictReader(input_csv)
    
    with open(output_file, "w", newline="") as output_csv:
        csv_writer = csv.writer(output_csv)
        csv_writer.writerow(["SYMBOL", "SECTOR", "PIVOT", "BOTTOMCPR", "TOPCPR", "MOMENTUMOFSTOCK","DIRECTION"])
        
        sector_momentum = {}
        
        for row in csv_reader:
            stock_symbol = row["CONTRACT_D"][6:][-12::-1][::-1] + ".NS"
            pivot, bottom_cpr, top_cpr, momentum_of_stock = calculate_cpr(row)
            
            try :
                sector = get_sector(stock_symbol)
                macd = calculate_macd(stock_symbol)
                if macd[0] > macd[1]  and macd[2] > macd[3] and momentum_of_stock == "High":
                    direction = "Strong Uptrend"
                elif macd[0] > macd[1]  and macd[2] < macd[3] and momentum_of_stock == "Low":
                    direction = "Weak Uptrend"
                elif macd[0] < macd[1]  and macd[2] > macd[3] and momentum_of_stock == "High":
                    direction = "Strong Downtrend"
                elif macd[0] < macd[1]  and macd[2] < macd[3] and momentum_of_stock == "Low":
                    direction = "Weak Downtrend"
                else :
                    direction = "No trend"
            except : 
                print("hi")
                continue

            # Calculate sector momentum count
            if sector not in sector_momentum:
                sector_momentum[sector] = {"High": 0, "Low": 0, "AVGCPR":0}
            sector_momentum[sector][momentum_of_stock] += 1
            sector_momentum[sector]["AVGCPR"] += abs(bottom_cpr - top_cpr)
            csv_writer.writerow([stock_symbol, sector, pivot, bottom_cpr, top_cpr, momentum_of_stock,direction])
            print (stock_symbol, sector, pivot, bottom_cpr, top_cpr, momentum_of_stock,direction)

# Sort sectors based on highest movement (narrow CPR)
for i in sector_momentum.keys() :
    sector_momentum[i]["AVGCPR"] = round(sector_momentum[i]["AVGCPR"]/(sector_momentum[i]["High"]+ sector_momentum[i]["Low"]) ,2)
    sector_momentum[i]["SECM"] = "High" if sector_momentum[i]["AVGCPR"] < threshold else "Low"
sectors_sorted = sorted(sector_momentum.items(), key=lambda x: x[1]["High"], reverse=True)
print (sectors_sorted)

print("\nSectors sorted based on highest movement (narrow CPR):")
for i, (sector, momentum_count) in enumerate(sectors_sorted, 1):
    print(f"{i}. {sector} - High: {momentum_count['High']}, Low: {momentum_count['Low']}, Average CPR width: {momentum_count['AVGCPR']}, Sector Momentum: {momentum_count['SECM']}")