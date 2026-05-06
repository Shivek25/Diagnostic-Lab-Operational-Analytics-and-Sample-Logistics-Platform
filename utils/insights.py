"""
insights.py
-----------
Generates dynamic text insights based on current dashboard data.
"""

import pandas as pd
from utils import metrics as m

def generate_insights(df: pd.DataFrame) -> list[str]:
    """Analyze the dataframe and return a list of actionable insights."""
    if df.empty:
        return ["No data available for insights."]

    insights = []
    
    # 1. Lab with highest rejection rate
    lab_df = m.lab_summary(df)
    if not lab_df.empty:
        # Filter to labs with at least 10 samples to avoid noise
        valid_labs = lab_df[lab_df["sample_count"] >= 10]
        if valid_labs.empty:
            valid_labs = lab_df # fallback
        
        worst_lab = valid_labs.sort_values("rejection_rate_pct", ascending=False).iloc[0]
        if worst_lab["rejection_rate_pct"] > 0:
            insights.append(
                f"🚨 **{worst_lab['lab_name']}** has the highest rejection rate at **{worst_lab['rejection_rate_pct']:.1f}%** (based on {worst_lab['sample_count']} samples)."
            )

    # 2. Courier with highest delay rate
    cou_df = m.courier_summary(df)
    if not cou_df.empty:
        valid_cou = cou_df[cou_df["sample_count"] >= 10]
        if valid_cou.empty:
            valid_cou = cou_df
            
        worst_cou = valid_cou.sort_values("delay_rate_pct", ascending=False).iloc[0]
        if worst_cou["delay_rate_pct"] > 0:
            insights.append(
                f"🚚 **{worst_cou['courier_name']}** has the highest delay rate at **{worst_cou['delay_rate_pct']:.1f}%**."
            )

    # 3. Test with longest TAT
    test_df = m.test_type_summary(df)
    if not test_df.empty:
        longest_test = test_df.sort_values("avg_tat_hours", ascending=False).iloc[0]
        if pd.notna(longest_test["avg_tat_hours"]) and longest_test["avg_tat_hours"] > 0:
            insights.append(
                f"⏳ **{longest_test['test_name']}** has the longest average turnaround time (**{longest_test['avg_tat_hours']:.1f} hrs**)."
            )

    # 4. City with most delays
    # Recalculate delayed subset
    delays_df = m.get_delayed_samples_df(df)
    if not delays_df.empty and "city" in delays_df.columns:
        city_delays = delays_df["city"].value_counts()
        if not city_delays.empty:
            worst_city = city_delays.index[0]
            count = city_delays.iloc[0]
            insights.append(
                f"🏙️ **{worst_city}** leads in delayed samples (**{count}** delayed samples)."
            )

    # General fallback if everything is perfect
    if not insights:
        insights.append("✅ All systems operating normally within selected filters.")

    return insights
