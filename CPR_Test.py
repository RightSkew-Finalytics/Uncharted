import csv

input_file = "cm19MAY2023bhav.csv"
output_file = "CPR.csv"


threshold = input("Do you want to change the default threshold of 0.25(press enter to skip) : ")

if threshold == '' :
    #Default threshold
    threshold = 0.25

# Function to calculate pivot, bottom CPR, top CPR, and momentum of the stock
def calculate_cpr(row):
    high = float(row["HIGH"])
    low = float(row["LOW"])
    close = float(row["CLOSE"])
    
    pivot = (high + low + close) / 3
    bottom_cpr = (high + low) / 2
    top_cpr = (pivot - bottom_cpr) + pivot
    
    # Calculate the momentum of stock based on the threshold (absolute difference between bottom_cpr and top_cpr)

    momentum_of_stock = "High" if abs(bottom_cpr - top_cpr) < threshold else "Low"
    
    return round(pivot,2) , round (bottom_cpr,2), round (top_cpr,2) , momentum_of_stock


# Read the stock data from NSEINDIA file
with open(input_file, "r") as input_csv:
    csv_reader = csv.DictReader(input_csv)
    
    # Write the output CPR values and momentum of each stock
    with open(output_file, "w", newline="") as output_csv:
        csv_writer = csv.writer(output_csv)
        csv_writer.writerow(["SYMBOL", "PIVOT", "BOTTOMCPR", "TOPCPR", "MOMENTUMOFSTOCK"])
        
        for row in csv_reader:
            pivot, bottom_cpr, top_cpr, momentum_of_stock = calculate_cpr(row)
            csv_writer.writerow([row["SYMBOL"], pivot, bottom_cpr, top_cpr, momentum_of_stock])
