"""AI utilities for generating insights and summaries."""
import os
from dotenv import load_dotenv
import openai
from datetime import datetime

load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_ai_response(prompt, max_tokens=500, temperature=0.7):
    """Get a response from OpenAI API or local LLM."""
    try:
        use_local = os.getenv("USE_LOCAL_LLM", "false").lower() == "true"
        
        if use_local:
            # Configure for local LLM endpoint
            openai.api_base = os.getenv("LOCAL_LLM_ENDPOINT", "http://localhost:8000/v1")
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo" if not use_local else "local-model",
            messages=[
                {"role": "system", "content": "You are a helpful personal assistant helping someone manage their life and startup. Be concise, encouraging, and insightful."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"


def generate_daily_summary(journal_text, tasks_done, tasks_remaining, mood, energy, stress):
    """Generate a daily summary with AI insights."""
    prompt = f"""Based on today's data, provide a brief summary and insights:

Journal: {journal_text[:500] if journal_text else "No journal entry"}
Tasks Completed: {len(tasks_done)}
Tasks Remaining: {len(tasks_remaining)}
Mood: {mood}/10
Energy: {energy}/10
Stress: {stress}/10

Provide:
1. A brief productivity assessment
2. One visible pattern or insight
3. One actionable suggestion for tomorrow

Keep it under 100 words, friendly and encouraging."""

    return get_ai_response(prompt, max_tokens=200)


def generate_task_suggestions(tasks, priorities):
    """Generate AI suggestions for task prioritization."""
    task_list = "\n".join([f"- {t.get('title')} (Priority: {t.get('priority')}, Deadline: {t.get('deadline', 'None')})" 
                           for t in tasks[:10]])  # Limit to 10 tasks
    
    prompt = f"""Based on these tasks and priorities:

Tasks:
{task_list}

Today's Priorities:
{priorities}

Provide:
1. Which 2-3 tasks should be tackled first
2. Any tasks that seem overdue or critical
3. A brief motivation

Keep it under 80 words."""

    return get_ai_response(prompt, max_tokens=150)


def analyze_journal_entry(entry_text):
    """Analyze a journal entry for emotional tone and insights."""
    prompt = f"""Analyze this journal entry:

{entry_text}

Provide:
1. Emotional tone (1-2 words)
2. Key themes (2-3 words)
3. One brief insight or reflection

Keep it under 60 words."""

    return get_ai_response(prompt, max_tokens=120)


def generate_journal_summary(entries):
    """Generate a summary from multiple journal entries."""
    if not entries:
        return "No journal entries to summarize."
    
    entries_text = "\n\n".join([f"Date: {e.get('date')}\n{e.get('content', '')[:200]}" 
                                for e in entries[:7]])  # Last 7 entries
    
    prompt = f"""Summarize these recent journal entries:

{entries_text}

Provide:
1. Overall mood trend
2. Recurring themes or concerns
3. Notable progress or changes

Keep it under 120 words."""

    return get_ai_response(prompt, max_tokens=200)


def categorize_note(note_text):
    """Categorize a note using AI."""
    prompt = f"""Categorize this note into ONE category:

{note_text[:300]}

Choose from: Idea, Todo, Learning, Personal, Work, Random

Return only the category name."""

    return get_ai_response(prompt, max_tokens=10, temperature=0.3)


def generate_weekly_report(journal_entries, tasks_completed, habits_data, mood_avg):
    """Generate a weekly report summary."""
    prompt = f"""Generate a weekly summary report:

Journal Entries: {len(journal_entries)}
Tasks Completed: {tasks_completed}
Average Mood: {mood_avg:.1f}/10
Habits Tracked: {len(habits_data)}

Provide:
1. Big wins of the week
2. Areas for improvement
3. Encouraging insight for next week

Keep it under 150 words."""

    return get_ai_response(prompt, max_tokens=250)


def generate_monthly_report(stats):
    """Generate a monthly report summary."""
    prompt = f"""Generate a monthly summary report based on these statistics:

{stats}

Provide:
1. Major achievements
2. Long-term patterns observed
3. Strategic suggestions for next month

Keep it under 200 words."""

    return get_ai_response(prompt, max_tokens=300)


def extract_goals_from_journal(entry_text):
    """Extract goals or action items from a journal entry."""
    prompt = f"""Extract any goals, intentions, or action items from this journal entry:

{entry_text}

List them as bullet points. If none found, say "No specific goals mentioned."

Keep it under 80 words."""

    return get_ai_response(prompt, max_tokens=150)
