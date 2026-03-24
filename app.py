import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import pandas as pd

# 🎨 PROFESSIONAL DARK UI
st.markdown("""
<style>
/* Background */
.stApp {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Title */
h1 {
    color: #ffffff;
    text-align: center;
    font-family: 'Segoe UI', sans-serif;
    font-weight: bold;
}

/* Subheaders */
h2, h3 {
    color: #00e6e6;
}

/* Labels */
label {
    color: #ffffff !important;
    font-weight: 500;
}

/* Input fields */
input {
    background-color: #f0f0f0 !important;
    color: black !important;
    border-radius: 8px !important;
    padding: 6px !important;
}

/* Button */
.stButton>button {
    background: linear-gradient(to right, #00c6ff, #0072ff);
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
}

/* Table */
.stDataFrame {
    background-color: white;
    border-radius: 10px;
}

/* Markdown text */
.css-1d391kg, .css-ffhzg2 {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# 🌐 Language selection
lang = st.selectbox("Select Language / மொழி தேர்வு", ["English", "Tamil"])

if lang == "Tamil":
    title = "📊 விற்பனை கணிப்பு செயலி"
    product_text = "பொருள் பெயர் (comma use பண்ணி பல பொருள் எழுதவும்)"
    data_text = "கடைசி 5 மாத தகவல் உள்ளிடவும்"
    btn = "கணிக்க"
else:
    title = "📊 Sales Prediction App"
    product_text = "Enter product names (comma separated)"
    data_text = "Enter Last 5 Months Data"
    btn = "Predict"

# 🏷 Title
st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)

# 📦 Product input
products = st.text_input(product_text)

if products:
    product_list = [p.strip() for p in products.split(",")]

    data = {}

    for product in product_list:
        st.subheader(f"{product} Data")

        months, price, quantity = [], [], []

        st.write(data_text)

        for i in range(5):
            m = st.text_input(f"{product} Month {i+1}", key=f"{product}m{i}")
            p = st.text_input(f"{product} Price {i+1}", key=f"{product}p{i}")
            q = st.text_input(f"{product} Quantity {i+1}", key=f"{product}q{i}")

            try:
                months.append(float(m))
                price.append(float(p))
                quantity.append(float(q))
            except:
                st.warning("⚠️ Enter valid numbers!")
                st.stop()

        data[product] = (months, price, quantity)

    st.markdown("---")
    st.markdown("## 📊 Prediction Results")

    if st.button(btn):

        all_results = []
        fig, ax = plt.subplots()

        for product in product_list:
            months, price, quantity = data[product]

            X = np.array(months).reshape(-1,1)

            model_p = LinearRegression().fit(X, price)
            model_q = LinearRegression().fit(X, quantity)

            future = np.array([6,7,8]).reshape(-1,1)

            pred_p = model_p.predict(future)
            pred_q = model_q.predict(future)
            revenue = pred_p * pred_q

            for i in range(3):
                all_results.append({
                    "Product": product,
                    "Month": f"M{6+i}",
                    "Price": round(pred_p[i],2),
                    "Quantity": round(pred_q[i],2),
                    "Revenue": round(revenue[i],2)
                })

            ax.plot(['M6','M7','M8'], revenue, marker='o', label=product)

        # 📋 Table
        st.subheader("📋 Prediction Table")
        df = pd.DataFrame(all_results)
        st.dataframe(df)

        # 📈 Graph
        ax.set_title("Future Revenue Comparison")
        ax.set_xlabel("Months")
        ax.set_ylabel("Revenue")
        ax.legend()

        st.pyplot(fig)
        plt.close(fig)