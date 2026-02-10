---
name: peruvian-legal-research
description: Research Peruvian law using locally stored legal codes. Query the Constitution, Civil Code, Penal Code, Procedural Codes, Tax Code, and Children's Code. Use when answering legal questions about Peru, citing specific articles, or comparing Peruvian law with other systems.
version: 1.0.0
metadata: {"openclaw":{"emoji":"⚖️"}}
---

# ⚖️ Peruvian Legal Research

Research tool for Peruvian law based on a locally stored library of 7 major legal codes totaling ~3 million characters.

## Available Codes

| Code | File | Size |
|------|------|------|
| Constitución Política del Perú (1993) | `{baseDir}/../../constitucion_peru_1993.txt` | 151k chars |
| Código Civil | `{baseDir}/../../codigo_civil.txt` | 468k chars |
| Código Penal | `{baseDir}/../../codigo_penal.txt` | 605k chars |
| Código Procesal Civil | `{baseDir}/../../codigo_procesal_civil.txt` | 566k chars |
| Código Procesal Penal | `{baseDir}/../../codigo_procesal_penal.txt` | 522k chars |
| Código Tributario | `{baseDir}/../../codigo_tributario.txt` | 530k chars |
| Código de Niños y Adolescentes | `{baseDir}/../../codigo_ninos_adolescentes.txt` | 137k chars |

## How to Use

1. **Identify the relevant code** based on the legal question
2. **Use `read` tool** to search the appropriate file for specific articles or keywords
3. **Use `exec` with `grep`** for quick keyword searches across codes:
   ```bash
   grep -n -i "habeas data" /root/.openclaw/workspace/constitucion_peru_1993.txt
   grep -n -i "legítima defensa" /root/.openclaw/workspace/codigo_penal.txt
   ```
4. **Cite specific articles** with their exact text when answering

## Research Guidelines

- Always cite the specific article number and its exact text
- Note if an article has been modified (look for "modificado por" annotations)
- Cross-reference between codes when relevant (e.g., Constitutional basis for a Civil Code provision)
- When comparing with other legal systems, clearly distinguish Peruvian law from foreign law
- Flag when information might be outdated (codes were downloaded Feb 2026 from lpderecho.pe)

## Deep Study Notes

Detailed analysis notes are available at `{baseDir}/../../memory/legal_study_notes.md`

## Source

All codes sourced from lpderecho.pe (actualizado/updated versions).
Some codes were unavailable (Comercio, Administrativo, Ejecución Penal, Consumidor, Sociedades — returned 403).
