import pandas as pd
import logging
import os
import json

class EcommerceETL:
    def __init__(self, orders_path: str, customers_path: str, output_dir: str) -> None:
        self.orders_path = orders_path
        self.customers_path = customers_path
        self.output_dir = output_dir
        self.result = None
        self.logger = logging.getLogger("pipeline")
    
    #---------- EXTRACT ----------
    def extract(self):
        """Reads input data from CSV and JSON files."""
        self.logger.info("Extraction Started")

        orders = pd.read_json(self.orders_path)
        customers = pd.read_csv(self.customers_path)

        return orders,customers

    #---------- TRANSFORM ----------
    def transform(self, orders: pd.DataFrame, customers: pd.DataFrame):
        self.logger.info("Transformation Started")

        total_rows = len(orders)

        #Clean orders
        invalid_orders = orders[orders["amount"].isnull()]
        orders = orders[orders["amount"].notnull()]

        #Clean customers
        customers["name"] = customers["name"].fillna("").astype(str)
        invalid_customers = customers[customers["name"].str.strip() == ""]
        customers = customers[customers["name"].str.strip() != ""]

        #Log dropped rows
        self.logger.warning(f"Dropped {len(invalid_orders)} invalid orders (null amount)")
        self.logger.warning(f"Dropped {len(invalid_customers)} invalid customers (empty name)")

        #Join
        df = orders.merge(customers, on="customer_id", how="left")

        #Drop rows where join failed(no customer match)
        df = df.dropna(subset=["name"])

        #Aggregation 1: Daily Sales
        sales = (
            df.groupby("date", as_index=False)
            .agg(
                total_sales = ("amount","sum"),
                order_count = ("order_id","count")
            )
        )

        #Aggregation 2: Customer Spend
        customer_metrics = (
            df.groupby(["customer_id","name"],as_index=False)
            .agg(total_spend = ("amount","sum"))
        )

        valid_rows = len(df)
        invalid_rows = total_rows - valid_rows

        self.logger.info(f"Total Rows: {total_rows}")
        self.logger.info(f"Transformed Rows: {valid_rows}")
        self.logger.info(f"Dropped Rows: {invalid_rows}")

        quality_report ={
            "total_rows": int(total_rows),
            "valid_rows": int(valid_rows),
            "invalid_rows": int(invalid_rows)
        }

        return sales, customer_metrics, quality_report
    
    #---------- LOAD ----------
    def load(self,df_sales: pd.DataFrame, df_customer: pd.DataFrame):
        self.logger.info("Saving Outputs")

        #Ensure output directory exists
        os.makedirs(self.output_dir,exist_ok=True)

        #Save sales Data
        sales_path = os.path.join(self.output_dir,"sales.csv")
        df_sales.to_csv(sales_path, index=False)

        #Save Customer Metrics
        customer_path = os.path.join(self.output_dir,"customer_metrics.csv")
        df_customer.to_csv(customer_path, index=False)

        self.logger.info(f"Transformed Sales Data saved -> {sales_path}")
        self.logger.info(f"Transformed Customer Metrics saved -> {customer_path}")
    
    #---------- RUN ----------
    def run_pipeline(self):
        self.logger.info("Pipeline Started")

        orders,customers = self.extract()
        df_sales,df_customers,quality = self.transform(orders,customers)
        self.load(df_sales,df_customers)

        #Saving Quality Report
        quality_path = os.path.join(self.output_dir,"data_quality.json")
        with open(quality_path,"w") as f:
            json.dump(quality, f, indent=4)
        
        self.logger.info(f"Saved Data Quality report -> {quality_path}")
        self.logger.info("Pipeline Completed")