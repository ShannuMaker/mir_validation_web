import flet as ft
import urllib.request
import json
import psycopg2

# Helper to create a result row
def create_result_row(key, value):
    return ft.Row(
        controls=[
            ft.Text(f"{key}:", width=150, text_align="right"),
            ft.TextField(value=str(value), read_only=True, expand=True),
        ],
    )

def fetch_data(query,params: dict, result_column, result_placeholder):
    try:
        # Using 'with' for automatic resource cleanup
        with psycopg2.connect(
            dbname="upag_db",
            user="upagadmin",
            password="rK9tyiTHv7A7DWPta3pQ",
            host="10.128.23.18",  # or your DB host
            port="6728"
        ) as conn:
            query='''select * from reporting.get_data(%s);'''
            print(query)
            print(params)
            with conn.cursor() as cursor:
                cursor.execute(query, (json.dumps(params),))
                rows = cursor.fetchall()
                print(rows)
                # Convert result to list of dictionaries
                column_names = [desc[0] for desc in cursor.description]
                json_data = [{column_names[i]: row[i] for i in range(len(row))} for row in rows]
                
                print(json_data)
                json_data = [json_data[0]['get_data']]
                print(json_data)
                result_column.controls.clear()
                result_placeholder.value = ""
                
                # Assuming the function returns a JSON string
                # json_data = json.loads(rows[0])

                if not json_data:
                    result_placeholder.value = "No data found"
                    return

                

                for record in json_data:
                    if isinstance(record, dict):
                        for key, val in record.items():
                            result_column.controls.append(create_result_row(key, val))

    except Exception as e:
        result_placeholder.value = f"Error1: {e}"


# # Fetch data with dynamic API URL
# def fetch_data(api_link, params, result_column, result_placeholder):
#     try:
#         headers = {"Content-Type": "application/json"}
#         data = json.dumps(params).encode("utf-8")

#         request = urllib.request.Request(api_link, data=data, headers=headers, method="POST")
#         with urllib.request.urlopen(request) as response:
#             response_data = json.loads(response.read().decode())

#         json_data = response_data.get("result", [])

#         result_column.controls.clear()
#         result_placeholder.value = ""

#         if not json_data:
#             result_placeholder.value = "No data found"
#             return

#         for record in json_data[0]:
#             if isinstance(record, dict):
#                 for key, val in record.items():
#                     result_column.controls.append(create_result_row(key, val))

#     except Exception as e:
#         result_placeholder.value = f"Error: {e}"

# Each screen as a Flet View with api_link passed
def apy_screen(page, api_link):
    crop_name = ft.TextField(label="Crop Name (default: Rice)")
    crop_year = ft.TextField(label="Crop Year Code (default: 2025)")
    estimation = ft.TextField(label="Estimation Cycle Code")
    metric = ft.TextField(label="Metric Name")
    uom = ft.TextField(label="Unit of Measure (default: Tonnes)")

    result_placeholder = ft.Text("Result will appear here")
    result_column = ft.Column()

    def on_fetch(e):
        params = {
            "crop_name": crop_name.value or "Rice",
            "crop_year_code": crop_year.value or "2025",
            "estimation_cycle_code": estimation.value,
            "metric_name": metric.value,
            "unit_of_measure": uom.value or "Tonnes",
            "source_name": "APY"
        }
        fetch_data(api_link, params, result_column, result_placeholder)
        page.update()

    return ft.Column(
        scroll="auto",
        controls=[
            crop_name, crop_year, estimation, metric, uom,
            ft.ElevatedButton("Fetch APY Data", on_click=on_fetch),
            result_placeholder,
            result_column,
        ]
    )

