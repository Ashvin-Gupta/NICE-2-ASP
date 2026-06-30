# NICE2ASP: Clinical Guidelines to Answer Set Programming

A pipeline that translates NICE cancer clinical guidelines into Answer Set Programming (ASP) rules using the Claude API, then applies those rules to patient vignettes to generate clinical recommendations.

Supports two cancer types: **Lung Cancer** and **Pancreatic Cancer**.

---

## Prerequisites

- An [Anthropic API key](https://console.anthropic.com/)
- Either [Docker](https://docs.docker.com/get-started/get-docker/) or **Python 3.12+**

---

## Setup

### Option 1 — Docker (recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/Ashvin-Gupta/NICE-2-ASP.git
   cd NICE-2-ASP
   ```

2. Copy the environment template and add your API key:
   ```bash
   cp .env.example .env
   # Open .env and replace the placeholder with your actual Anthropic API key
   ```

3. Build the image:
   ```bash
   docker compose build
   ```

4. Run a pipeline:
   ```bash
   # Lung cancer
   docker compose run lung-cancer

   # Pancreatic cancer
   docker compose run pancreatic-cancer
   ```

Results are saved to `src/output_files/` on your machine. If you want to change the settings in the config file be sure to build the project again before running.

---

### Option 2 — Manual (Python 3.12+)

1. Clone and enter the repository:
   ```bash
   git clone https://github.com/Ashvin-Gupta/NICE-2-ASP.git
   cd NICE-2-ASP
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the environment template and add your API key:
   ```bash
   cp .env.example .env
   # Open .env and replace the placeholder with your actual Anthropic API key
   ```

5. Run a pipeline:
   ```bash
   python main.py --config src/configs/lung_cancer_config.yaml
   python main.py --config src/configs/pancreatic_cancer_config.yaml
   ```

---

## Configuration

Edit the config files in `src/configs/` to change the model, pipeline mode, or output directory. See [`src/configs/README.md`](src/configs/README.md) for all options.

The key setting is `pipeline_mode`:

| Mode | Description |
|---|---|
| `D2K-only` | Guideline → ASP rules (both cancer types) |
| `K2P-only` | Apply existing rules to patients (pancreatic only) |
| `D2K+K2P` | Full end-to-end pipeline (pancreatic only) |

---

## Output

Results are written to `<output_dir>/<cancer_type>/` (where `output_dir` is set in the config file):

- `D2K/` — extracted constants, predicates, and generated ASP rules
- `K2P/` — patient-level rule firings and explanations
- `reviews/` — precision, recall, and F1 evaluation metrics

---

## License

MIT License. Clinical guideline content is from [NICE](https://www.nice.org.uk/terms-and-conditions).
