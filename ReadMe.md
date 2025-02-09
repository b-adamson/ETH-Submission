RugPullRadar:

Billy Adamson
Artharv Gupta
Julian Huddart

Uses a random forest LLM to analyse memecoin history in terms of past price and google search analytics of the coin ticker code (e.g. $USDC)
If its about to be rugpulled closer to 100, if stable closer to 0

Build instructions:

1. clone the repo
2. npm init
3. follow the instructions
4. ensure Python is installed (3.12)
5. npm install @solana/web3.js @project-serum/borsh node-fetch fs
6. pip install numpy matplotlib scikit-learn pytrends pandas
7. go into frontend/server.js and change PORT to a suitable value, like 5500
8. go into frontend/base.html and change every instance of http://localhost:5500/save-search to the correct port value (there are 2)
9. node frontend/server.js
10. start the port, in vscode this is in the bottom right
11. navigate to frontend/html
12. your in!

try:

So11111111111111111111111111111111111111112
6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN
FUAfBo2jgks6gB4Z4LfZkqSZgzNucisEHqnNebaRxM1P
EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
BvSyXBvy76mUgzLSbvvT4NQw5rSM4P5zAsdnvqUJpump
SsKFgDPEqyzAM8nWPiiX7MGY7iNDTEX6DxRdxmkpump

Use solscan or explorer.solana to find mint addresses of popular solana coins

These include trump coin, melania coin, usdc

USDC is lower than TRUMP coin because USDC is more stable than TRUMP, and our ML model naturally predicts that

As of 09/02/25 we got these results:

@DOGE = 0.17
SDOGE = 0.13
SOL = 0.08
TRUMP = 0.28
USDT = 0.01

Not bad!

plotcsv.py plots a csv of data extracted from the ML model, is optional and doesn't run on its own
