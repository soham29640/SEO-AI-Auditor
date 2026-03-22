import os
import json
from dotenv import load_dotenv
from google import genai

# ---------------- LOAD ENV ----------------
load_dotenv("model/.env")

api_key = os.getenv("GEMINI_API_KEY")

model="gemini-3-flash-preview"

client = genai.Client(api_key=api_key)


# =====================================================
# NUMERICAL FEATURE REPORT
# =====================================================

def report_generator_for_numerical_feature_extraction(word_diff_percent, backlink_diff_percent):

    prompt = f"""
You are a professional SEO auditor.

Analyze the following metrics comparing a webpage against SERP competitors.

Metrics:
- Content Depth Score: {word_diff_percent:.2f}% of SERP average
- Backlink Authority Score: {backlink_diff_percent:.2f}% of SERP average

Explain what these metrics mean for SEO performance.

Instructions:
- Use concise bullet points
- Avoid long paragraphs
- Base reasoning only on the provided data
- Focus on ranking implications

Output format:

Content Depth Analysis
• insight
• insight

Authority Analysis
• insight
• insight

Ranking Potential
• insight
• insight

SEO Recommendations
• actionable suggestion
• actionable suggestion
"""

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    return response.text


# =====================================================
# SEMANTIC SIMILARITY REPORT
# =====================================================

def report_generator_for_similarity(report):

    prompt = f"""
You are an SEO specialist analyzing semantic relevance.

The following data measures how closely the page content aligns
with the semantic structure of top SERP competitors.

DATA:
{json.dumps(report, indent=2)}

Interpret this information.

Instructions:
- Use concise bullet points
- Avoid repeating the raw numbers
- Focus on topical coverage and semantic completeness

Output format:

Semantic Alignment
• explanation

Competitor Comparison
• explanation

Ranking Impact
• explanation

SEO Recommendations
• suggestions to improve semantic coverage
"""

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    return response.text


# =====================================================
# SEARCH INTENT REPORT (LDA)
# =====================================================

def report_generator_for_topic_modeling(report):

    prompt = f"""
You are an SEO strategist evaluating search intent alignment.

The following topic modeling results describe dominant themes
from top-ranking SERP pages.

DATA:
{json.dumps(report, indent=2)}

Analyze whether the page aligns with the dominant SERP intent.

Instructions:
- Focus on search intent satisfaction
- Use concise bullet points
- Avoid speculation beyond the data

Output format:

SERP Intent Overview
• explanation

Content Intent Match
• explanation

Ranking Implications
• explanation

Optimization Suggestions
• ways to better match user intent
"""

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    return response.text


# =====================================================
# KEYWORD GAP REPORT (TF-IDF)
# =====================================================

def report_generator_for_tfidf(report):

    prompt = f"""
You are an SEO content optimization expert.

The following data compares important SERP keywords
with the keywords present in the analyzed page.

DATA:
{json.dumps(report, indent=2)}

Identify keyword coverage gaps.

Instructions:
- Use concise bullet points
- Focus on missing keyword clusters
- Avoid repeating raw data

Output format:

Keyword Coverage Overview
• explanation

Keyword Gaps
• explanation

Ranking Impact
• explanation

Content Optimization Suggestions
• improvements to increase keyword coverage
"""

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    return response.text


# =====================================================
# ENTITY COVERAGE REPORT (NER)
# =====================================================

def report_generator_for_ner(report):

    prompt = f"""
You are an SEO topical authority analyst.

The following data compares entities mentioned in
the analyzed page with entities used by top SERP competitors.

DATA:
{json.dumps(report, indent=2)}

Evaluate the page's topical authority.

Instructions:
- Use concise bullet points
- Focus on entity coverage and topic completeness
- Provide practical SEO suggestions

Output format:

Entity Coverage Overview
• explanation

Entity Gaps
• explanation

Ranking Implications
• explanation

SEO Recommendations
• ways to improve entity coverage
"""

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    return response.text