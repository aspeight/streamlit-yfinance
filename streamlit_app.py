import streamlit as st
import pandas as pd
import datetime


def yield_from(
    trade_date,
    expiration_date,
    box_width,
    extra_days,
    box_price,
    days_per_year,
):
    num_days = (pd.to_datetime(expiration_date) - pd.to_datetime(trade_date)).days + extra_days
    tau = num_days / days_per_year
    return 100 * (box_width / box_price - 1) / tau

def price_from(
    trade_date,
    expiration_date,
    box_width,
    extra_days,
    yield_pct,
    days_per_year,
):
    num_days = (pd.to_datetime(expiration_date) - pd.to_datetime(trade_date)).days + extra_days
    tau = num_days / days_per_year
    price = box_width / (1 + 0.01*yield_pct * tau)
    return price
    
def compute_box_price(yield_pct):
    commission_offset = 4 * commission_per_contract / contract_multiplier
    return round(price_from(
        trade_date=trade_date,
        expiration_date=expiration_date,
        box_width=box_width + commission_offset,
        extra_days=extra_days,
        yield_pct=yield_pct,
        days_per_year=days_per_year,     
    ), 4)

def compute_box_yield(box_price):
    commission_offset = 4 * commission_per_contract / contract_multiplier
    return round(yield_from(
        trade_date=trade_date,
        expiration_date=expiration_date,
        box_width=box_width + commission_offset,
        extra_days=extra_days,
        box_price=box_price,
        days_per_year=days_per_year,     
    ), 4) ## TODO: check commission offset?



st.title('Box Spread Calculator')

st.markdown(
    'Computes prices/yields of a box spread: \n'
    '  - B is the width of the strikes \n'
    '  - P is the price of the box spread \n'
    '    - The price is net of commissions. \n'
    '  - R is the yield of the box spread \n'
    '  - T is the fraction of year between trade and expiration dates \n'
    '    - T may include a few extra days to allow funds to settle \n'
    '\n'
    '`B = (1 + R * T) * P`\n'
)

with st.sidebar:
    trade_date = st.date_input(
        'Trade Date: ', 
        value=datetime.date.today(),
    )
    expiration_date = st.date_input(
        'Expiration Date: ',
        value=datetime.date.today() + datetime.timedelta(days=90),
    )
    box_width = st.number_input('Box Strike Width: ', value=1000, min_value=0, max_value=999_999)
    extra_days = st.number_input('Extra Settle Days: ', value=0, min_value=-5, max_value=10)
    commission_per_contract = st.number_input('Commission per contract: ', value=0., min_value=0., max_value=10., step=0.25)
    contract_multiplier = st.number_input('Contract Multiplier: ', value=100, min_value=0, max_value=1_000_000, step=10)
    days_per_year = st.selectbox('Days per year: ', [360, 365], index=0)

col1,col2 = st.columns(2)
with col1:
    yield_pct1 = st.number_input('Yield (pct): ', step=0.01, value=5.)
    st.markdown(f'### Box Price: {compute_box_price(yield_pct1):.3f}')

with col2:
    box_price2 = st.number_input('Box Price: ', step=0.01, value=float(box_width))
    st.markdown(f'### Box Yield (pct): {compute_box_yield(box_price2):.2f}')


#st.json(st.session_state)
    



