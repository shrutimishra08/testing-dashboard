import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("RedBull AI Talent Matching Dashboard")

# Precomputed personas (replace with your Colab output)
personas = {
    'Sales': {'Diplomatic': 85.80, 'Balanced': 87.10, 'Sociable': 78.30, 'Innovative': 83.00, 'SalesRevenue': 485000.00, 'MarketShare': 5.09},
    'Retail': {'Diplomatic': 78.60, 'Balanced': 81.00, 'Sociable': 87.30, 'Innovative': 71.00, 'SalesRevenue': 406700.00, 'MarketShare': 4.06},
    'Product': {'Diplomatic': 70.50, 'Balanced': 86.50, 'Sociable': 76.70, 'Innovative': 90.60, 'EBIT': 502000.00, 'ProjectDeliveryRate': 90.00},
    'HR': {'Diplomatic': 86.50, 'Balanced': 90.50, 'Sociable': 80.60, 'Innovative': 76.30, 'RetentionRate': 85.50},
    'Legal': {'Diplomatic': 90.40, 'Balanced': 85.60, 'Sociable': 70.40, 'Innovative': 80.60, 'ComplianceRate': 95.10}
}

# Display personas
st.header("Department Personas")
persona_df = pd.DataFrame(personas).T
st.dataframe(persona_df.round(2))

# Function to match candidate to a department
def match_candidate(diplomatic, balanced, sociable, innovative):
    candidate = np.array([diplomatic, balanced, sociable, innovative])
    distances = {}
    for dept in personas:
        persona_scores = np.array([personas[dept][m] for m in ['Diplomatic', 'Balanced', 'Sociable', 'Innovative']])
        distance = np.sqrt(np.sum((candidate - persona_scores) ** 2))
        distances[dept] = distance
    best_match = min(distances, key=distances.get)
    return best_match, distances

# Candidate input for multiple candidates
st.header("Multiple Candidate WingFinder Input")
num_candidates = st.number_input("Number of Candidates (1-5)", min_value=1, max_value=5, value=1, step=1)

candidates = []
for i in range(num_candidates):
    st.subheader(f"Candidate {i+1}")
    with st.form(key=f"candidate_{i}"):
        diplomatic = st.slider("Diplomatic", 0, 100, 85, key=f"diplomatic_{i}")
        balanced = st.slider("Balanced", 0, 100, 90, key=f"balanced_{i}")
        sociable = st.slider("Sociable", 0, 100, 75, key=f"sociable_{i}")
        innovative = st.slider("Innovative", 0, 100, 80, key=f"innovative_{i}")
        candidates.append((diplomatic, balanced, sociable, innovative))
        st.form_submit_button(label=f"Submit Candidate {i+1}")

if st.button("Match All Candidates"):
    results = []
    for idx, (diplomatic, balanced, sociable, innovative) in enumerate(candidates):
        best_dept, distances = match_candidate(diplomatic, balanced, sociable, innovative)
        results.append({"Candidate": f"Candidate {idx+1}", "Best Department": best_dept, **distances})

    results_df = pd.DataFrame(results)
    st.subheader("Matching Results")
    st.dataframe(results_df.round(2))

    # Visualization
    melt_df = results_df.melt(id_vars=["Candidate", "Best Department"], var_name="Department", value_name="Distance")
    fig = px.bar(melt_df, x="Candidate", y="Distance", color="Department", barmode="group",
                 title="Match Scores for All Candidates", height=400)
    st.plotly_chart(fig)