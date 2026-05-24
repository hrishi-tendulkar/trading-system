# Tradeable Board

## Date

2026-05-22

## Universe

`S&P 100 + ETF sleeve`

## Objective

Produce a small next-week board that is actually usable in the real market.

This board separates:

- `ETF sleeve`: cleaner market or sector exposure
- `Single-name sleeve`: more selective stock entries

## ETF Sleeve

| Ticker | Strategy | Action | Entry | Stop | Target | Why it matters |
|---|---|---|---|---|---|---|
| XLK | ETF rotation | Buy now | $179-$180 | $166 | $185 | Stronger group-level trend expression with lower single-name event risk |
| QQQ | ETF rotation | Buy now | $713-$718 | $683 | $731 | Stronger group-level trend expression with lower single-name event risk |

## Single-Name Sleeve: Buy On Pullback

| Ticker | Strategy | Action | Entry | Stop | Target | Why it matters |
|---|---|---|---|---|---|---|
| CVS | Constructive pullback continuation | Buy on pullback | $92 | $81 | $98 | Stock remains stronger than market and/or sector while offering a cleaner reset than chase entries |
| UNH | Constructive pullback continuation | Buy on pullback | $384 | $331 | $405 | Stock remains stronger than market and/or sector while offering a cleaner reset than chase entries |

## Single-Name Sleeve: Wait For Pullback

| Ticker | Strategy | Action | Pullback Zone | Cancel Level | Why it matters |
|---|---|---|---|---|---|
| INTC | Extended strength, wait for pullback | Wait for pullback | $109 | $99 | Strong stock, but the current entry is too stretched to justify fresh buying today |
| TXN | Extended strength, wait for pullback | Wait for pullback | $291 | $280 | Strong stock, but the current entry is too stretched to justify fresh buying today |
| LRCX | Extended strength, wait for pullback | Wait for pullback | $280 | $265 | Strong stock, but the current entry is too stretched to justify fresh buying today |

## Single-Name Sleeve: Wait For Confirmation

| Ticker | Strategy | Action | Entry Trigger | Stop | Target | Why it matters |
|---|---|---|---|---|---|---|
| AMD | Breakout confirmation | Wait for confirmation | $481 | $375 | $519 | Strong candidate, but should prove itself through price before capital is deployed |
| MU | Breakout confirmation | Wait for confirmation | $819 | $609 | $890 | Strong candidate, but should prove itself through price before capital is deployed |
| QCOM | Breakout confirmation | Wait for confirmation | $248 | $175 | $272 | Strong candidate, but should prove itself through price before capital is deployed |

## Practical Read

- `Buy now` is mostly an ETF decision right now.
- `Buy on pullback` is the main single-name entry style currently supported by the research and replay.
- `Wait for pullback` means the stock is strong, but the current price is too stretched to chase.
- `Wait for confirmation` is not a junk bucket. It is a live watchlist for names that could become actionable soon.

## Current Top 5 Attention List

1. `XLK`
2. `QQQ`
3. `CVS`
4. `UNH`
5. `INTC`

## Operating View

- The engine is saying `use ETFs for immediate exposure` and `be patient with most single names`.
- A small board is a feature, not a bug. The system should earn selectivity before it earns trust.

## Important Limits

- This is still based mostly on daily-price-only research logic.
- The engine is more selective than before, but it is still in `research mode`, not full `live-ready` confidence mode.
- Single-name `Buy now` is still not strong enough to be handed out casually.