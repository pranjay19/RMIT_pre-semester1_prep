import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# Configure the page layout to wide and set the title/icon
st.set_page_config(page_title="Nexus FinTech Portal", page_icon="🏦", layout="wide")

# ----------------------------------------------------
# Session State Initialization
# ----------------------------------------------------
if 'accounts' not in st.session_state:
    st.session_state.accounts = {
        "Current": 500.00,
        "Savings": 1500.00
    }
if 'pin_attempts' not in st.session_state:
    st.session_state.pin_attempts = 3
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'card_blocked' not in st.session_state:
    st.session_state.card_blocked = False
if 'transactions' not in st.session_state:
    st.session_state.transactions = []

# Helper Function: Add transaction to history
def add_transaction(acc_type, trans_type, amount, balance_after):
    st.session_state.transactions.append({
        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Account": acc_type,
        "Type": trans_type,
        "Amount": f"${amount:.2f}",
        "Balance After": f"${balance_after:.2f}"
    })

# ----------------------------------------------------
# Custom Styling for "Futuristic FinTech" Look
# ----------------------------------------------------
st.markdown("""
<style>
    /* Sleek container styles for metrics */
    div[data-testid="stMetricValue"] {
        color: #00e5ff;
        font-size: 2rem;
    }
    div[data-testid="stMetricLabel"] {
        color: #b0bec5;
        font-size: 1rem;
        font-weight: bold;
    }
    
    /* Headers and Dividers styling */
    h1, h2, h3 {
        color: #e0f7fa !important;
        font-family: 'Courier New', Courier, monospace;
    }
    hr {
        border-color: #00e5ff !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# Application Logic
# ----------------------------------------------------
if not st.session_state.logged_in:
    # --- Login Screen ---
    st.title("🌐 Nexus Secure Terminal")
    st.divider()
    
    # Use columns to center the login box
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("🔐 User Authentication")
        
        if st.session_state.card_blocked:
            st.error("🚫 ACCESS TERMINATED. Card blocked due to multiple security violations.")
        else:
            st.info(f"Security clearance required. Attempts remaining: **{st.session_state.pin_attempts}**")
            
            pin = st.text_input("Enter 4-Digit Security Code (Hint: 1234):", type="password")
            
            if st.button("Authenticate", use_container_width=True, type="primary"):
                if pin == "1234":
                    st.session_state.logged_in = True
                    st.success("✅ Authentication successful. Establishing secure connection...")
                    st.rerun()
                else:
                    st.session_state.pin_attempts -= 1
                    if st.session_state.pin_attempts > 0:
                        st.error("❌ Invalid security code. Please try again.")
                    else:
                        st.session_state.card_blocked = True
                        st.error("🚫 ACCESS TERMINATED. Card blocked.")
                    st.rerun()

else:
    # --- Main FinTech Dashboard ---
    st.title("🌌 Nexus Wealth Management")
    st.divider()

    # Calculate portfolio values
    current_bal = st.session_state.accounts["Current"]
    savings_bal = st.session_state.accounts["Savings"]
    total_wealth = current_bal + savings_bal

    # 1. Top Metrics Cards
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        st.metric(label="Total Portfolio Value", value=f"${total_wealth:,.2f}")
    with metric_col2:
        st.metric(label="Current Account", value=f"${current_bal:,.2f}")
    with metric_col3:
        st.metric(label="Savings Account", value=f"${savings_bal:,.2f}")

    st.divider()

    # 2. Main Dual-Column Layout
    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader("⚡ Quick Operations")
        
        # Expanders for clutter-free UI
        with st.expander("📥 Deposit Funds", expanded=False):
            dep_acc = st.selectbox("Destination Account:", ["Current", "Savings"], key="dep_acc")
            dep_amt = st.number_input("Amount to Deposit ($):", min_value=0.0, step=10.0, format="%.2f", key="dep_amt")
            if st.button("Execute Deposit", type="primary"):
                if dep_amt > 0:
                    st.session_state.accounts[dep_acc] += dep_amt
                    add_transaction(dep_acc, "Deposit 📥", dep_amt, st.session_state.accounts[dep_acc])
                    st.success(f"✅ Successfully deposited ${dep_amt:.2f} into {dep_acc}.")
                    st.rerun()
                else:
                    st.error("❌ Error: Deposit amount must be greater than zero.")
                    
        with st.expander("📤 Withdraw Funds", expanded=False):
            with_acc = st.selectbox("Source Account:", ["Current", "Savings"], key="with_acc")
            with_amt = st.number_input("Amount to Withdraw ($):", min_value=0.0, step=10.0, format="%.2f", key="with_amt")
            if st.button("Execute Withdrawal", type="primary"):
                if with_amt <= 0:
                    st.error("❌ Error: Please enter a valid positive amount.")
                elif with_amt > st.session_state.accounts[with_acc]:
                    st.error("❌ Error: Insufficient liquidity for this transaction.")
                else:
                    st.session_state.accounts[with_acc] -= with_amt
                    add_transaction(with_acc, "Withdrawal 📤", -with_amt, st.session_state.accounts[with_acc])
                    st.success(f"✅ Successfully withdrew ${with_amt:.2f} from {with_acc}.")
                    st.rerun()

        st.subheader("📜 Transaction Ledger")
        if len(st.session_state.transactions) > 0:
            # Create a dataframe and reverse it to show newest transactions first
            df_transactions = pd.DataFrame(st.session_state.transactions)
            st.dataframe(
                df_transactions.iloc[::-1], 
                use_container_width=True, 
                hide_index=True
            )
        else:
            st.info("No recent ledger activity detected.")

    with right_col:
        st.subheader("📊 Asset Allocation")
        
        # Plotly Donut Chart
        df_assets = pd.DataFrame({
            "Account": ["Current", "Savings"],
            "Balance": [current_bal, savings_bal]
        })
        
        fig = px.pie(
            df_assets, 
            values="Balance", 
            names="Account", 
            hole=0.6,
            color_discrete_sequence=["#00e5ff", "#7e57c2"]
        )
        # Make the background transparent for the futuristic theme
        fig.update_layout(
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#b0bec5")
        )
        st.plotly_chart(fig, use_container_width=True)

        st.divider()
        st.subheader("🔒 Terminal Access")
        if st.button("End Secure Session (Logout)", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.pin_attempts = 3
            st.success("Session terminated securely.")
            st.rerun()
