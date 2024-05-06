from datetime import date  
import pandas as pd
from send_emails import send_email ### import from local directory

### Public Googleheets url 
SHEET_ID = "1EqYv0wVJRVBt6zaMpakCqDuJmY5fVP5kntuNLqL_0QU"
SHEET_NAME = "sheet1"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"



def load_df(url):
    parse_dates = ["due_date", "reminder_date"]
    df = pd.read_csv(url, parse_dates=parse_dates)
    return df


def query_data_and_send_emails(df):
    present = date.today()
    email_counter = 0
    for _, row in df.iterrows():
        if (present >= row["reminder_date"].date()) and (row["has_paid"] == "no"):
            send_email(
                subject=f'[Coding is Fun] Invoice: {row["invoice_no"]}',
                receiver_email=row["email"],
                name=row["name"],
                due_date=row["due_date"].strftime("%d, %b %Y"),
                invoice_no=row["invoice_no"],
                amount=row["amount"],
            )
            email_counter += 1
    return f"Total Emails Sent: {email_counter}"
    
df = load_df(URL)
result = query_data_and_send_emails(df)
print(result)