def dgcis_screen(page, api_link):
    crop_name = ft.TextField(label="Crop Name (default: Rice)")
    financial_year_code = ft.TextField(label="Financial Year Code (default: 2025)")
    start_year_month_code = ft.TextField(label="Start Year Month (default: 202404)")
    end_year_month_code = ft.TextField(label="End Year Month (default: 202502)")
    metric = ft.TextField(label="Metric Name")
    uom = ft.TextField(label="Unit of Measure (default: 6)")
    country = ft.TextField(label="Country (Optional)")
    hscode = ft.TextField(label="HSCode (Optional)")

    result_placeholder = ft.Text("Result will appear here")
    result_column = ft.Column()

    def on_fetch(e):
        params = {
            "crop_name": crop_name.value or "Rice",
            "financial_year_code": financial_year_code.value or "2025",
            "start_year_month_code": start_year_month_code.value,
            "end_year_month_code": end_year_month_code.value,
            "metric_name": metric.value,
            "unit_of_measure": uom.value,
            "country":country.value,
            "hscode":hscode.value,
            "source_name": "DGCIS"
        }
        fetch_data(api_link, params, result_column, result_placeholder)
        page.update()

    return ft.Column(
        scroll="auto",
        controls=[
            crop_name, financial_year_code, start_year_month_code, end_year_month_code, metric, uom,country,hscode,
            ft.ElevatedButton("Fetch DGCIS Data", on_click=on_fetch),
            result_placeholder,
            result_column,
        ]
    )

def wc_screen(page, api_link):
    crop_name = ft.TextField(label="Crop Name (default: Rice)")
    start_year_month_code = ft.TextField(label="Start Year Month (default: 202404)")
    metric = ft.TextField(label="Metric Name")

    result_placeholder = ft.Text("Result will appear here")
    result_column = ft.Column()

    def on_fetch(e):
        params = {
            "crop_name": crop_name.value or "Rice",
            "start_year_month_code": start_year_month_code.value,
            "metric_name": metric.value,
            "source_name": "WC"
        }
        fetch_data(api_link, params, result_column, result_placeholder)
        page.update()

    return ft.Column(
        scroll="auto",
        controls=[
            crop_name, start_year_month_code, metric,
            ft.ElevatedButton("Fetch WPI & CPI Data", on_click=on_fetch),
            result_placeholder,
            result_column,
        ]
    )

def apat_screen(page, api_link):
    crop_name = ft.TextField(label="Crop Name (default: Rice)")
    start_year_month_code = ft.TextField(label="Start Year Month (default: 202404)")
    frequency = ft.TextField(label="Frequency")

    result_placeholder = ft.Text("Result will appear here")
    result_column = ft.Column()

    def on_fetch(e):
        params = {
            "crop_name": crop_name.value or "Rice",
            "start_year_month_code": start_year_month_code.value,
            "frequency": frequency.value,
            "source_name": "APAT"
        }
        fetch_data(api_link, params, result_column, result_placeholder)
        page.update()

    return ft.Column(
        scroll="auto",
        controls=[
            crop_name, start_year_month_code, frequency,
            ft.ElevatedButton("Fetch APAT Data", on_click=on_fetch),
            result_placeholder,
            result_column,
        ]
    )

def calculator_screen(page, api_link):
    current_value = ft.TextField(label="Current Value")
    past_value = ft.TextField(label="Past Value")
    number_of_years = ft.TextField(label="Number of Years")

    result_placeholder = ft.Text("Result will appear here")
    result_column = ft.Column()

    def on_fetch(e):
        params = {
            "current_value": current_value.value,
            "past_value": past_value.value,
            "number_of_years": number_of_years.value,
            "source_name": "Calculator"
        }
        fetch_data(api_link, params, result_column, result_placeholder)
        page.update()

    return ft.Column(
        scroll="auto",
        controls=[
            current_value, past_value, number_of_years,
            ft.ElevatedButton("Fetch Calculated Data", on_click=on_fetch),
            result_placeholder,
            result_column,
        ]
    )

def fci_procurement_screen(page, api_link):
    crop_name = ft.TextField(label="Crop Name")
    state_name = ft.TextField(label="State Name")
    season_name = ft.TextField(label="Season Name")
    year = ft.TextField(label="Year")

    result_placeholder = ft.Text("Result will appear here")
    result_column = ft.Column()

    def on_fetch(e):
        params = {
            "crop_name": crop_name.value,
            "statename": state_name.value,
            "year": year.value,
            "season":season_name.value,
            "source_name": "FCI Procurement"
        }
        fetch_data(api_link, params, result_column, result_placeholder)
        page.update()

    return ft.Column(
        scroll="auto",
        controls=[
            crop_name, state_name, season_name,year,
            ft.ElevatedButton("Fetch Calculated Data", on_click=on_fetch),
            result_placeholder,
            result_column,
        ]
    )


