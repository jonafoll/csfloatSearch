﻿# CSFloat search tool

A Python script for fetching listings on CSFloat.com. This tool allows you to easily check multiple seeds for a specific skin without manually searching each one.

# Features
- Search for listings by paint_seed, def_index, and paint_index.
- Filter results by max_price, min_price, max_float, and min_float.
- Choose between simple mode (count of unique listings) and detailed mode (full listing details).

1.  Add your CSFloat API key to the .env file. You can find your API key under the Developer tab on your CSFloat profile.
    ```
    CSFLOAT_API_KEY=your_api_key_here
    ```
2. Execute the script by running:
    ```
    python main.py
    ```
3. Search for the skin on CSFloat and inspect the URL to find the def_index and paint_index values.
4. Input a list of paint_seed values (comma or space-separated).
5. Optionally, specify values for max_price, min_price, max_float, and min_float to filter the results.

# Notes
You will get rate limited if you use it a lot in a short amount of time. 
## Recommended workflow
- Use simple mode to quickly check a list of seeds. Then search up the resulting seeds on CSFloat for more info.
