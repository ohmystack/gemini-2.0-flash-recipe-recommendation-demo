# Smart Recipe Recommendation (Demo)

A Demo for Gemini 2.0 Flash, showing how to use function calls and structured data.

Author: @ohmystack

## Installation

```bash
pip install google-generativeai

# (Optional) Get rid of annoying warnings, we should downgrade grpcio, which will be fixed in the future
pip uninstall grpcio grpcio-status
pip install grpcio==1.60.1 grpcio-status==1.60.1
```

## Run

```bash
export GOOGLE_API_KEY='<get from https://aistudio.google.com/apikey >'
python recipe-recommendation.py
```

Result would be:

```
Recommended Recipe: [{'name': 'Vegetarian Pasta Primavera', 'ingredients': ['pasta', 'vegetables'], 'dietary_restrictions': ['vegetarian']}]
```
