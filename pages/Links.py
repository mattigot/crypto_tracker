import streamlit as st  # pip install streamlit

# Define the emojis and corresponding links
# https://carpedm20.github.io/emoji/
#https://www.freecodecamp.org/news/all-emojis-emoji-list-for-copy-and-paste/#zodiac
page_links = [
        ["🪙", "Coinmarketcap", "https://coinmarketcap.com"],
        ["🤝", "Tradingview", "https://www.tradingview.com/"],
        ["📹", "Suppoman Twitch", "https://www.twitch.tv/suppomancrypto"],
        ["🎵", "Suppoman Youtube", "https://www.youtube.com/@SuppomanCrypto"],
        ["💰", "Crypto Master", "https://cryptomaster.co.il"],
        ["\U0001F600", "Crypto Master", "https://cryptomaster.co.il"],
    ]

# Display the links with emojis
for page in page_links:
    st.write(f"{page[0]} [{page[1]}]({page[2]})")

