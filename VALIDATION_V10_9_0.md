# JARVIS v11.1.0 Validation

| Check | Result |
|---|---|
| compileall | PASS |
| pytest | 51 passed / 0 failed |
| module import sweep | 94 / 94 passed |
| clean core boot | PASS |
| version | 10.9.0 |
| tools registered | 10 |
| hardware certification | PASS/WARN by environment |

## Environment qualification

Optional integrations such as CUDA llama.cpp, LanceDB, Flet, microphone capture and Sentence Transformers are environment-dependent. The certification system never reports an unavailable dependency as a successful live integration.
