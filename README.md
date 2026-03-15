# Stock Portfolio Analyser V2

A Python command-line stock portfolio management system with live market data, performance analysis, and data persistence. Tracks your investments, monitor your positions, and make data-driven decisions with real-time market data.

## Features
- **Add Stocks:** Register stocks with ticker, buy price and shares
- **View Portfolio:** Display all holdings with total value
- **View Single Stock:** Instant O(1) lookup by ticker
- **Search Stock:** Live market data via yfinance API
- **Remove Stock:** Remove holdings with confirmation prompt
- **Portfolio Analysis:** Live P&L calculations with real-time prices
- **Pandas Analysis:** Data analysis submenu with filtering and sorting
- **CSV Export:** Export portfolio data to CSV via Pandas
- **JSON Persistence:** Auto-save on every change with backup system
- **Corruption Handling:** Graceful recovery from corrupted save files

## Tech Stack
- Python 3 (OOP — Inheritance & Composition)
- yfinance (Live market data)
- Pandas (Data analysis & CSV export)
- JSON (Data persistence)

## Project Structure
| Class | Purpose |
|-------|---------|
| `Asset` | Parent class — name, buy_price, shares, total_value() |
| `Stock` | Child class — inherits Asset, adds ticker |
| `Portfolio` | Composition class — holds Stock objects in dictionary |

## Planned Features
- [ ] Matplotlib/Plotly visualisations
- [ ] Portfolio performance charts
- [ ] Gain/loss visualisations
- [ ] Trending stocks feature
- [ ] Professional screenshots and demos
- ✅ JSON persistence (save/load portfolio)
- ✅ Error handling for user input / data requests
- ✅ CSV export
- ✅ Live price API integration
- ✅ Portfolio analysis and performance metrics