def fci_stock_screen(page, api_link):
    crop_name = ft.TextField(label="Crop Name (default: Rice)")
    start_year_month_code = ft.TextField(label="Start Year Month (default: 202404)")

    result_placeholder = ft.Text("Result will appear here")
    result_column = ft.Column()

    def on_fetch(e):
        params = {
            "crop_name": crop_name.value or "Rice",
            "start_year_month_code": start_year_month_code.value,
            "source_name": "FCI Stock"
        }
        fetch_data(api_link, params, result_column, result_placeholder)
        page.update()

    return ft.Column(
        scroll="auto",
        controls=[
            crop_name, start_year_month_code,
            ft.ElevatedButton("Fetch Calculated Data", on_click=on_fetch),
            result_placeholder,
            result_column,
        ]
    )

def international_prices_screen(page, api_link):
    crop_name = ft.TextField(label="Crop Name (default: Rice)")
    start_year_month_code = ft.TextField(label="Start Year Month (default: 202404)")

    result_placeholder = ft.Text("Result will appear here")
    result_column = ft.Column()

    def on_fetch(e):
        params = {
            "crop_name": crop_name.value or "Rice",
            "start_year_month_code": start_year_month_code.value,
            "source_name": "International Prices"
        }
        fetch_data(api_link, params, result_column, result_placeholder)
        page.update()

    return ft.Column(
        scroll="auto",
        controls=[
            crop_name, start_year_month_code,
            ft.ElevatedButton("Fetch Calculated Data", on_click=on_fetch),
            result_placeholder,
            result_column,
        ]
    )

def global_production_screen(page, api_link):
    crop_name = ft.TextField(label="Crop Name (default: Rice)")
    year = ft.TextField(label="Year")

    result_placeholder = ft.Text("Result will appear here")
    result_column = ft.Column()

    def on_fetch(e):
        params = {
            "crop_name": crop_name.value or "Rice",
            "year": year.value,
            "source_name": "Global Production"
        }
        fetch_data(api_link, params, result_column, result_placeholder)
        page.update()

    return ft.Column(
        scroll="auto",
        controls=[
            crop_name, year,
            ft.ElevatedButton("Fetch Calculated Data", on_click=on_fetch),
            result_placeholder,
            result_column,
        ]
    )
def state_level_prices_screen(page, api_link):
    crop_name = ft.TextField(label="Crop Name (default: Rice)")
    state_name = ft.TextField(label="State Name")
    start_year_month_code = ft.TextField(label="Start Year Month (default: 202404)")

    result_placeholder = ft.Text("Result will appear here")
    result_column = ft.Column()

    def on_fetch(e):
        params = {
            "crop_name": crop_name.value or "Rice",
            "statename":state_name.value,
            "start_year_month_code": start_year_month_code.value,
            "source_name": "State Level Prices"
        }
        fetch_data(api_link, params, result_column, result_placeholder)
        page.update()

    return ft.Column(
        scroll="auto",
        controls=[
            crop_name, state_name,start_year_month_code,
            ft.ElevatedButton("Fetch Calculated Data", on_click=on_fetch),
            result_placeholder,
            result_column,
        ]
    )
def nafed_procurement_screen(page, api_link):
    crop_name = ft.TextField(label="Crop Name")
    state_name = ft.TextField(label="State Name")
    scheme = ft.TextField(label="Scheme")
    year = ft.TextField(label="Year")

    result_placeholder = ft.Text("Result will appear here")
    result_column = ft.Column()

    def on_fetch(e):
        params = {
            "crop_name": crop_name.value,
            "statename": state_name.value,
            "year": year.value,
            "scheme":scheme.value,
            "source_name": "NAFED Procurement"
        }
        fetch_data(api_link, params, result_column, result_placeholder)
        page.update()

    return ft.Column(
        scroll="auto",
        controls=[
            crop_name, state_name, scheme,year,
            ft.ElevatedButton("Fetch Calculated Data", on_click=on_fetch),
            result_placeholder,
            result_column,
        ]
    )

