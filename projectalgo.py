import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
#from utils import generate_mock_data
import random
import requests
from kiteconnect import KiteConnect
import time
import threading
#import datetime
from datetime import datetime, timedelta
import os
import pytz  # ✅ Add this for details ssfsdfsdf 
from streamlit_autorefresh import st_autorefresh
from math import floor
from dotenv import load_dotenv
import numpy as np
import matplotlib.pyplot as plt
from ta.momentum import RSIIndicator


# Global kite object placeholder
if 'kite' not in st.session_state:
    st.session_state.kite = None
# Page configuration
st.set_page_config(layout="wide", page_title="Trade Strategy Dashboard")
    
# Sidebar navigation
with st.sidebar:
    selected = option_menu(
    menu_title="ALGO BOT  ",
    options=[
        "Dashboard", "Get Stock Data", "Doctor Strategy","Doctor1.0 Strategy","Doctor2.0 Strategy","Doctor3.0 Strategy", "Swing Trade Strategy", "Swing SMA44 Strategy","SMA44+200MA Strategy","Golden Cross","Pullback to EMA20","New Nifty Strategy",
        "Intraday Stock Finder","ORB Strategy","ORB Screener", "Trade Log", "Account Info", "Candle Chart", "Strategy Detail","Strategy2.0 Detail", "Project Detail", "KITE API", "API","Alpha Vantage API","Live Algo Trading","Paper Trade","Volatility Scanner","TradingView","Telegram Demo","NIFTY PCR","3PM STRATEGY","3PM OPTION","NIFTY OI,PCR,D "
    ],
    icons=[
        "bar-chart", "search", "cpu", "cpu","cpu", "cpu","cpu","cpu","cpu","cpu", "arrow-repeat",
        "search", "clipboard-data", "wallet2", "graph-up","graph-up", "info-circle", "search","file-earmark","file-earmark", "code-slash", "code-slash","code-slash", "code-slash","journal-text","search", "bar-chart", "bar-chart","file-earmark", "bar-chart","file-earmark","file-earmark","file-earmark"
    ],
    menu_icon="cast",
    default_index=0,
)   

