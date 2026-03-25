import os
import argparse
from logger import setupLogger
from pipeline import EcommerceETL

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--orders", default="data/orders.json")
    parser.add_argument("--customers", default="data/customers.csv")
    parser.add_argument("--output", default="output/")

    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))

    orders_path = os.path.join(base_dir,args.orders)
    customers_path = os.path.join(base_dir,args.customers)
    output_path = os.path.join(base_dir,args.output)

    log_file = os.path.join(base_dir,"pipeline.log")
    setupLogger(log_file)

    pipeline = EcommerceETL(
        orders_path,
        customers_path,
        output_path
    )

    pipeline.run_pipeline()

if __name__ == "__main__":
    main()