def nafed_stock_screen(page, api_link):
    crop_name = ft.TextField(label="Crop Name")
    state_name = ft.TextField(label="State Name")
    scheme = ft.TextField(label="Scheme")
    year = ft.TextField(label="Year")

    result_placeholder = ft.Text("Result will appear here")
    result_column = ft.Column()

    def on_fetch(e):
        params = {
            "crop_name": crop_name.value,
            "statename": state_name.value,
            "year": year.value,
            "scheme":scheme.value,
            "source_name": "NAFED Stock"
        }
        fetch_data(api_link, params, result_column, result_placeholder)
        page.update()

    return ft.Column(
        scroll="auto",
        controls=[
            crop_name, state_name, scheme,year,
            ft.ElevatedButton("Fetch Calculated Data", on_click=on_fetch),
            result_placeholder,
            result_column,
        ]
    )
    
    
def fao_screen(page, api_link):
    start_year_month_code = ft.TextField(label="Start Year Month (default: 202404)")

    result_placeholder = ft.Text("Result will appear here")
    result_column = ft.Column()

    def on_fetch(e):
        params = {
            "start_year_month_code": start_year_month_code.value,
            "source_name": "FAO"
        }
        fetch_data(api_link, params, result_column, result_placeholder)
        page.update()

    return ft.Column(
        scroll="auto",
        controls=[
            start_year_month_code,
            ft.ElevatedButton("Fetch Calculated Data", on_click=on_fetch),
            result_placeholder,
            result_column,
        ]
    )

def cfpi_screen(page, api_link):
    start_year_month_code = ft.TextField(label="Start Year Month (default: 202404)")

    result_placeholder = ft.Text("Result will appear here")
    result_column = ft.Column()

    def on_fetch(e):
        params = {
            "start_year_month_code": start_year_month_code.value,
            "source_name": "CFPI"
        }
        fetch_data(api_link, params, result_column, result_placeholder)
        page.update()

    return ft.Column(
        scroll="auto",
        controls=[
            start_year_month_code,
            ft.ElevatedButton("Fetch Calculated Data", on_click=on_fetch),
            result_placeholder,
            result_column,
        ]
    )





# Home screen to accept API link
def home_screen(page, set_api_link):
    api_input = ft.TextField(label="Enter API Link", width=500)
    status_text = ft.Text()

    def on_submit(e):
        if api_input.value:
            set_api_link(api_input.value)
        else:
            status_text.value = "API Link is required!"
        page.update()

    return ft.Column(
        controls=[
            api_input,
            ft.ElevatedButton("Continue", on_click=on_submit),
            status_text,
        ]
    )

# Main function with page navigation
def main(page: ft.Page):
    page.title = "Crop Data Fetcher"
    page.scroll = "auto"

    def load_tabs(api_link):
        page.controls.clear()
        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(text="APY", content=apy_screen(page, api_link)),
                ft.Tab(text="DGCIS", content=dgcis_screen(page, api_link)),
                ft.Tab(text="WPI/CPI", content=wc_screen(page, api_link)),
                ft.Tab(text="APAT", content=apat_screen(page, api_link)),
                ft.Tab(text="Calculator", content=calculator_screen(page, api_link)),
                ft.Tab(text="FCI Procurement", content=fci_procurement_screen(page, api_link)),
                ft.Tab(text="FCI STOCK", content=fci_stock_screen(page, api_link)),
                ft.Tab(text="International Prices", content=international_prices_screen(page, api_link)),
                ft.Tab(text="Global Production", content=global_production_screen(page, api_link)),
                ft.Tab(text="State Prices", content=state_level_prices_screen(page, api_link)),
                ft.Tab(text="NAFED Procurement", content=nafed_procurement_screen(page, api_link)),
                ft.Tab(text="NAFED Stock", content=nafed_stock_screen(page, api_link)),
                ft.Tab(text="FAO", content=fao_screen(page, api_link)),
                ft.Tab(text="CFPI", content=cfpi_screen(page, api_link)),
            ]
        )
        page.add(tabs)
        page.update()

    page.add(home_screen(page, set_api_link=load_tabs))

ft.app(target=main)