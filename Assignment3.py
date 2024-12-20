import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load dataset (update the paths to match your local environment)
def load_datasets():
    dataset_paths = [
        "01 renewable-share-energy.csv",
        "02 modern-renewable-energy-consumption.csv",
        "03 modern-renewable-prod.csv",
        "04 share-electricity-renewables.csv",
    ]
    datasets = {}
    for dataset in dataset_paths:
        file_path = dataset
        datasets[dataset] = pd.read_csv(file_path)
    return datasets

# Combine datasets for comprehensive visualization
def prepare_combined_data(datasets):
    combined_data = pd.DataFrame()
    for key, df in datasets.items():
        if "Year" in df.columns and "Entity" in df.columns:
            filtered_df = df[(df["Year"] >= 1965) & (df["Year"] <= 2022)]
            combined_data = pd.concat([combined_data, filtered_df], ignore_index=True)
    return combined_data

# Generate static visualization
def generate_static_visualization(combined_data):
    summary_data = combined_data.groupby("Year").sum(numeric_only=True).reset_index()
    plt.figure(figsize=(12, 8))
    plt.plot(summary_data["Year"], summary_data.iloc[:, 1:].sum(axis=1), label="Total Renewable Energy (TWh)", color='green')
    plt.xlabel("Year")
    plt.ylabel("Total Energy (TWh)")
    plt.title("Global Renewable Energy Trends (1965-2022)")
    plt.legend()
    plt.grid(True)
    output_path = "global_renewable_energy_trends.png"
    plt.savefig(output_path)
    plt.close()
    return output_path

# Generate interactive visualization
def generate_interactive_visualization(combined_data):
    combined_data["Region"] = combined_data["Entity"].apply(
        lambda x: "Europe" if "EU" in x or "Germany" in x else "Asia" if "China" in x else "Americas" if "USA" in x or "Brazil" in x else "Other"
    )
    regional_data = combined_data.groupby(["Region", "Year"]).sum(numeric_only=True).reset_index()
    fig = px.line(
        regional_data,
        x="Year",
        y="Electricity from solar (TWh)",
        color="Region",
        title="Regional Contributions to Renewable Energy (1965-2022)",
        labels={"Electricity from solar (TWh)": "Renewable Energy (TWh)", "Year": "Year"},
    )
    fig.update_layout(hovermode="x unified", template="plotly_white")
    output_path = "interactive_renewable_energy.html"
    fig.write_html(output_path)
    return output_path

# Main function to generate all outputs
def main():
    datasets = load_datasets()
    combined_data = prepare_combined_data(datasets)

    static_viz = generate_static_visualization(combined_data)
    interactive_viz = generate_interactive_visualization(combined_data)

    print(f"Static Visualization saved at: {static_viz}")
    print(f"Interactive Visualization saved at: {interactive_viz}")

if __name__ == "__main__":
    main()
