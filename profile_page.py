# profile_page.py

import streamlit as st
import json
import pandas as pd
import os
import plotly.express as px

def show_profile(user):
    st.title("🙍🏻‍♂️ User Profile")

    # --- Card: User Info ---
    st.markdown(f"""
        <div style='
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #ddd;
            width: 400px;
            margin: auto;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        '>
            <h3 style='text-align: center; color: #3b5998;'>Welcome, {user['username'].capitalize()}</h3>
            <p><strong>Username:</strong> {user['username']}</p>
            <p><strong>Role:</strong> {user['role'].capitalize()}</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("## 📊 Prediction History")

    # --- Load prediction logs ---
    if os.path.exists("prediction_history.json"):
        with open("prediction_history.json", "r") as f:
            logs = json.load(f)

        # Filter logs for current user
        user_logs = [log for log in logs if log["username"] == user["username"]]

        if not user_logs:
            st.info("You have no prediction history yet.")
        else:
            # Process logs into DataFrame
            rows = []
            for log in user_logs:
                row = log["input"]
                row["predicted_price"] = log["predicted_price"]
                rows.append(row)

            df = pd.DataFrame(rows)

            # --- Show DataFrame ---
            st.dataframe(df, use_container_width=True)

            # --- CSV Download ---
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Prediction History as CSV",
                data=csv,
                file_name='prediction_history.csv',
                mime='text/csv',
            )

            # --- Price Distribution Chart ---
            # --- Prediction Trend Chart ---
            st.markdown("### 📈 Prediction Trend Over Time")

            # Assign index as a timestamp or sequential number
            df["Prediction #"] = range(1, len(df) + 1)

            fig = px.line(
                df,
                x="Prediction #",
                y="predicted_price",
                markers=True,
                title="Predicted Price Trend",
                color_discrete_sequence=["#3b5998"]
            )
            fig.update_layout(
                xaxis_title="Prediction Number",
                yaxis_title="Predicted Price ($)",
                template="simple_white"
            )
            st.plotly_chart(fig, use_container_width=True)
            # --- Average Price by Car Make ---
            if any(col.startswith("Make_") for col in df.columns):
                st.markdown("### 🚘 Average Predicted Price by Car Make")

                # Extract the car make from one-hot columns
                make_cols = [col for col in df.columns if col.startswith("Make_")]
                df["Make"] = df[make_cols].idxmax(axis=1).str.replace("Make_", "")

                avg_price_by_make = df.groupby("Make")["predicted_price"].mean().reset_index()

                fig_make = px.bar(
                    avg_price_by_make,
                    x="Make",
                    y="predicted_price",
                    title="Average Predicted Price by Car Brand",
                    color_discrete_sequence=["#3b5998"]
                )
                fig_make.update_layout(
                    xaxis_title="Car Brand",
                    yaxis_title="Average Predicted Price ($)",
                    template="simple_white"
                )
                st.plotly_chart(fig_make, use_container_width=True)



    else:
        st.info("Prediction history file not found.")

    st.markdown("---")
    if st.button("⬅️ Back to Dashboard"):
        st.session_state["page"] = "main"