# Main area rendering
st.markdown("""
    <style>
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .card {
            background-color: white;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            padding: 20px;
            margin: 10px 0;
        }
        .card-title {
            font-size: 18px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

nifty50_stocks = [
        '360ONE.NS',
        '3MINDIA.NS',
        'ABB.NS',
        'ACC.NS',
        'ACMESOLAR.NS',
        'AIAENG.NS',
        'APLAPOLLO.NS',
        'AUBANK.NS',
        'AWL.NS',
        'AADHARHFC.NS',
        'AARTIIND.NS',
        'AAVAS.NS',
        'ABBOTINDIA.NS',
        'ACE.NS',
        'ADANIENSOL.NS',
        'ADANIENT.NS',
        'ADANIGREEN.NS',
        'ADANIPORTS.NS',
        'ADANIPOWER.NS',
        'ATGL.NS',
        'ABCAPITAL.NS',
        'ABFRL.NS',
        'ABREL.NS',
        'ABSLAMC.NS',
        'AEGISLOG.NS',
        'AFCONS.NS',
        'AFFLE.NS',
        'AJANTPHARM.NS',
        'AKUMS.NS',
        'APLLTD.NS',
        'ALIVUS.NS',
        'ALKEM.NS',
        'ALKYLAMINE.NS',
        'ALOKINDS.NS',
        'ARE&M.NS',
        'AMBER.NS',
        'AMBUJACEM.NS',
        'ANANDRATHI.NS',
        'ANANTRAJ.NS',
        'ANGELONE.NS',
        'APARINDS.NS',
        'APOLLOHOSP.NS',
        'APOLLOTYRE.NS',
        'APTUS.NS',
        'ASAHIINDIA.NS',
        'ASHOKLEY.NS',
        'ASIANPAINT.NS',
        'ASTERDM.NS',
        'ASTRAZEN.NS',
        'ASTRAL.NS',
        'ATUL.NS',
        'AUROPHARMA.NS',
        'AIIL.NS',
        'DMART.NS',
        'AXISBANK.NS',
        'BASF.NS',
        'BEML.NS',
        'BLS.NS',
        'BSE.NS',
        'BAJAJ-AUTO.NS',
        'BAJFINANCE.NS',
        'BAJAJFINSV.NS',
        'BAJAJHLDNG.NS',
        'BAJAJHFL.NS',
        'BALKRISIND.NS',
        'BALRAMCHIN.NS',
        'BANDHANBNK.NS',
        'BANKBARODA.NS',
        'BANKINDIA.NS',
        'MAHABANK.NS',
        'BATAINDIA.NS',
        'BAYERCROP.NS',
        'BERGEPAINT.NS',
        'BDL.NS',
        'BEL.NS',
        'BHARATFORG.NS',
        'BHEL.NS',
        'BPCL.NS',
        'BHARTIARTL.NS',
        'BHARTIHEXA.NS',
        'BIKAJI.NS',
        'BIOCON.NS',
        'BSOFT.NS',
        'BLUEDART.NS',
        'BLUESTARCO.NS',
        'BBTC.NS',
        'BOSCHLTD.NS',
        'FIRSTCRY.NS',
        'BRIGADE.NS',
        'BRITANNIA.NS',
        'MAPMYINDIA.NS',
        'CCL.NS',
        'CESC.NS',
        'CGPOWER.NS',
        'CRISIL.NS',
        'CAMPUS.NS',
        'CANFINHOME.NS',
        'CANBK.NS',
        'CAPLIPOINT.NS',
        'CGCL.NS',
        'CARBORUNIV.NS',
        'CASTROLIND.NS',
        'CEATLTD.NS',
        'CENTRALBK.NS',
        'CDSL.NS',
        'CENTURYPLY.NS',
        'CERA.NS',
        'CHALET.NS',
        'CHAMBLFERT.NS',
        'CHENNPETRO.NS',
        'CHOLAHLDNG.NS',
        'CHOLAFIN.NS',
        'CIPLA.NS',
        'CUB.NS',
        'CLEAN.NS',
        'COALINDIA.NS',
        'COCHINSHIP.NS',
        'COFORGE.NS',
        'COHANCE.NS',
        'COLPAL.NS',
        'CAMS.NS',
        'CONCORDBIO.NS',
        'CONCOR.NS',
        'COROMANDEL.NS',
        'CRAFTSMAN.NS',
        'CREDITACC.NS',
        'CROMPTON.NS',
        'CUMMINSIND.NS',
        'CYIENT.NS',
        'DCMSHRIRAM.NS',
        'DLF.NS',
        'DOMS.NS',
        'DABUR.NS',
        'DALBHARAT.NS',
        'DATAPATTNS.NS',
        'DEEPAKFERT.NS',
        'DEEPAKNTR.NS',
        'DELHIVERY.NS',
        'DEVYANI.NS',
        'DIVISLAB.NS',
        'DIXON.NS',
        'LALPATHLAB.NS',
        'DRREDDY.NS',   
        'EIDPARRY.NS',
        'EIHOTEL.NS',
        'EICHERMOT.NS',
        'ELECON.NS',
        'ELGIEQUIP.NS',
        'EMAMILTD.NS',
        'EMCURE.NS',
        'ENDURANCE.NS',
        'ENGINERSIN.NS',
        'ERIS.NS',
        'ESCORTS.NS',
        'ETERNAL.NS',
        'EXIDEIND.NS',
        'NYKAA.NS',
        'FEDERALBNK.NS',
        'FACT.NS',
        'FINCABLES.NS',
        'FINPIPE.NS',
        'FSL.NS',
        'FIVESTAR.NS',
        'FORTIS.NS',
        'GAIL.NS',
        'GVT&D.NS',
        'GMRAIRPORT.NS',
        'GRSE.NS',
        'GICRE.NS',
        'GILLETTE.NS',
        'GLAND.NS',
        'GLAXO.NS',
        'GLENMARK.NS',
        'MEDANTA.NS',
        'GODIGIT.NS',
        'GPIL.NS',
        'GODFRYPHLP.NS',
        'GODREJAGRO.NS',
        'GODREJCP.NS',
        'GODREJIND.NS',
        'GODREJPROP.NS',
        'GRANULES.NS',
        'GRAPHITE.NS',
        'GRASIM.NS',
        'GRAVITA.NS',
        'GESHIP.NS',
        'FLUOROCHEM.NS',
        'GUJGASLTD.NS',
        'GMDCLTD.NS',
        'GNFC.NS',
        'GPPL.NS',
        'GSPL.NS',
        'HEG.NS',
        'HBLENGINE.NS',
        'HCLTECH.NS',
        'HDFCAMC.NS',
        'HDFCBANK.NS',
        'HDFCLIFE.NS',
        'HFCL.NS',
        'HAPPSTMNDS.NS',
        'HAVELLS.NS',
        'HEROMOTOCO.NS',
        'HSCL.NS',
        'HINDALCO.NS',
        'HAL.NS',
        'HINDCOPPER.NS',
        'HINDPETRO.NS',
        'HINDUNILVR.NS',
        'HINDZINC.NS',
        'POWERINDIA.NS',
        'HOMEFIRST.NS',
        'HONASA.NS',
        'HONAUT.NS',
        'HUDCO.NS',
        'HYUNDAI.NS',
        'ICICIBANK.NS',
        'ICICIGI.NS',
        'ICICIPRULI.NS',
        'IDBI.NS',
        'IDFCFIRSTB.NS',
        'IFCI.NS',
        'IIFL.NS',
        'INOXINDIA.NS',
        'IRB.NS',
        'IRCON.NS',
        'ITC.NS',
        'ITI.NS',
        'INDGN.NS',
        'INDIACEM.NS',
        'INDIAMART.NS',
        'INDIANB.NS',
        'IEX.NS',
        'INDHOTEL.NS',
        'IOC.NS',
        'IOB.NS',
        'IRCTC.NS',
        'IRFC.NS',
        'IREDA.NS',
        'IGL.NS',
        'INDUSTOWER.NS',
        'INDUSINDBK.NS',
        'NAUKRI.NS',
        'INFY.NS',
        'INOXWIND.NS',
        'INTELLECT.NS',
        'INDIGO.NS',
        'IGIL.NS',
        'IKS.NS',
        'IPCALAB.NS',
        'JBCHEPHARM.NS',
        'JKCEMENT.NS',
        'JBMA.NS',
        'JKTYRE.NS',
        'JMFINANCIL.NS',
        'JSWENERGY.NS',
        'JSWHL.NS',
        'JSWINFRA.NS',
        'JSWSTEEL.NS',
        'JPPOWER.NS',
        'J&KBANK.NS',
        'JINDALSAW.NS',
        'JSL.NS',
        'JINDALSTEL.NS',
        'JIOFIN.NS',
        'JUBLFOOD.NS',
        'JUBLINGREA.NS',
        'JUBLPHARMA.NS',
        'JWL.NS',
        'JUSTDIAL.NS',
        'JYOTHYLAB.NS',
        'JYOTICNC.NS',
        'KPRMILL.NS',
        'KEI.NS',
        'KNRCON.NS',
        'KPITTECH.NS',
        'KAJARIACER.NS',
        'KPIL.NS',
        'KALYANKJIL.NS',
        'KANSAINER.NS',
        'KARURVYSYA.NS',
        'KAYNES.NS',
        'KEC.NS',
        'KFINTECH.NS',
        'KIRLOSBROS.NS',
        'KIRLOSENG.NS',
        'KOTAKBANK.NS',
        'KIMS.NS',
        'LTF.NS',
        'LTTS.NS',
        'LICHSGFIN.NS',
        'LTFOODS.NS',
        'LTIM.NS',
        'LT.NS',
        'LATENTVIEW.NS',
        'LAURUSLABS.NS',
        'LEMONTREE.NS',
        'LICI.NS',
        'LINDEINDIA.NS',
        'LLOYDSME.NS',
        'LUPIN.NS',
        'MMTC.NS',
        'MRF.NS',
        'LODHA.NS',
        'MGL.NS',
        'MAHSEAMLES.NS',
        'M&MFIN.NS',
        'M&M.NS',
        'MANAPPURAM.NS',
        'MRPL.NS',
        'MANKIND.NS',
        'MARICO.NS',
        'MARUTI.NS',
        'MASTEK.NS',
        'MFSL.NS',
        'MAXHEALTH.NS',
        'MAZDOCK.NS',
        'METROPOLIS.NS',
        'MINDACORP.NS',
        'MSUMI.NS',
        'MOTILALOFS.NS',
        'MPHASIS.NS',
        'MCX.NS',
        'MUTHOOTFIN.NS',
        'NATCOPHARM.NS',
        'NBCC.NS',
        'NCC.NS',
        'NHPC.NS',
        'NLCINDIA.NS',
        'NMDC.NS',
        'NSLNISP.NS',
        'NTPCGREEN.NS',
        'NTPC.NS',
        'NH.NS',
        'NATIONALUM.NS',
        'NAVA.NS',
        'NAVINFLUOR.NS',
        'NESTLEIND.NS',
        'NETWEB.NS',
        'NETWORK18.NS',
        'NEULANDLAB.NS',
        'NEWGEN.NS',
        'NAM-INDIA.NS',
        'NIVABUPA.NS',
        'NUVAMA.NS',
        'OBEROIRLTY.NS',
        'ONGC.NS',
        'OIL.NS',
        'OLAELEC.NS',
        'OLECTRA.NS',
        'PAYTM.NS',
        'OFSS.NS',
        'POLICYBZR.NS',
        'PCBL.NS',
        'PGEL.NS',
        'PIIND.NS',
        'PNBHOUSING.NS',
        'PNCINFRA.NS',
        'PTCIL.NS',
        'PVRINOX.NS',
        'PAGEIND.NS',
        'PATANJALI.NS',
        'PERSISTENT.NS',
        'PETRONET.NS',
        'PFIZER.NS',
        'PHOENIXLTD.NS',
        'PIDILITIND.NS',
        'PEL.NS',
        'PPLPHARMA.NS',
        'POLYMED.NS',
        'POLYCAB.NS',
        'POONAWALLA.NS',
        'PFC.NS',
        'POWERGRID.NS',
        'PRAJIND.NS',
        'PREMIERENE.NS',
        'PRESTIGE.NS',
        'PNB.NS',
        'RRKABEL.NS',
        'RBLBANK.NS',
        'RECLTD.NS',
        'RHIM.NS',
        'RITES.NS',
        'RADICO.NS',
        'RVNL.NS',
        'RAILTEL.NS',
        'RAINBOW.NS',
        'RKFORGE.NS',
        'RCF.NS',
        'RTNINDIA.NS',
        'RAYMONDLSL.NS',
        'RAYMOND.NS',
        'REDINGTON.NS',
        'RELIANCE.NS',
        'RPOWER.NS',
        'ROUTE.NS',
        'SBFC.NS',
        'SBICARD.NS',
        'SBILIFE.NS',
        'SJVN.NS',
        'SKFINDIA.NS',
        'SRF.NS',
        'SAGILITY.NS',
        'SAILIFE.NS',
        'SAMMAANCAP.NS',
        'MOTHERSON.NS',
        'SAPPHIRE.NS',
        'SARDAEN.NS',
        'SAREGAMA.NS',
        'SCHAEFFLER.NS',
        'SCHNEIDER.NS',
        'SCI.NS',
        'SHREECEM.NS',
        'RENUKA.NS',
        'SHRIRAMFIN.NS',
        'SHYAMMETL.NS',
        'SIEMENS.NS',
        'SIGNATURE.NS',
        'SOBHA.NS',
        'SOLARINDS.NS',
        'SONACOMS.NS',
        'SONATSOFTW.NS',
        'STARHEALTH.NS',
        'SBIN.NS',
        'SAIL.NS',
        'SWSOLAR.NS',
        'SUMICHEM.NS',
        'SUNPHARMA.NS',
        'SUNTV.NS',
        'SUNDARMFIN.NS',
        'SUNDRMFAST.NS',
        'SUPREMEIND.NS',
        'SUZLON.NS',
        'SWANENERGY.NS',
        'SWIGGY.NS',
        'SYNGENE.NS',
        'SYRMA.NS',
        'TBOTEK.NS',
        'TVSMOTOR.NS',
        'TANLA.NS',
        'TATACHEM.NS',
        'TATACOMM.NS',
        'TCS.NS',
        'TATACONSUM.NS',
        'TATAELXSI.NS',
        'TATAINVEST.NS',
        'TATAMOTORS.NS',
        'TATAPOWER.NS',
        'TATASTEEL.NS',
        'TATATECH.NS',
        'TTML.NS',
        'TECHM.NS',
        'TECHNOE.NS',
        'TEJASNET.NS',
        'NIACL.NS',
        'RAMCOCEM.NS',
        'THERMAX.NS',
        'TIMKEN.NS',
        'TITAGARH.NS',
        'TITAN.NS',
        'TORNTPHARM.NS',
        'TORNTPOWER.NS',
        'TARIL.NS',
        'TRENT.NS',
        'TRIDENT.NS',
        'TRIVENI.NS',
        'TRITURBINE.NS',
        'TIINDIA.NS',
        'UCOBANK.NS',
        'UNOMINDA.NS',
        'UPL.NS',
        'UTIAMC.NS',
        'ULTRACEMCO.NS',
        'UNIONBANK.NS',
        'UBL.NS',
        'UNITDSPR.NS',
        'USHAMART.NS',
        'VGUARD.NS',
        'DBREALTY.NS',
        'VTL.NS',
        'VBL.NS',
        'MANYAVAR.NS',
        'VEDL.NS',
        'VIJAYA.NS',
        'VMM.NS',
        'IDEA.NS',
        'VOLTAS.NS',
        'WAAREEENER.NS',
        'WELCORP.NS',
        'WELSPUNLIV.NS',
        'WESTLIFE.NS',
        'WHIRLPOOL.NS',
        'WIPRO.NS',
        'WOCKPHARMA.NS',
        'YESBANK.NS',
        'ZFCVINDIA.NS',
        'ZEEL.NS',
        'ZENTEC.NS',
        'ZENSARTECH.NS',
        'ZYDUSLIFE.NS',
        'ECLERX.NS',
    ]
    


if selected == "Dashboard":
    st.subheader("📊 Dashboard - Zerodha Account Overview")       
    # Get current time in UTC
    #utc_now = datetime.datetime.utcnow()
    
    # Define the Indian time zone
    #ist_timezone = pytz.timezone('Asia/Kolkata')
    
    # Localize the UTC time to IST
    #ist_now = utc_now.replace(tzinfo=pytz.utc).astimezone(ist_timezone)
    
    # Display the time in Streamlit
    #st.write("Current time in IST:", ist_now.strftime("%Y-%m-%d %H:%M:%S %Z%z"))
    if "kite" in st.session_state and st.session_state.kite is not None:
        kite = st.session_state.kite

        # ✅ Funds
        try:
            funds = kite.margins(segment="equity")
            available_cash = funds['available']['cash']
            st.metric("💰 Available Fund", f"₹ {available_cash:,.2f}")
        except Exception as e:
            st.error(f"Failed to fetch funds: {e}")

        # ✅ Holdings
        try:
            holdings = kite.holdings()
            if holdings:
                df_holdings = pd.DataFrame(holdings)
                df_holdings = df_holdings[["tradingsymbol", "quantity", "average_price", "last_price", "pnl"]]
                df_holdings["holding_value"] = df_holdings["quantity"] * df_holdings["last_price"]

                total_holding_value = df_holdings["holding_value"].sum()
                total_pnl = df_holdings["pnl"].sum()

                st.metric("📦 Total Holding Value", f"₹ {total_holding_value:,.2f}")
                st.metric("📈 Total P&L", f"₹ {total_pnl:,.2f}", delta_color="normal")

                st.write("📄 Your Holdings:")
                st.dataframe(
                    df_holdings.style.format({
                        "average_price": "₹{:.2f}",
                        "last_price": "₹{:.2f}",
                        "pnl": "₹{:.2f}",
                        "holding_value": "₹{:.2f}"
                    }),
                    use_container_width=True
                )
            else:
                st.info("No holdings available.")
        except Exception as e:
            st.error(f"Failed to fetch holdings: {e}")
            # ✅ Orders
        try:
            st.subheader("🧾 Recent Orders")
            orders = kite.orders()
            if orders:
                df_orders = pd.DataFrame(orders)
                df_orders = df_orders[["order_id", "tradingsymbol", "transaction_type", "quantity", "price", "status", "order_timestamp"]]
                df_orders = df_orders.sort_values(by="order_timestamp", ascending=False)
                st.dataframe(df_orders.head(10), use_container_width=True)
            else:
                st.info("No recent orders found.")
        except Exception as e:
            st.error(f"Failed to fetch orders: {e}")

        # ✅ Positions
        try:
            st.subheader("📌 Net Positions")
            positions = kite.positions()
            net_positions = positions['net']
            if net_positions:
                df_positions = pd.DataFrame(net_positions)
                df_positions = df_positions[["tradingsymbol", "quantity", "average_price", "last_price", "pnl"]]
                st.dataframe(
                    df_positions.style.format({
                        "average_price": "₹{:.2f}",
                        "last_price": "₹{:.2f}",
                        "pnl": "₹{:.2f}"
                    }),
                    use_container_width=True
                )
            else:
                st.info("No open positions.")
        except Exception as e:
            st.error(f"Failed to fetch positions: {e}")

                    # 📈 Live NIFTY 50 Price Chart
        st.subheader("📈 Live NIFTY 50 Chart")

       

        # Setup live prices tracking
        if 'live_prices' not in st.session_state:
            st.session_state.live_prices = []

        if 'ws_started' not in st.session_state:
            def start_websocket():
                try:
                    kws = KiteTicker(api_key, st.session_state.access_token)
                    
                    def on_ticks(ws, ticks):
                        for tick in ticks:
                            price = tick['last_price']
                            timestamp = datetime.now()
                            st.session_state.live_prices.append((timestamp, price))
                            if len(st.session_state.live_prices) > 100:
                                st.session_state.live_prices.pop(0)

                    def on_connect(ws, response):
                        ws.subscribe([256265])  # Token for NIFTY 50 spot

                    def on_close(ws, code, reason):
                        print("WebSocket closed:", reason)

                    kws.on_ticks = on_ticks
                    kws.on_connect = on_connect
                    kws.on_close = on_close
                    kws.connect(threaded=True)
                except Exception as e:
                    print("WebSocket Error:", e)

            thread = threading.Thread(target=start_websocket, daemon=True)
            thread.start()
            st.session_state.ws_started = True

        # Display the chart
        def show_chart():
            if st.session_state.live_prices:
                df = pd.DataFrame(st.session_state.live_prices, columns=["Time", "Price"])
                fig = go.Figure(data=[go.Scatter(x=df["Time"], y=df["Price"], mode="lines+markers")])
                fig.update_layout(title="NIFTY 50 Live Price", xaxis_title="Time", yaxis_title="Price", height=400)
                st.plotly_chart(fig, use_container_width=True)

        show_chart()


    else:
        st.warning("Please login to Kite Connect first.")

elif selected == "Pullback to EMA20":
    st.title("📈 Pullback to 20 EMA Scanner")

    with st.expander("ℹ Strategy Explanation"):
        st.markdown(""" 
        ### 🟢 Pullback to EMA20 (Buy the Dip)
        - Price above EMA20 and EMA50 (Uptrend)
        - Pullback to near EMA20 (within 1%)
        - *Reversal candlestick* (Bullish Engulfing or Hammer)
        - RSI > 40 for confirmation
        """)

    # List of stocks (customize as needed)
    #nifty50_stocks = [
        #'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS',
        #'LT.NS', 'SBIN.NS', 'AXISBANK.NS', 'ITC.NS', 'KOTAKBANK.NS'
        # Add more as needed
    #]

    # User input
    selected_stocks = st.multiselect("Select Stocks to Scan", nifty50_stocks, default=nifty50_stocks)

    # Date range
    end_date = datetime.today()
    start_date = end_date - timedelta(days=200)

    pullback_signals = []

    if st.button("Run Pullback Scan"):
        progress_text = "🔍 Scanning stocks..."
        progress_bar = st.progress(0)

        for i, stock in enumerate(selected_stocks):
            try:
                df = yf.download(stock, start=start_date, end=end_date, progress=False)

                if df.empty or len(df) < 60:
                    st.warning(f"{stock}: Not enough data")
                    continue

                # Calculate EMA and RSI
                #df["EMA20"] = df["Close"].ewm(span=20).mean()
                #df["EMA50"] = df["Close"].ewm(span=50).mean()
                #df["RSI"] = RSIIndicator(df["Close"], window=14).rsi()
                # Calculate indicators after downloading
                # Calculate indicators
                df["EMA20"] = df["Close"].ewm(span=20).mean()
                df["EMA50"] = df["Close"].ewm(span=50).mean()
                
                # Safely convert to 1D and compute RSI
                close_series = df[["Close"]].squeeze()
                df["RSI"] = RSIIndicator(close=close_series, window=14).rsi()



                df.dropna(inplace=True)
                if len(df) < 2:
                    continue

                # Previous and latest rows
                prev = df.iloc[-2]
                latest = df.iloc[-1]

                # Values
                prev_close = float(prev["Close"])
                prev_open = float(prev["Open"])
                latest_close = float(latest["Close"])
                latest_open = float(latest["Open"])
                latest_low = float(latest["Low"])
                latest_ema20 = float(latest["EMA20"])
                latest_ema50 = float(latest["EMA50"])
                latest_rsi = float(latest["RSI"])

                # Conditions
                in_uptrend = latest_close > latest_ema20 and latest_ema20 > latest_ema50
                near_ema20 = abs(latest_close - latest_ema20) / latest_close < 0.01

                is_bullish_engulfing = (
                    prev_close < prev_open and
                    latest_close > latest_open and
                    latest_close > prev_open and
                    latest_open < prev_close
                )

                is_hammer = (
                    latest_close > latest_open and
                    (latest_open - latest_low) > 2 * (latest_close - latest_open)
                )

                rsi_ok = latest_rsi > 40

                if in_uptrend and near_ema20 and rsi_ok and (is_bullish_engulfing or is_hammer):
                    pullback_signals.append({"Stock": stock, "Signal": "🟢 Pullback Buy"})

            except Exception as e:
                st.error(f"Error for {stock}: {e}")

            progress_bar.progress((i + 1) / len(selected_stocks))

        progress_bar.empty()

        if pullback_signals:
            st.success(f"✅ Found {len(pullback_signals)} signals:")
            st.table(pd.DataFrame(pullback_signals))
        else:
            st.info("🔎 No signals found.")






elif selected == "Golden Cross":
    st.title("📈 20/50 EMA Crossover Scanner")
    crosses_md = """
    # Golden Cross & Death Cross 📈📉
    
    ## Golden Cross 📈
    The *Golden Cross* is a bullish technical indicator that occurs when a *short-term moving average* crosses *above* a *long-term moving average*.  
    This crossover signals a potential shift to an upward trend and is often used as a buy signal.
    
    *Common Setup:*
    - Short-term MA: 20-day or 50-day EMA
    - Long-term MA: 50-day or 200-day EMA
    
    *Meaning:*  
    - Indicates growing buying momentum and possible sustained price increase.  
    - Traders often consider this a signal to enter or add to long positions.
    
    ---
    
    ## Death Cross 📉
    The *Death Cross* is a bearish technical indicator that occurs when a *short-term moving average* crosses *below* a *long-term moving average*.  
    This crossover signals a potential shift to a downward trend and is often used as a sell signal.
    
    *Common Setup:*
    - Short-term MA: 20-day or 50-day EMA
    - Long-term MA: 50-day or 200-day EMA
    
    *Meaning:*  
    - Indicates growing selling pressure and potential further declines.  
    - Traders often consider this a signal to exit or reduce long positions.
    
    ---
    
    *Example Table:*
    
    | Date       | EMA 20 | EMA 50 | Signal        |
    |------------|--------|--------|---------------|
    | 2025-07-10 | 150.2  | 151.0  | No Cross      |
    | 2025-07-11 | 151.5  | 150.9  | *Golden Cross* |
    | 2025-08-01 | 148.0  | 149.5  | *Death Cross*  |
    
    ---
    
    *Summary:*  
    - *Golden Cross:* Bullish, consider buying.  
    - *Death Cross:* Bearish, consider selling or caution.
    """
    
    # Usage example:
    # st.markdown(crosses_md)
    
    
    # List of some NIFTY 50 stocks (customize as you want)
    
    nifty50_stocks = [
        '360ONE.NS',
        '3MINDIA.NS',
        'ABB.NS',
        'ACC.NS',
        'ACMESOLAR.NS',
        'AIAENG.NS',
        'APLAPOLLO.NS',
        'AUBANK.NS',
        'AWL.NS',
        'AADHARHFC.NS',
        'AARTIIND.NS',
        'AAVAS.NS',
        'ABBOTINDIA.NS',
        'ACE.NS',
        'ADANIENSOL.NS',
        'ADANIENT.NS',
        'ADANIGREEN.NS',
        'ADANIPORTS.NS',
        'ADANIPOWER.NS',
        'ATGL.NS',
        'ABCAPITAL.NS',
        'ABFRL.NS',
        'ABREL.NS',
        'ABSLAMC.NS',
        'AEGISLOG.NS',
        'AFCONS.NS',
        'AFFLE.NS',
        'AJANTPHARM.NS',
        'AKUMS.NS',
        'APLLTD.NS',
        'ALIVUS.NS',
        'ALKEM.NS',
        'ALKYLAMINE.NS',
        'ALOKINDS.NS',
        'ARE&M.NS',
        'AMBER.NS',
        'AMBUJACEM.NS',
        'ANANDRATHI.NS',
        'ANANTRAJ.NS',
        'ANGELONE.NS',
        'APARINDS.NS',
        'APOLLOHOSP.NS',
        'APOLLOTYRE.NS',
        'APTUS.NS',
        'ASAHIINDIA.NS',
        'ASHOKLEY.NS',
        'ASIANPAINT.NS',
        'ASTERDM.NS',
        'ASTRAZEN.NS',
        'ASTRAL.NS',
        'ATUL.NS',
        'AUROPHARMA.NS',
        'AIIL.NS',
        'DMART.NS',
        'AXISBANK.NS',
        'BASF.NS',
        'BEML.NS',
        'BLS.NS',
        'BSE.NS',
        'BAJAJ-AUTO.NS',
        'BAJFINANCE.NS',
        'BAJAJFINSV.NS',
        'BAJAJHLDNG.NS',
        'BAJAJHFL.NS',
        'BALKRISIND.NS',
        'BALRAMCHIN.NS',
        'BANDHANBNK.NS',
        'BANKBARODA.NS',
        'BANKINDIA.NS',
        'MAHABANK.NS',
        'BATAINDIA.NS',
        'BAYERCROP.NS',
        'BERGEPAINT.NS',
        'BDL.NS',
        'BEL.NS',
        'BHARATFORG.NS',
        'BHEL.NS',
        'BPCL.NS',
        'BHARTIARTL.NS',
        'BHARTIHEXA.NS',
        'BIKAJI.NS',
        'BIOCON.NS',
        'BSOFT.NS',
        'BLUEDART.NS',
        'BLUESTARCO.NS',
        'BBTC.NS',
        'BOSCHLTD.NS',
        'FIRSTCRY.NS',
        'BRIGADE.NS',
        'BRITANNIA.NS',
        'MAPMYINDIA.NS',
        'CCL.NS',
        'CESC.NS',
        'CGPOWER.NS',
        'CRISIL.NS',
        'CAMPUS.NS',
        'CANFINHOME.NS',
        'CANBK.NS',
        'CAPLIPOINT.NS',
        'CGCL.NS',
        'CARBORUNIV.NS',
        'CASTROLIND.NS',
        'CEATLTD.NS',
        'CENTRALBK.NS',
        'CDSL.NS',
        'CENTURYPLY.NS',
        'CERA.NS',
        'CHALET.NS',
        'CHAMBLFERT.NS',
        'CHENNPETRO.NS',
        'CHOLAHLDNG.NS',
        'CHOLAFIN.NS',
        'CIPLA.NS',
        'CUB.NS',
        'CLEAN.NS',
        'COALINDIA.NS',
        'COCHINSHIP.NS',
        'COFORGE.NS',
        'COHANCE.NS',
        'COLPAL.NS',
        'CAMS.NS',
        'CONCORDBIO.NS',
        'CONCOR.NS',
        'COROMANDEL.NS',
        'CRAFTSMAN.NS',
        'CREDITACC.NS',
        'CROMPTON.NS',
        'CUMMINSIND.NS',
        'CYIENT.NS',
        'DCMSHRIRAM.NS',
        'DLF.NS',
        'DOMS.NS',
        'DABUR.NS',
        'DALBHARAT.NS',
        'DATAPATTNS.NS',
        'DEEPAKFERT.NS',
        'DEEPAKNTR.NS',
        'DELHIVERY.NS',
        'DEVYANI.NS',
        'DIVISLAB.NS',
        'DIXON.NS',
        'LALPATHLAB.NS',
        'DRREDDY.NS',   
        'EIDPARRY.NS',
        'EIHOTEL.NS',
        'EICHERMOT.NS',
        'ELECON.NS',
        'ELGIEQUIP.NS',
        'EMAMILTD.NS',
        'EMCURE.NS',
        'ENDURANCE.NS',
        'ENGINERSIN.NS',
        'ERIS.NS',
        'ESCORTS.NS',
        'ETERNAL.NS',
        'EXIDEIND.NS',
        'NYKAA.NS',
        'FEDERALBNK.NS',
        'FACT.NS',
        'FINCABLES.NS',
        'FINPIPE.NS',
        'FSL.NS',
        'FIVESTAR.NS',
        'FORTIS.NS',
        'GAIL.NS',
        'GVT&D.NS',
        'GMRAIRPORT.NS',
        'GRSE.NS',
        'GICRE.NS',
        'GILLETTE.NS',
        'GLAND.NS',
        'GLAXO.NS',
        'GLENMARK.NS',
        'MEDANTA.NS',
        'GODIGIT.NS',
        'GPIL.NS',
        'GODFRYPHLP.NS',
        'GODREJAGRO.NS',
        'GODREJCP.NS',
        'GODREJIND.NS',
        'GODREJPROP.NS',
        'GRANULES.NS',
        'GRAPHITE.NS',
        'GRASIM.NS',
        'GRAVITA.NS',
        'GESHIP.NS',
        'FLUOROCHEM.NS',
        'GUJGASLTD.NS',
        'GMDCLTD.NS',
        'GNFC.NS',
        'GPPL.NS',
        'GSPL.NS',
        'HEG.NS',
        'HBLENGINE.NS',
        'HCLTECH.NS',
        'HDFCAMC.NS',
        'HDFCBANK.NS',
        'HDFCLIFE.NS',
        'HFCL.NS',
        'HAPPSTMNDS.NS',
        'HAVELLS.NS',
        'HEROMOTOCO.NS',
        'HSCL.NS',
        'HINDALCO.NS',
        'HAL.NS',
        'HINDCOPPER.NS',
        'HINDPETRO.NS',
        'HINDUNILVR.NS',
        'HINDZINC.NS',
        'POWERINDIA.NS',
        'HOMEFIRST.NS',
        'HONASA.NS',
        'HONAUT.NS',
        'HUDCO.NS',
        'HYUNDAI.NS',
        'ICICIBANK.NS',
        'ICICIGI.NS',
        'ICICIPRULI.NS',
        'IDBI.NS',
        'IDFCFIRSTB.NS',
        'IFCI.NS',
        'IIFL.NS',
        'INOXINDIA.NS',
        'IRB.NS',
        'IRCON.NS',
        'ITC.NS',
        'ITI.NS',
        'INDGN.NS',
        'INDIACEM.NS',
        'INDIAMART.NS',
        'INDIANB.NS',
        'IEX.NS',
        'INDHOTEL.NS',
        'IOC.NS',
        'IOB.NS',
        'IRCTC.NS',
        'IRFC.NS',
        'IREDA.NS',
        'IGL.NS',
        'INDUSTOWER.NS',
        'INDUSINDBK.NS',
        'NAUKRI.NS',
        'INFY.NS',
        'INOXWIND.NS',
        'INTELLECT.NS',
        'INDIGO.NS',
        'IGIL.NS',
        'IKS.NS',
        'IPCALAB.NS',
        'JBCHEPHARM.NS',
        'JKCEMENT.NS',
        'JBMA.NS',
        'JKTYRE.NS',
        'JMFINANCIL.NS',
        'JSWENERGY.NS',
        'JSWHL.NS',
        'JSWINFRA.NS',
        'JSWSTEEL.NS',
        'JPPOWER.NS',
        'J&KBANK.NS',
        'JINDALSAW.NS',
        'JSL.NS',
        'JINDALSTEL.NS',
        'JIOFIN.NS',
        'JUBLFOOD.NS',
        'JUBLINGREA.NS',
        'JUBLPHARMA.NS',
        'JWL.NS',
        'JUSTDIAL.NS',
        'JYOTHYLAB.NS',
        'JYOTICNC.NS',
        'KPRMILL.NS',
        'KEI.NS',
        'KNRCON.NS',
        'KPITTECH.NS',
        'KAJARIACER.NS',
        'KPIL.NS',
        'KALYANKJIL.NS',
        'KANSAINER.NS',
        'KARURVYSYA.NS',
        'KAYNES.NS',
        'KEC.NS',
        'KFINTECH.NS',
        'KIRLOSBROS.NS',
        'KIRLOSENG.NS',
        'KOTAKBANK.NS',
        'KIMS.NS',
        'LTF.NS',
        'LTTS.NS',
        'LICHSGFIN.NS',
        'LTFOODS.NS',
        'LTIM.NS',
        'LT.NS',
        'LATENTVIEW.NS',
        'LAURUSLABS.NS',
        'LEMONTREE.NS',
        'LICI.NS',
        'LINDEINDIA.NS',
        'LLOYDSME.NS',
        'LUPIN.NS',
        'MMTC.NS',
        'MRF.NS',
        'LODHA.NS',
        'MGL.NS',
        'MAHSEAMLES.NS',
        'M&MFIN.NS',
        'M&M.NS',
        'MANAPPURAM.NS',
        'MRPL.NS',
        'MANKIND.NS',
        'MARICO.NS',
        'MARUTI.NS',
        'MASTEK.NS',
        'MFSL.NS',
        'MAXHEALTH.NS',
        'MAZDOCK.NS',
        'METROPOLIS.NS',
        'MINDACORP.NS',
        'MSUMI.NS',
        'MOTILALOFS.NS',
        'MPHASIS.NS',
        'MCX.NS',
        'MUTHOOTFIN.NS',
        'NATCOPHARM.NS',
        'NBCC.NS',
        'NCC.NS',
        'NHPC.NS',
        'NLCINDIA.NS',
        'NMDC.NS',
        'NSLNISP.NS',
        'NTPCGREEN.NS',
        'NTPC.NS',
        'NH.NS',
        'NATIONALUM.NS',
        'NAVA.NS',
        'NAVINFLUOR.NS',
        'NESTLEIND.NS',
        'NETWEB.NS',
        'NETWORK18.NS',
        'NEULANDLAB.NS',
        'NEWGEN.NS',
        'NAM-INDIA.NS',
        'NIVABUPA.NS',
        'NUVAMA.NS',
        'OBEROIRLTY.NS',
        'ONGC.NS',
        'OIL.NS',
        'OLAELEC.NS',
        'OLECTRA.NS',
        'PAYTM.NS',
        'OFSS.NS',
        'POLICYBZR.NS',
        'PCBL.NS',
        'PGEL.NS',
        'PIIND.NS',
        'PNBHOUSING.NS',
        'PNCINFRA.NS',
        'PTCIL.NS',
        'PVRINOX.NS',
        'PAGEIND.NS',
        'PATANJALI.NS',
        'PERSISTENT.NS',
        'PETRONET.NS',
        'PFIZER.NS',
        'PHOENIXLTD.NS',
        'PIDILITIND.NS',
        'PEL.NS',
        'PPLPHARMA.NS',
        'POLYMED.NS',
        'POLYCAB.NS',
        'POONAWALLA.NS',
        'PFC.NS',
        'POWERGRID.NS',
        'PRAJIND.NS',
        'PREMIERENE.NS',
        'PRESTIGE.NS',
        'PNB.NS',
        'RRKABEL.NS',
        'RBLBANK.NS',
        'RECLTD.NS',
        'RHIM.NS',
        'RITES.NS',
        'RADICO.NS',
        'RVNL.NS',
        'RAILTEL.NS',
        'RAINBOW.NS',
        'RKFORGE.NS',
        'RCF.NS',
        'RTNINDIA.NS',
        'RAYMONDLSL.NS',
        'RAYMOND.NS',
        'REDINGTON.NS',
        'RELIANCE.NS',
        'RPOWER.NS',
        'ROUTE.NS',
        'SBFC.NS',
        'SBICARD.NS',
        'SBILIFE.NS',
        'SJVN.NS',
        'SKFINDIA.NS',
        'SRF.NS',
        'SAGILITY.NS',
        'SAILIFE.NS',
        'SAMMAANCAP.NS',
        'MOTHERSON.NS',
        'SAPPHIRE.NS',
        'SARDAEN.NS',
        'SAREGAMA.NS',
        'SCHAEFFLER.NS',
        'SCHNEIDER.NS',
        'SCI.NS',
        'SHREECEM.NS',
        'RENUKA.NS',
        'SHRIRAMFIN.NS',
        'SHYAMMETL.NS',
        'SIEMENS.NS',
        'SIGNATURE.NS',
        'SOBHA.NS',
        'SOLARINDS.NS',
        'SONACOMS.NS',
        'SONATSOFTW.NS',
        'STARHEALTH.NS',
        'SBIN.NS',
        'SAIL.NS',
        'SWSOLAR.NS',
        'SUMICHEM.NS',
        'SUNPHARMA.NS',
        'SUNTV.NS',
        'SUNDARMFIN.NS',
        'SUNDRMFAST.NS',
        'SUPREMEIND.NS',
        'SUZLON.NS',
        'SWANENERGY.NS',
        'SWIGGY.NS',
        'SYNGENE.NS',
        'SYRMA.NS',
        'TBOTEK.NS',
        'TVSMOTOR.NS',
        'TANLA.NS',
        'TATACHEM.NS',
        'TATACOMM.NS',
        'TCS.NS',
        'TATACONSUM.NS',
        'TATAELXSI.NS',
        'TATAINVEST.NS',
        'TATAMOTORS.NS',
        'TATAPOWER.NS',
        'TATASTEEL.NS',
        'TATATECH.NS',
        'TTML.NS',
        'TECHM.NS',
        'TECHNOE.NS',
        'TEJASNET.NS',
        'NIACL.NS',
        'RAMCOCEM.NS',
        'THERMAX.NS',
        'TIMKEN.NS',
        'TITAGARH.NS',
        'TITAN.NS',
        'TORNTPHARM.NS',
        'TORNTPOWER.NS',
        'TARIL.NS',
        'TRENT.NS',
        'TRIDENT.NS',
        'TRIVENI.NS',
        'TRITURBINE.NS',
        'TIINDIA.NS',
        'UCOBANK.NS',
        'UNOMINDA.NS',
        'UPL.NS',
        'UTIAMC.NS',
        'ULTRACEMCO.NS',
        'UNIONBANK.NS',
        'UBL.NS',
        'UNITDSPR.NS',
        'USHAMART.NS',
        'VGUARD.NS',
        'DBREALTY.NS',
        'VTL.NS',
        'VBL.NS',
        'MANYAVAR.NS',
        'VEDL.NS',
        'VIJAYA.NS',
        'VMM.NS',
        'IDEA.NS',
        'VOLTAS.NS',
        'WAAREEENER.NS',
        'WELCORP.NS',
        'WELSPUNLIV.NS',
        'WESTLIFE.NS',
        'WHIRLPOOL.NS',
        'WIPRO.NS',
        'WOCKPHARMA.NS',
        'YESBANK.NS',
        'ZFCVINDIA.NS',
        'ZEEL.NS',
        'ZENTEC.NS',
        'ZENSARTECH.NS',
        'ZYDUSLIFE.NS',
        'ECLERX.NS',
    ]
    
    
    # User input: select stocks to scan
    selected_stocks = st.multiselect("Select Stocks to Scan", nifty50_stocks, default=nifty50_stocks)
    
    # Date range
    end_date = datetime.today()
    start_date = end_date - timedelta(days=200)
    
    signals = []
    
    if st.button("Run EMA Crossover Scan"):
        progress_text = "Scanning stocks..."
        progress_bar = st.progress(0)
    
        for i, stock in enumerate(selected_stocks):
            try:
                df = yf.download(stock, start=start_date, end=end_date, progress=False)
    
                if df.empty or len(df) < 2:
                    st.warning(f"{stock}: Not enough data")
                    continue
    
                df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()
                df["EMA50"] = df["Close"].ewm(span=50, adjust=False).mean()
    
                prev = df.iloc[-2]
                latest = df.iloc[-1]
    
                # Extract scalar values safely
                prev_ema20 = prev["EMA20"].item() if hasattr(prev["EMA20"], "item") else prev["EMA20"]
                prev_ema50 = prev["EMA50"].item() if hasattr(prev["EMA50"], "item") else prev["EMA50"]
                latest_ema20 = latest["EMA20"].item() if hasattr(latest["EMA20"], "item") else latest["EMA20"]
                latest_ema50 = latest["EMA50"].item() if hasattr(latest["EMA50"], "item") else latest["EMA50"]
    
                # Check Golden Cross
                if prev_ema20 < prev_ema50 and latest_ema20 > latest_ema50:
                    signals.append({"Stock": stock, "Signal": "📈 Golden Cross"})
    
                # Check Death Cross
                elif prev_ema20 > prev_ema50 and latest_ema20 < latest_ema50:
                    signals.append({"Stock": stock, "Signal": "📉 Death Cross"})
    
            except Exception as e:
                st.error(f"Error for {stock}: {e}")
    
            progress_bar.progress((i + 1) / len(selected_stocks))
    
        progress_bar.empty()
    
        if signals:
            st.success(f"✅ Found {len(signals)} crossover signals:")
            st.table(pd.DataFrame(signals))
        else:
            st.info("No crossover signals found.")
    

    
#############################################################################-------------------------------------------------------------------------------    
elif selected == "NIFTY PCR":
    # -------------------------------
    index_map = {
        "NIFTY 50": "^NSEI",
        "BANKNIFTY": "^NSEBANK",
        "SENSEX": "^BSESN"
    }
    selected_index = st.selectbox("Select Index", options=list(index_map.keys()), index=0)
    ticker = index_map[selected_index]

    

        # Fetch last 30 trading days of NIFTY data
    nifty = yf.download(ticker, period="1mo", interval="1d")
    nifty = nifty[["Close"]].dropna().reset_index()
    nifty.rename(columns={"Date": "date", "Close": "nifty_close"}, inplace=True)
    
    # Simulate PCR data (in real case, fetch from NSE or data vendor)
    np.random.seed(42)
    pcr_values = np.round(np.random.uniform(0.8, 1.3, size=len(nifty)), 2)
    nifty["pcr"] = pcr_values
    
    # Plot
    fig, ax1 = plt.subplots(figsize=(10, 5))
    
    # Nifty line
    ax1.set_xlabel("Date")
    ax1.set_ylabel("NIFTY Close", color="tab:blue")
    ax1.plot(nifty["date"], nifty["nifty_close"], color="tab:blue", label="NIFTY Close")
    ax1.tick_params(axis="y", labelcolor="tab:blue")
    
    # PCR on secondary y-axis
    ax2 = ax1.twinx()
    ax2.set_ylabel("PCR", color="tab:red")
    ax2.plot(nifty["date"], nifty["pcr"], color="tab:red", linestyle="--", label="PCR")
    ax2.tick_params(axis="y", labelcolor="tab:red")
    ax2.axhline(1, color='gray', linestyle='--', linewidth=0.7)
    
    # Title and legend
    fig.suptitle("📅 NIFTY Closing Price vs PCR (Simulated for 1 Month)")
    fig.tight_layout()
    st.pyplot(fig)
    
    # Show data
    with st.expander("📋 View Data Table"):
        st.dataframe(nifty)

    st.markdown("""
        ## 📘 What is NIFTY PCR (Put-Call Ratio)?
        
        The *Put-Call Ratio (PCR)* is a popular sentiment indicator used in options trading. It helps understand the *overall mood of the market, especially for indexes like **NIFTY*.
        
        ---
        
        ### 🔢 How is PCR Calculated?
        
        *PCR = Total Open Interest of Puts / Total Open Interest of Calls*
        
        - *Open Interest (OI):* Total number of outstanding contracts that are not settled.
        - A PCR > 1 means more PUTs are open → bearish sentiment
        - A PCR < 1 means more CALLs are open → bullish sentiment
        
        ---
        
        ### 📊 How to Interpret NIFTY PCR?
        
        | PCR Value | Market Sentiment | Interpretation                        |
        |-----------|------------------|----------------------------------------|
        | > 1.2     | Bearish          | Traders are hedging or expecting fall |
        | ~1.0      | Neutral          | Balanced OI, indecision               |
        | < 0.8     | Bullish          | More call writing, bullish bets       |
        
        ---
        
        ### 🧠 Why is PCR Important?
        
        - Helps identify *market sentiment*
        - Aids in *contrarian strategies* — e.g., extremely high PCR could indicate oversold conditions
        - Useful for *NIFTY and BANKNIFTY option traders*
        
        ---
        
        ### 📌 Notes:
        - PCR should not be used alone — combine with technical/fundamental indicators
        - Look at *historical PCR trends* along with current data for better decisions
        """)




    
    

    

elif selected == "Telegram Demo":
    # --- Streamlit App ---
    #st.set_page_config(page_title="Indian Market Dashboard", layout="centered")
    st.write("📈 Indian Market Dashboard")
    st.write("Live stock/index prices + Telegram update")
    
    # Load environment variables
    load_dotenv()
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN_demo")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID_demo")
    
    # Function to send a Telegram message
    def send_telegram_message(message):
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}
        r = requests.post(url, data=payload)
        return r.ok
    
    # Get stock/index data using yfinance
    def get_market_data():
        indices = {
            'NIFTY 50': '^NSEI',
            'BANK NIFTY': '^NSEBANK',
            'SENSEX': '^BSESN',
            'ADANIENT': 'ADANIENT.NS',
            'ADANIPORTS': 'ADANIPORTS.NS',
            'ASIANPAINT': 'ASIANPAINT.NS',
            'AXISBANK': 'AXISBANK.NS',
            'BAJAJ-AUTO': 'BAJAJ-AUTO.NS',
            'BAJFINANCE': 'BAJFINANCE.NS',
            'BAJAJFINSV': 'BAJAJFINSV.NS',
            'BPCL': 'BPCL.NS',
            'BHARTIARTL': 'BHARTIARTL.NS',
            'BRITANNIA': 'BRITANNIA.NS',
            'CIPLA': 'CIPLA.NS',
            'COALINDIA': 'COALINDIA.NS',
            'DIVISLAB': 'DIVISLAB.NS',
            'DRREDDY': 'DRREDDY.NS',
            'EICHERMOT': 'EICHERMOT.NS',
            'GRASIM': 'GRASIM.NS',
            'HCLTECH': 'HCLTECH.NS',
            'HDFCBANK': 'HDFCBANK.NS',
            'HDFCLIFE': 'HDFCLIFE.NS',
            'HEROMOTOCO': 'HEROMOTOCO.NS',
            'HINDALCO': 'HINDALCO.NS',
            'HINDUNILVR': 'HINDUNILVR.NS',
            'ICICIBANK': 'ICICIBANK.NS',
            'ITC': 'ITC.NS',
            'INDUSINDBK': 'INDUSINDBK.NS',
            'INFY': 'INFY.NS',
            'JSWSTEEL': 'JSWSTEEL.NS',
            'KOTAKBANK': 'KOTAKBANK.NS',
            'LT': 'LT.NS',
            'M&M': 'M&M.NS',
            'MARUTI': 'MARUTI.NS',
            'NTPC': 'NTPC.NS',
            'NESTLEIND': 'NESTLEIND.NS',
            'ONGC': 'ONGC.NS',
            'POWERGRID': 'POWERGRID.NS',
            'RELIANCE': 'RELIANCE.NS',
            'SBILIFE': 'SBILIFE.NS',
            'SBIN': 'SBIN.NS',
            'SUNPHARMA': 'SUNPHARMA.NS',
            'TCS': 'TCS.NS',
            'TATACONSUM': 'TATACONSUM.NS',
            'TATAMOTORS': 'TATAMOTORS.NS',
            'TATASTEEL': 'TATASTEEL.NS',
            'TECHM': 'TECHM.NS',
            'TITAN': 'TITAN.NS',
            'UPL': 'UPL.NS',
            'ULTRACEMCO': 'ULTRACEMCO.NS',
            'WIPRO': 'WIPRO.NS'
        }
    
        message = "📊 Indian Market Snapshot 📈\n\n"
        market_list = []
    
        for name, symbol in indices.items():
            ticker = yf.Ticker(symbol)
            info = ticker.info
    
            price = info.get("regularMarketPrice")
            change = info.get("regularMarketChange")
            percent = info.get("regularMarketChangePercent")
            volume = info.get("volume")
    
            if price is not None and percent is not None:
                row = {
                    "Name": name,
                    "Price (₹)": round(price, 2),
                    "Change": f"{change:+.2f}",
                    "Change %": f"{percent:+.2f}%",
                    "Volume": volume if volume is not None else "N/A",
                    "percent_numeric": percent
                }
                market_list.append(row)
    
        # Sort by Change % numeric descending
        market_list.sort(key=lambda x: x["percent_numeric"], reverse=True)
    
        # Build Telegram message from sorted data
        message = "📊 Indian Market Snapshot 📈\n\n"
        for row in market_list:
            emoji = "🟢" if row["percent_numeric"] >= 0 else "🔴"
            message += (f"{emoji} {row['Name']}: ₹{row['Price (₹)']:.2f} "
                        f"({row['Change']}, {row['Change %']}), Vol: {row['Volume']}\n")
    
        # Remove helper key before returning data for DataFrame
        for row in market_list:
            del row["percent_numeric"]
    
        return market_list, message
    # Fetch data
    market_data, message = get_market_data()
    
    # Convert to DataFrame
    df = pd.DataFrame(market_data)
    
    # Convert 'Change %' to float for sorting (strip % sign)
    df["Change % (numeric)"] = df["Change %"].str.replace('%', '').astype(float)
    
    # Sort by Change % descending (highest first)
    df = df.sort_values(by="Change % (numeric)", ascending=False)
    
    # Drop the helper column before display (optional)
    df = df.drop(columns=["Change % (numeric)"])
    
    # Color formatting: red for negative, green for positive
    def highlight_change(val):
        try:
            val_float = float(val.strip('%'))
            return 'color: green;' if val_float > 0 else 'color: red;'
        except:
            return ''
    
    # Display styled dataframe
    #st.dataframe(
       # df.style.applymap(highlight_change, subset=["Change", "Change %"])
    #)
    # Convert to DataFrame
    df = pd.DataFrame(market_data)
    
    # Convert 'Change %' to float for sorting (strip % sign and convert)
    df["Change % (numeric)"] = df["Change %"].str.replace('%', '', regex=False).astype(float)
    
    # Sort by % change descending
    df = df.sort_values(by="Change % (numeric)", ascending=False)
    
    # Drop the helper column before display
    df_display = df.drop(columns=["Change % (numeric)"])
    
    # Apply text color formatting
    def text_color(row):
        color = 'color: green' if row["Change %"].startswith('+') else 'color: red'
        return [color] * len(row)
    
    # Display styled table
    #st.dataframe(df_display.style.apply(row_color, axis=1))
    # Display styled dataframe in Streamlit with colored text
    st.dataframe(df_display.style.apply(text_color, axis=1))
    send_telegram_message(message)
    # Refresh every 5 minutes
    st_autorefresh(interval=5 * 60 * 1000, key="datarefresh")
    import yfinance as yf

    nifty50 = yf.Ticker("^NSEI").info["regularMarketPrice"]
    banknifty = yf.Ticker("^NSEBANK").info["regularMarketPrice"]
    midcap = yf.Ticker("^NSEMDCP50").info["regularMarketPrice"]
    
    message = f"""📊 NIFTY Index Update\n
    🔹 NIFTY 50: {nifty50}
    🔹 BANKNIFTY: {banknifty}
    🔹 MIDCAP 50: {midcap}
    """
    
    #send_telegram_message(message)
    def get_index_data(ticker_symbol, name):
        ticker = yf.Ticker(ticker_symbol)
        data = ticker.history(period="2d", interval="1d")
        if len(data) < 2:
            return f"{name}: Data not available"
    
        latest = data.iloc[-1]
        prev = data.iloc[-2]
    
        current = latest["Close"]
        change = current - prev["Close"]
        pct_change = (change / prev["Close"]) * 100
        volume = int(latest["Volume"])
    
        return f"{name}: ₹{current:,.2f} ({change:+.2f}, {pct_change:+.2f}%), Vol: {volume}"

    # --- Indices to Monitor ---
    index_list = [
        ("^NSEI", "NIFTY 50"),
        ("^NSEBANK", "BANK NIFTY"),
        ("^CNXIT", "NIFTY IT"),
        ("^NSEMDCP50", "MIDCAP 50"),
    ]
    
    # --- Prepare message ---
    message = "📊 NIFTY Index Snapshot\n\n"
    for symbol, name in index_list:
        line = get_index_data(symbol, name)
        message += line + "\n"
    
    # --- Send to Telegram ---
    #send_to_telegram(message, BOT_TOKEN, CHAT_ID)
    send_telegram_message(message)

   # from telegram import Bot

    #def send_to_telegram(message, bot_token, channel_id):
        #bot = Bot(token=bot_token)
        #bot.send_message(chat_id=channel_id, text=message, parse_mode='Markdown')
    #send_to_telegram(message, BOT_TOKEN, CHAT_ID)

    #BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN_demo")
    #CHAT_ID = os.getenv("TELEGRAM_CHAT_ID_demo")

    #message = get_nifty_indices()
    #send_to_telegram(message, BOT_TOKEN, CHAT_ID)
    
    



    
    # Send update to Telegram
    
    # Display in Streamlit
    #st.table(market_data)
    
    # Manual send button
    if st.button("📤 Send Market Data to Telegram"):
        success = send_telegram_message(message)
        if success:
            st.success("Message sent to Telegram successfully!")
        else:
            st.error("Failed to send message. Check bot token and chat ID.")

elif selected == "NIFTY OI,PCR,D ":
    st.title("📊 NIFTY OI, PCR & Market Direction")

# NSE request setup
session = requests.Session()
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, /",
    "Referer": "https://www.nseindia.com/",
    "Accept-Language": "en-US,en;q=0.9",
}

# Helper function to safely fetch JSON
def safe_get_json(url, retries=3, delay=2):
    for _ in range(retries):
        try:
            resp = session.get(url, headers=HEADERS, timeout=10)
            if resp.status_code == 200 and resp.text.strip().startswith("{"):
                return resp.json()
        except Exception:
            pass
        time.sleep(delay)
    return None

# Function to fetch OI, PCR, direction
def fetch_oi_data(symbol):
    data = {"Symbol": symbol, "Call OI": None, "Put OI": None, "PCR": None, "Direction": None}
    try:
        opt_url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
        opt_resp = safe_get_json(opt_url)

        if not opt_resp or "records" not in opt_resp:
            data["Direction"] = "Error: Option chain data unavailable"
            return data

        records = opt_resp["records"]["data"]
        call_oi = sum(d["CE"]["openInterest"] for d in records if "CE" in d)
        put_oi = sum(d["PE"]["openInterest"] for d in records if "PE" in d)
        data["Call OI"] = call_oi
        data["Put OI"] = put_oi
        data["PCR"] = round(put_oi / call_oi, 2) if call_oi else None

        # Direction logic
        pcr = data["PCR"]
        if pcr is None:
            data["Direction"] = "No Data"
        elif pcr > 1.3:
            data["Direction"] = "📈 Bullish (Overbought)"
        elif 0.7 <= pcr <= 1.3:
            data["Direction"] = "⚖ Neutral / Stable"
        elif pcr < 0.7:
            data["Direction"] = "📉 Bearish / Weak"
        else:
            data["Direction"] = "Sideways"
    except Exception as e:
        data["Direction"] = f"Error: {str(e)}"

    return data


# --- Streamlit UI ---
symbol = st.selectbox("Select Index", ["NIFTY", "BANKNIFTY"])
if st.button("Fetch Live Data"):
    with st.spinner("Fetching live data from NSE..."):
        result = fetch_oi_data(symbol)
        time.sleep(1)
        st.success("Data fetched successfully ✅")

        df = pd.DataFrame([result])
        st.table(df)

        # Optional: Display summary text
        st.subheader("📊 Summary")
        st.markdown(f"""
        - *Symbol:* {symbol}  
        - *Total Call OI:* {result['Call OI']:,}  
        - *Total Put OI:* {result['Put OI']:,}  
        - *PCR:* {result['PCR']}  
        - *Market Direction:* {result['Direction']}  
        """)
    

elif selected == "Swing SMA44 Strategy":
    def scan_bhanushali_strategy(stock):
        # Download historical stock data
        df = yf.download(stock, period='90d', interval='1d')
        if df.empty:
            return None  # Skip if no data returned
    
        # Calculate the 44-period SMA
        df['SMA44'] = df['Close'].rolling(window=44).mean()
    
        # Drop rows with NaN values (if any)
        df.dropna(inplace=True)
    
        if len(df) < 2:
            return None  # Not enough data
    
        last_candle = df.iloc[-1]  # Get the most recent candle (row)
        prev_candle = df.iloc[-2]  # Get the previous candle (row)
    
        # Ensure you're working with scalar values
        low = last_candle['Low']
        close = last_candle['Close']
        sma44 = last_candle['SMA44']
    
        # Ensure values are scalar (individual numbers)
        if isinstance(low, pd.Series): low = low.values[0]
        if isinstance(close, pd.Series): close = close.values[0]
        if isinstance(sma44, pd.Series): sma44 = sma44.values[0]
    
        # Condition: low < SMA44 < close (candle near rising 44 SMA)
        if low < sma44 < close:
            # Buy above the high of the candle, stoploss below the low of the candle
            #entry = last_candle['High']
            #stoploss = low
            entry = float(last_candle['High'])       # entry as scalar
            stoploss = float(last_candle['Low'])     # stoploss as scalar
    
    
            # Calculate targets based on a 1:2 and 1:3 risk-reward ratio
            target1 = entry + (entry - stoploss) * 2
            target2 = entry + (entry - stoploss) * 3
    
            # Return a dictionary with the results
            return {
                'symbol': stock,
                'entry': round(entry, 2),
                'stoploss': round(stoploss, 2),
                'target_1_2': round(target1, 2),
                'target_1_3': round(target2, 2)
            }
    
        return None

    
    
    # Example usage with a list of NIFTY 100 stocks
    #nifty_100 = [
        
    nifty_100 = [
    '360ONE.NS',
    '3MINDIA.NS',
    'ABB.NS',
    'ACC.NS',
    'ACMESOLAR.NS',
    'AIAENG.NS',
    'APLAPOLLO.NS',
    'AUBANK.NS',
    'AWL.NS',
    'AADHARHFC.NS',
    'AARTIIND.NS',
    'AAVAS.NS',
    'ABBOTINDIA.NS',
    'ACE.NS',
    'ADANIENSOL.NS',
    'ADANIENT.NS',
    'ADANIGREEN.NS',
    'ADANIPORTS.NS',
    'ADANIPOWER.NS',
    'ATGL.NS',
    'ABCAPITAL.NS',
    'ABFRL.NS',
    'ABREL.NS',
    'ABSLAMC.NS',
    'AEGISLOG.NS',
    'AFCONS.NS',
    'AFFLE.NS',
    'AJANTPHARM.NS',
    'AKUMS.NS',
    'APLLTD.NS',
    'ALIVUS.NS',
    'ALKEM.NS',
    'ALKYLAMINE.NS',
    'ALOKINDS.NS',
    'ARE&M.NS',
    'AMBER.NS',
    'AMBUJACEM.NS',
    'ANANDRATHI.NS',
    'ANANTRAJ.NS',
    'ANGELONE.NS',
    'APARINDS.NS',
    'APOLLOHOSP.NS',
    'APOLLOTYRE.NS',
    'APTUS.NS',
    'ASAHIINDIA.NS',
    'ASHOKLEY.NS',
    'ASIANPAINT.NS',
    'ASTERDM.NS',
    'ASTRAZEN.NS',
    'ASTRAL.NS',
    'ATUL.NS',
    'AUROPHARMA.NS',
    'AIIL.NS',
    'DMART.NS',
    'AXISBANK.NS',
    'BASF.NS',
    'BEML.NS',
    'BLS.NS',
    'BSE.NS',
    'BAJAJ-AUTO.NS',
    'BAJFINANCE.NS',
    'BAJAJFINSV.NS',
    'BAJAJHLDNG.NS',
    'BAJAJHFL.NS',
    'BALKRISIND.NS',
    'BALRAMCHIN.NS',
    'BANDHANBNK.NS',
    'BANKBARODA.NS',
    'BANKINDIA.NS',
    'MAHABANK.NS',
    'BATAINDIA.NS',
    'BAYERCROP.NS',
    'BERGEPAINT.NS',
    'BDL.NS',
    'BEL.NS',
    'BHARATFORG.NS',
    'BHEL.NS',
    'BPCL.NS',
    'BHARTIARTL.NS',
    'BHARTIHEXA.NS',
    'BIKAJI.NS',
    'BIOCON.NS',
    'BSOFT.NS',
    'BLUEDART.NS',
    'BLUESTARCO.NS',
    'BBTC.NS',
    'BOSCHLTD.NS',
    'FIRSTCRY.NS',
    'BRIGADE.NS',
    'BRITANNIA.NS',
    'MAPMYINDIA.NS',
    'CCL.NS',
    'CESC.NS',
    'CGPOWER.NS',
    'CRISIL.NS',
    'CAMPUS.NS',
    'CANFINHOME.NS',
    'CANBK.NS',
    'CAPLIPOINT.NS',
    'CGCL.NS',
    'CARBORUNIV.NS',
    'CASTROLIND.NS',
    'CEATLTD.NS',
    'CENTRALBK.NS',
    'CDSL.NS',
    'CENTURYPLY.NS',
    'CERA.NS',
    'CHALET.NS',
    'CHAMBLFERT.NS',
    'CHENNPETRO.NS',
    'CHOLAHLDNG.NS',
    'CHOLAFIN.NS',
    'CIPLA.NS',
    'CUB.NS',
    'CLEAN.NS',
    'COALINDIA.NS',
    'COCHINSHIP.NS',
    'COFORGE.NS',
    'COHANCE.NS',
    'COLPAL.NS',
    'CAMS.NS',
    'CONCORDBIO.NS',
    'CONCOR.NS',
    'COROMANDEL.NS',
    'CRAFTSMAN.NS',
    'CREDITACC.NS',
    'CROMPTON.NS',
    'CUMMINSIND.NS',
    'CYIENT.NS',
    'DCMSHRIRAM.NS',
    'DLF.NS',
    'DOMS.NS',
    'DABUR.NS',
    'DALBHARAT.NS',
    'DATAPATTNS.NS',
    'DEEPAKFERT.NS',
    'DEEPAKNTR.NS',
    'DELHIVERY.NS',
    'DEVYANI.NS',
    'DIVISLAB.NS',
    'DIXON.NS',
    'LALPATHLAB.NS',
    'DRREDDY.NS',
    'DUMMYABFRL.NS',
    'DUMMYSIEMS.NS',
    'DUMMYRAYMN.NS',
    'EIDPARRY.NS',
    'EIHOTEL.NS',
    'EICHERMOT.NS',
    'ELECON.NS',
    'ELGIEQUIP.NS',
    'EMAMILTD.NS',
    'EMCURE.NS',
    'ENDURANCE.NS',
    'ENGINERSIN.NS',
    'ERIS.NS',
    'ESCORTS.NS',
    'ETERNAL.NS',
    'EXIDEIND.NS',
    'NYKAA.NS',
    'FEDERALBNK.NS',
    'FACT.NS',
    'FINCABLES.NS',
    'FINPIPE.NS',
    'FSL.NS',
    'FIVESTAR.NS',
    'FORTIS.NS',
    'GAIL.NS',
    'GVT&D.NS',
    'GMRAIRPORT.NS',
    'GRSE.NS',
    'GICRE.NS',
    'GILLETTE.NS',
    'GLAND.NS',
    'GLAXO.NS',
    'GLENMARK.NS',
    'MEDANTA.NS',
    'GODIGIT.NS',
    'GPIL.NS',
    'GODFRYPHLP.NS',
    'GODREJAGRO.NS',
    'GODREJCP.NS',
    'GODREJIND.NS',
    'GODREJPROP.NS',
    'GRANULES.NS',
    'GRAPHITE.NS',
    'GRASIM.NS',
    'GRAVITA.NS',
    'GESHIP.NS',
    'FLUOROCHEM.NS',
    'GUJGASLTD.NS',
    'GMDCLTD.NS',
    'GNFC.NS',
    'GPPL.NS',
    'GSPL.NS',
    'HEG.NS',
    'HBLENGINE.NS',
    'HCLTECH.NS',
    'HDFCAMC.NS',
    'HDFCBANK.NS',
    'HDFCLIFE.NS',
    'HFCL.NS',
    'HAPPSTMNDS.NS',
    'HAVELLS.NS',
    'HEROMOTOCO.NS',
    'HSCL.NS',
    'HINDALCO.NS',
    'HAL.NS',
    'HINDCOPPER.NS',
    'HINDPETRO.NS',
    'HINDUNILVR.NS',
    'HINDZINC.NS',
    'POWERINDIA.NS',
    'HOMEFIRST.NS',
    'HONASA.NS',
    'HONAUT.NS',
    'HUDCO.NS',
    'HYUNDAI.NS',
    'ICICIBANK.NS',
    'ICICIGI.NS',
    'ICICIPRULI.NS',
    'IDBI.NS',
    'IDFCFIRSTB.NS',
    'IFCI.NS',
    'IIFL.NS',
    'INOXINDIA.NS',
    'IRB.NS',
    'IRCON.NS',
    'ITC.NS',
    'ITI.NS',
    'INDGN.NS',
    'INDIACEM.NS',
    'INDIAMART.NS',
    'INDIANB.NS',
    'IEX.NS',
    'INDHOTEL.NS',
    'IOC.NS',
    'IOB.NS',
    'IRCTC.NS',
    'IRFC.NS',
    'IREDA.NS',
    'IGL.NS',
    'INDUSTOWER.NS',
    'INDUSINDBK.NS',
    'NAUKRI.NS',
    'INFY.NS',
    'INOXWIND.NS',
    'INTELLECT.NS',
    'INDIGO.NS',
    'IGIL.NS',
    'IKS.NS',
    'IPCALAB.NS',
    'JBCHEPHARM.NS',
    'JKCEMENT.NS',
    'JBMA.NS',
    'JKTYRE.NS',
    'JMFINANCIL.NS',
    'JSWENERGY.NS',
    'JSWHL.NS',
    'JSWINFRA.NS',
    'JSWSTEEL.NS',
    'JPPOWER.NS',
    'J&KBANK.NS',
    'JINDALSAW.NS',
    'JSL.NS',
    'JINDALSTEL.NS',
    'JIOFIN.NS',
    'JUBLFOOD.NS',
    'JUBLINGREA.NS',
    'JUBLPHARMA.NS',
    'JWL.NS',
    'JUSTDIAL.NS',
    'JYOTHYLAB.NS',
    'JYOTICNC.NS',
    'KPRMILL.NS',
    'KEI.NS',
    'KNRCON.NS',
    'KPITTECH.NS',
    'KAJARIACER.NS',
    'KPIL.NS',
    'KALYANKJIL.NS',
    'KANSAINER.NS',
    'KARURVYSYA.NS',
    'KAYNES.NS',
    'KEC.NS',
    'KFINTECH.NS',
    'KIRLOSBROS.NS',
    'KIRLOSENG.NS',
    'KOTAKBANK.NS',
    'KIMS.NS',
    'LTF.NS',
    'LTTS.NS',
    'LICHSGFIN.NS',
    'LTFOODS.NS',
    'LTIM.NS',
    'LT.NS',
    'LATENTVIEW.NS',
    'LAURUSLABS.NS',
    'LEMONTREE.NS',
    'LICI.NS',
    'LINDEINDIA.NS',
    'LLOYDSME.NS',
    'LUPIN.NS',
    'MMTC.NS',
    'MRF.NS',
    'LODHA.NS',
    'MGL.NS',
    'MAHSEAMLES.NS',
    'M&MFIN.NS',
    'M&M.NS',
    'MANAPPURAM.NS',
    'MRPL.NS',
    'MANKIND.NS',
    'MARICO.NS',
    'MARUTI.NS',
    'MASTEK.NS',
    'MFSL.NS',
    'MAXHEALTH.NS',
    'MAZDOCK.NS',
    'METROPOLIS.NS',
    'MINDACORP.NS',
    'MSUMI.NS',
    'MOTILALOFS.NS',
    'MPHASIS.NS',
    'MCX.NS',
    'MUTHOOTFIN.NS',
    'NATCOPHARM.NS',
    'NBCC.NS',
    'NCC.NS',
    'NHPC.NS',
    'NLCINDIA.NS',
    'NMDC.NS',
    'NSLNISP.NS',
    'NTPCGREEN.NS',
    'NTPC.NS',
    'NH.NS',
    'NATIONALUM.NS',
    'NAVA.NS',
    'NAVINFLUOR.NS',
    'NESTLEIND.NS',
    'NETWEB.NS',
    'NETWORK18.NS',
    'NEULANDLAB.NS',
    'NEWGEN.NS',
    'NAM-INDIA.NS',
    'NIVABUPA.NS',
    'NUVAMA.NS',
    'OBEROIRLTY.NS',
    'ONGC.NS',
    'OIL.NS',
    'OLAELEC.NS',
    'OLECTRA.NS',
    'PAYTM.NS',
    'OFSS.NS',
    'POLICYBZR.NS',
    'PCBL.NS',
    'PGEL.NS',
    'PIIND.NS',
    'PNBHOUSING.NS',
    'PNCINFRA.NS',
    'PTCIL.NS',
    'PVRINOX.NS',
    'PAGEIND.NS',
    'PATANJALI.NS',
    'PERSISTENT.NS',
    'PETRONET.NS',
    'PFIZER.NS',
    'PHOENIXLTD.NS',
    'PIDILITIND.NS',
    'PEL.NS',
    'PPLPHARMA.NS',
    'POLYMED.NS',
    'POLYCAB.NS',
    'POONAWALLA.NS',
    'PFC.NS',
    'POWERGRID.NS',
    'PRAJIND.NS',
    'PREMIERENE.NS',
    'PRESTIGE.NS',
    'PNB.NS',
    'RRKABEL.NS',
    'RBLBANK.NS',
    'RECLTD.NS',
    'RHIM.NS',
    'RITES.NS',
    'RADICO.NS',
    'RVNL.NS',
    'RAILTEL.NS',
    'RAINBOW.NS',
    'RKFORGE.NS',
    'RCF.NS',
    'RTNINDIA.NS',
    'RAYMONDLSL.NS',
    'RAYMOND.NS',
    'REDINGTON.NS',
    'RELIANCE.NS',
    'RPOWER.NS',
    'ROUTE.NS',
    'SBFC.NS',
    'SBICARD.NS',
    'SBILIFE.NS',
    'SJVN.NS',
    'SKFINDIA.NS',
    'SRF.NS',
    'SAGILITY.NS',
    'SAILIFE.NS',
    'SAMMAANCAP.NS',
    'MOTHERSON.NS',
    'SAPPHIRE.NS',
    'SARDAEN.NS',
    'SAREGAMA.NS',
    'SCHAEFFLER.NS',
    'SCHNEIDER.NS',
    'SCI.NS',
    'SHREECEM.NS',
    'RENUKA.NS',
    'SHRIRAMFIN.NS',
    'SHYAMMETL.NS',
    'SIEMENS.NS',
    'SIGNATURE.NS',
    'SOBHA.NS',
    'SOLARINDS.NS',
    'SONACOMS.NS',
    'SONATSOFTW.NS',
    'STARHEALTH.NS',
    'SBIN.NS',
    'SAIL.NS',
    'SWSOLAR.NS',
    'SUMICHEM.NS',
    'SUNPHARMA.NS',
    'SUNTV.NS',
    'SUNDARMFIN.NS',
    'SUNDRMFAST.NS',
    'SUPREMEIND.NS',
    'SUZLON.NS',
    'SWANENERGY.NS',
    'SWIGGY.NS',
    'SYNGENE.NS',
    'SYRMA.NS',
    'TBOTEK.NS',
    'TVSMOTOR.NS',
