# Data and license

## Data

The model dictionaries and caliber list ship inside the package (`gunsnprices/data/`). The same data, with listing
counts and price levels, is published as open datasets:

- MCP server for AI assistants (Claude, Cursor, VS Code), built on this parser: [gunsnprices-mcp](https://github.com/gunsnprices/gunsnprices-mcp)
- Hugging Face: [gunsnprices/firearm-calibers](https://huggingface.co/datasets/gunsnprices/firearm-calibers),
  [gunsnprices/firearm-models](https://huggingface.co/datasets/gunsnprices/firearm-models)
- GitHub: [gunsnprices/firearm-datasets](https://github.com/gunsnprices/firearm-datasets)
- Kaggle: [gunsnprices](https://www.kaggle.com/gunsnprices)

## Limitations

- Titles from US retailers, in English.
- Models are covered for the 50 brands above. Other brands still get calibers and numbers.
- Built for firearms and ammunition. Magazines, parts and accessories get calibers and numbers but no model.

## License

The code is under the [MIT License](https://github.com/gunsnprices/gunsnprices-python/blob/main/LICENSE). The data files in `gunsnprices/data/` are under
[CC BY 4.0](https://github.com/gunsnprices/gunsnprices-python/blob/main/LICENSE-DATA): you can use them for anything, including commercial use, if you credit
**GunsNPrices (gunsnprices.com)** with a link.

Questions, corrections and missing models: open an issue or write to app@gunsnprices.com.
Current gun and ammo prices: [gunsnprices.com](https://gunsnprices.com).
