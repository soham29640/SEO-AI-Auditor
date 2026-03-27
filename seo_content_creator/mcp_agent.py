"""
SEO optimizer built around llama3's 4096-token context window.


Strategy:
- Never send more than 2000 chars of HTML body per Ollama call
- Never send more than 400 chars of a report section
- Each call asks llama3 to ADD one small <section> block only
- Accumulate all added blocks, then stitch into the original HTML at the end
- Gemini handles only <head> meta tags (tiny prompt, skipped if quota gone)
"""


import os
import re
import shutil
import time


from seo_content_creator.utils import load_json, load_html, save_html




# ── Token-safe limits for llama3 ─────────────────────────────────────────
MAX_SECTION_CHARS = 400   # ~100 tokens of report context per call
MAX_BODY_CHARS    = 2000  # ~500 tokens of HTML body for context
MAX_OUTPUT_CHARS  = 8000  # sanity cap on what llama3 returns




# ── Helpers ───────────────────────────────────────────────────────────────


def _backup(file_path: str):
    backup = file_path.replace(".html", "_backup.html")
    if not os.path.exists(backup):
        shutil.copy(file_path, backup)
        print(f"   💾 Backup: {os.path.basename(backup)}")




def _strip_markdown(text: str) -> str:
    return re.sub(r"```[a-z]*", "", text).replace("```", "").strip()




def _extract_section_block(text: str) -> str:
    """Pull out just the first <section>...</section> from llama3 output."""
    match = re.search(r"<section[\s\S]*?</section>", text, re.IGNORECASE)
    if match:
        return match.group(0).strip()
    # fallback: grab any <div> block
    match = re.search(r"<div[\s\S]*?</div>", text, re.IGNORECASE)
    if match:
        return match.group(0).strip()
    return ""




def _get_body_snippet(html: str) -> str:
    """
    Return a short snippet of the body for context.
    Keeps well under MAX_BODY_CHARS so llama3 doesn't overflow.
    """
    start = html.lower().find("<body")
    end   = html.lower().rfind("</body>")
    if start == -1 or end == -1:
        return html[:MAX_BODY_CHARS]
    body = html[start:end]
    # Send only the first part — enough for llama3 to understand the page topic
    return body[:MAX_BODY_CHARS]




# ── Pass 1: Gemini — head/meta only (skipped gracefully if quota gone) ────


def _gemini_meta_pass(html: str, report_data: dict) -> str:
    try:
        from seo_content_creator.gemini_client import GeminiClient
        gemini = GeminiClient()


        head_start = html.lower().find("<head")
        head_end   = html.lower().find("</head>") + 7
        if head_start == -1:
            return html


        head_block = html[head_start:head_end]


        # Find keyword section in report (most useful for meta tags)
        keyword_hint = ""
        if isinstance(report_data, list):
            for s in report_data:
                if "keyword" in s.lower() and len(s) > 100:
                    keyword_hint = s[:400]
                    break


        prompt = f"""SEO task: improve this HTML <head> section only.


KEYWORD GAPS: {keyword_hint}


FIX:
1. Improve <title> — include primary cricket keywords
2. Improve/add <meta name="description"> — 150-160 chars
3. Add <meta name="keywords"> if missing


Return ONLY the updated <head>...</head>. No explanation.


HEAD:
{head_block}
"""
        result = gemini.call_with_retry(prompt)
        result = _strip_markdown(result)


        if "<head" in result.lower():
            updated = html[:head_start] + result + html[head_end:]
            print("   ✅ Gemini meta pass done")
            return updated


    except Exception as e:
        print(f"   ⚠️  Gemini skipped ({type(e).__name__}): {str(e)[:80]}")


    return html




# ── Pass 2: Ollama — one new <section> per report gap ────────────────────


def _ollama_content_pass(html: str, report_sections: list, llm) -> str:
    """
    For each report section, ask llama3 to write ONE new <section> block.
    We never send the full HTML — only a short body snippet for topic context.
    All new blocks are collected and injected before </body>.
    """
    body_snippet  = _get_body_snippet(html)
    new_blocks    = []


    for i, section in enumerate(report_sections):
        short_section = section[:MAX_SECTION_CHARS]
        print(f"   🦙 Ollama section {i+1}/{len(report_sections)}: "
              f"{short_section[:55]}...")


        prompt = f"""You write SEO-optimized HTML content blocks for a cricket website.


PAGE CONTEXT (start of page body):
{body_snippet}


SEO GAP TO FIX:
{short_section}


TASK:
Write ONE <section> block that fills this SEO gap.
- Use an H2 heading
- Write 3-5 sentences of real cricket content
- Use relevant keywords naturally
- Return ONLY the <section>...</section> HTML block
- No explanation, no markdown, no full page"""


        try:
            raw = llm.generate(prompt, timeout=120)
            raw = _strip_markdown(raw)
            block = _extract_section_block(raw)


            if block:
                new_blocks.append(block)
                print(f"      ✅ Got block ({len(block)} chars)")
            else:
                print(f"      ⚠️  No valid block extracted, skipping")


        except RuntimeError as e:
            print(f"      ❌ Ollama error: {e}")
            continue


        time.sleep(0.5)   # small pause between calls


    if not new_blocks:
        print("   ⚠️  No new blocks generated by Ollama")
        return html


    # Stitch all new blocks before </body>
    injection = "\n\n" + "\n\n".join(new_blocks) + "\n\n"
    body_close = html.lower().rfind("</body>")
    if body_close == -1:
        html += injection
    else:
        html = html[:body_close] + injection + html[body_close:]


    print(f"   ✅ Injected {len(new_blocks)} new section(s) into HTML")
    return html




# ── Main ──────────────────────────────────────────────────────────────────


def run_mcp_agent(website_path: str, report_path: str):
    try:
        from seo_content_creator.ollama_client import OllamaClient
        llm = OllamaClient()   # uses llama3 by default


        report_data = load_json(report_path)
        report_sections = [s for s in report_data
                           if isinstance(s, str) and len(s) > 100]


        results = []


        for file_name in os.listdir(website_path):
            if not file_name.endswith(".html") or "_backup" in file_name:
                continue


            file_path = os.path.join(website_path, file_name)
            print(f"\n🔍 Processing: {file_name}")


            _backup(file_path)
            html         = load_html(file_path)
            original_len = len(html)


            # Pass 1: Gemini fixes <head> (skips gracefully if quota gone)
            print("   🤖 Pass 1: Gemini meta tags...")
            html = _gemini_meta_pass(html, report_data)


            # Pass 2: Ollama adds new content sections
            print("   🦙 Pass 2: Ollama content blocks...")
            html = _ollama_content_pass(html, report_sections, llm)


            if len(html) <= original_len:
                print(f"   ⚠️  No growth in {file_name}, skipping save")
                results.append(f"SKIPPED (no growth): {file_name}")
                continue


            save_html(file_path, html)
            print(f"   ✅ Saved {file_name}: {original_len} → {len(html)} chars "
                  f"(+{len(html)-original_len})")
            results.append(f"OK: {file_name}")


        summary = ", ".join(results) if results else "No HTML files found"
        return f"Done — {summary}"


    except Exception as e:
        print(f"❌ MCP agent error: {e}")
        return f"Error: {e}"
