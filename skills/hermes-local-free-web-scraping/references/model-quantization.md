# Model Quantization Selection Guide for Local GGUF Models

## When to use which quant level

| Quant | RAM Required | Quality | Speed | Best Use Case |
|-------|-------------|---------|-------|---------------|
| **Q2_K** | 2GB+ | Lower | Fastest | Tightest RAM budgets, simple chat |
| **Q3_K_M** | 4GB+ | Good | Good | General purpose, most users start here |
| **Q4_K_M** | 6GB+ | Very Good | Good | **Recommended default**, hermes3:3b default |
| **Q5_K_M** | 8GB+ | Excellent | Moderate | Technical work, code generation |
| **Q6_K** | 12GB+ | Great | Slower | Demanding tasks, longer context |
| **Q7_0** | 16GB+ | Near-lossless | Slow | Quality-over-speed scenarios |
| **Q8_0** | 20GB+ | Lossless | Slowest | Maximum quality, VRAM-heavy |

## hermes3:3b specific

- Your model ships at **Q4_K_M** - this is the optimal default
- 2GB model file size, ~6GB RAM needed at runtime for Q4_K_M
- Q5_K_M would require ~8GB RAM but offer marginal quality gain
- Q3_K_M would work on 4GB RAM but slight quality reduction

## Selection flowchart

```
           ┌─────────────────────┐
           │  How much RAM?      │
           └─────────────────────┘
                          │
              ┌────────────-┼─────────────┐
              │             │             │
          4GB or less     6-8GB        8GB or more
              │             │             │
     ──────────┼───────────┼───────────┼──────────
              │             │             │
    Q3_K_M       Q4_K_M     Q5_K_M        Q6_K+
              │             │             │
  Good quality    Very Good   Excellent     Great
  (recommended)   (default)   (if needed)   (if needed)
```

## Quick pick rule

| RAM Available | Pick |
|--------------|------|
| 4GB or less | `Q3_K_M` |
| 6-8GB | `Q4_K_M` *(hermes3:3b default)* |
| 8GB or more | `Q5_K_M` if quality matters, else `Q4_K_M` |

## Verifying your setup

```bash
# Check model details after pulling
ollama show hermes3:3b

# Or via API
curl http://localhost:11434/api/tags

# Expected output includes:
# "quantization_level": "Q4_K_M"
# "parameter_size": "3.2B"
```