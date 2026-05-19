import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# --------------------------------
# FILES
# --------------------------------
USER_FILE = "users.csv"
EXPENSE_FILE = "expenses.csv"

# --------------------------------
# CREATE FILES IF NOT EXISTS
# --------------------------------
if not os.path.exists(USER_FILE):
    users_df = pd.DataFrame(columns=["username", "password"])
    users_df.to_csv(USER_FILE, index=False)

if not os.path.exists(EXPENSE_FILE):
    expenses_df = pd.DataFrame(
        columns=["Username", "Date", "Category", "Amount"]
    )
    expenses_df.to_csv(EXPENSE_FILE, index=False)

# --------------------------------
# LOAD DATA
# --------------------------------
users_df = pd.read_csv(USER_FILE)
expenses_df = pd.read_csv(EXPENSE_FILE)

# --------------------------------
# SESSION STATE
# --------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# --------------------------------
# TITLE
# --------------------------------
st.title("💰 Smart Expense Tracker")

# --------------------------------
# SIDEBAR MENU
# --------------------------------
menu = st.sidebar.selectbox(
    "Menu",
    ["Login", "Register"]
)

# =========================================
# REGISTER
# =========================================
if menu == "Register":

    st.subheader("📝 Create Account")

    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")

    if st.button("Register"):

        if new_user in users_df["username"].values:

            st.error("❌ Username already exists")

        else:

            new_data = pd.DataFrame({
                "username": [new_user],
                "password": [new_pass]
            })

            users_df = pd.concat(
                [users_df, new_data],
                ignore_index=True
            )

            users_df.to_csv(USER_FILE, index=False)

            st.success("✅ Account Created Successfully!")

# =========================================
# LOGIN
# =========================================
elif menu == "Login":

    st.subheader("🔐 Login")

    username = st.text_input("Enter Username")
    password = st.text_input(
        "Enter Password",
        type="password"
    )

    if st.button("Login"):

        user = users_df[
            (users_df["username"] == username) &
            (users_df["password"] == password)
        ]

        if not user.empty:

            st.session_state.logged_in = True
            st.session_state.username = username

            st.success(f"✅ Welcome {username}")

        else:

            st.error("❌ Invalid Username or Password")

# =========================================
# AFTER LOGIN
# =========================================
if st.session_state.logged_in:

    current_user = st.session_state.username

    st.header(f"👤 Logged in as: {current_user}")

    # --------------------------------
    # ADD EXPENSE
    # --------------------------------
    st.subheader("➕ Add Expense")

    date = st.date_input("Select Date")

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Travel",
            "Shopping",
            "Bills",
            "Entertainment",
            "Other"
        ]
    )

    amount = st.number_input(
        "Enter Amount",
        min_value=0
    )

    if st.button("Add Expense"):

        new_expense = pd.DataFrame({
            "Username": [current_user],
            "Date": [date],
            "Category": [category],
            "Amount": [amount]
        })

        expenses_df = pd.concat(
            [expenses_df, new_expense],
            ignore_index=True
        )

        expenses_df.to_csv(EXPENSE_FILE, index=False)

        st.success("✅ Expense Added Successfully!")

    # --------------------------------
    # USER DATA
    # --------------------------------
    user_data = expenses_df[
        expenses_df["Username"] == current_user
    ]

    # --------------------------------
    # DISPLAY DATA
    # --------------------------------
    st.subheader("📄 Your Expenses")

    st.dataframe(user_data)

    # --------------------------------
    # TOTAL EXPENSE
    # --------------------------------
    total = user_data["Amount"].sum()

    st.subheader(f"💸 Total Spent: ₹{total}")

    # --------------------------------
    # CATEGORY TOTAL
    # --------------------------------
    if not user_data.empty:

        category_total = user_data.groupby(
            "Category"
        )["Amount"].sum()

        # --------------------------------
        # BAR CHART
        # --------------------------------
        st.subheader("📊 Bar Chart")

        fig1, ax1 = plt.subplots()

        category_total.plot(
            kind='bar',
            ax=ax1
        )

        ax1.set_xlabel("Category")
        ax1.set_ylabel("Amount")

        st.pyplot(fig1)

        # --------------------------------
        # PIE CHART
        # --------------------------------
        st.subheader("🥧 Pie Chart")

        fig2, ax2 = plt.subplots()

        category_total.plot(
            kind='pie',
            autopct='%1.1f%%',
            ax=ax2
        )

        ax2.set_ylabel("")

        st.pyplot(fig2)

    # --------------------------------
    # MONTHLY INCOME
    # --------------------------------
    st.subheader("💼 Monthly Income")

    income = st.number_input(
        "Enter Monthly Income",
        min_value=0,
        value=10000
    )

    # --------------------------------
    # MONTHLY BUDGET
    # --------------------------------
    st.subheader("🎯 Monthly Budget")

    budget = st.number_input(
        "Enter Monthly Budget",
        min_value=0,
        value=5000
    )

    # --------------------------------
    # CALCULATIONS
    # --------------------------------
    spent = total

    remaining_budget = budget - spent

    savings = income - spent

    # --------------------------------
    # FINANCIAL SUMMARY
    # --------------------------------
    st.subheader("📌 Financial Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💸 Total Spent",
        f"₹{spent}"
    )

    col2.metric(
        "💰 Remaining Budget",
        f"₹{remaining_budget}"
    )

    col3.metric(
        "🏦 Savings",
        f"₹{savings}"
    )

    # --------------------------------
    # PROGRESS BAR
    # --------------------------------
    st.subheader("📊 Budget Usage")

    if budget > 0:

        progress = min(spent / budget, 1.0)

        st.progress(progress)

    # --------------------------------
    # ALERTS
    # --------------------------------
    if spent > budget:

        st.error("🚨 ALERT! Budget Exceeded!")

        st.audio(
            "https://www.soundjay.com/buttons/sounds/beep-01a.mp3",
            autoplay=True
        )

    elif spent > (0.8 * budget):

        st.warning("⚠ Warning: 80% Budget Used!")

    else:

        st.success("✅ Budget Under Control")

    # --------------------------------
    # SAVINGS STATUS
    # --------------------------------
    if savings > 0:

        st.success(
            f"🎉 You saved ₹{savings} this month!"
        )

    else:

        st.error(
            f"😢 Overspent by ₹{abs(savings)}"
        )

    # --------------------------------
    # EXPORT REPORT
    # --------------------------------
    if st.button("Export My Report"):

        if not os.path.exists("reports"):
            os.makedirs("reports")

        path = f"reports/{current_user}_report.xlsx"

        user_data.to_excel(path, index=False)

        st.success("✅ Report Exported!")

        with open(path, "rb") as file:

            st.download_button(
                label="📥 Download Report",
                data=file,
                file_name=f"{current_user}_report.xlsx",
                mime="application/vnd.ms-excel"
            )

    # --------------------------------
    # LOGOUT
    # --------------------------------
    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.username = ""

        st.success("✅ Logged Out")