"""
🌟 הכנה למבחני מחוננים - שלב א׳ ושלב ב׳
Gifted Children Exam Preparation App
Built with Streamlit and OpenAI API
"""

import streamlit as st
import random
import json

# ============================================
# Page Configuration - MUST be first Streamlit command
# ============================================
st.set_page_config(
    page_title="הכנה למבחני מחוננים 🧠",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# Custom CSS for Hebrew RTL support and child-friendly design
# ============================================
st.markdown("""
<style>
    /* RTL Support for Hebrew */
    .stApp {
        direction: rtl;
    }
    
    /* Main container styling */
    .main-header {
        text-align: center;
        padding: 25px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
        border-radius: 25px;
        margin-bottom: 30px;
        color: white;
        box-shadow: 0 10px 40px rgba(99, 102, 241, 0.3);
    }
    
    .main-header h1 {
        font-size: 2.8rem;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.95;
    }
    
    /* Stage selector cards */
    .stage-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        border: 3px solid transparent;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        cursor: pointer;
        direction: rtl;
        text-align: right;
    }
    
    .stage-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .stage-a {
        border-color: #10b981;
        background: linear-gradient(145deg, #ecfdf5 0%, #d1fae5 100%);
    }
    
    .stage-b {
        border-color: #f59e0b;
        background: linear-gradient(145deg, #fffbeb 0%, #fef3c7 100%);
    }
    
    /* Question card styling */
    .question-card {
        background: linear-gradient(145deg, #ffffff 0%, #f0f4f8 100%);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        border-right: 6px solid #6366f1;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        direction: rtl;
        text-align: right;
    }
    
    .question-number {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 15px;
        font-size: 1.1rem;
    }
    
    .question-text {
        font-size: 1.35rem;
        color: #1e293b;
        line-height: 2;
        margin-top: 15px;
    }
    
    .answer-option {
        background: #f1f5f9;
        border-radius: 12px;
        padding: 12px 20px;
        margin: 8px 0;
        border: 2px solid #e2e8f0;
        transition: all 0.2s ease;
    }
    
    .answer-option:hover {
        background: #e0e7ff;
        border-color: #6366f1;
    }
    
    /* Category badges */
    .category-badge {
        display: inline-block;
        padding: 6px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        margin: 5px;
    }
    
    .badge-verbal {
        background: #dbeafe;
        color: #1e40af;
    }
    
    .badge-quantitative {
        background: #dcfce7;
        color: #166534;
    }
    
    .badge-shapes {
        background: #fef3c7;
        color: #92400e;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 25px;
        padding: 15px 30px;
        font-size: 1.2rem;
        font-weight: bold;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
    }
    
    /* Info box */
    .info-box {
        background: linear-gradient(145deg, #eff6ff 0%, #dbeafe 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        border-right: 4px solid #3b82f6;
        direction: rtl;
        text-align: right;
    }
    
    /* Success message */
    .success-banner {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        font-size: 1.2rem;
    }
    
    /* Error message styling */
    .error-banner {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        direction: rtl;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 30px;
        color: #64748b;
        margin-top: 50px;
        border-top: 2px solid #e2e8f0;
    }
    
    /* Tip box */
    .tip-box {
        background: linear-gradient(145deg, #fdf4ff 0%, #fae8ff 100%);
        border-radius: 15px;
        padding: 15px 20px;
        margin: 15px 0;
        border-right: 4px solid #a855f7;
        direction: rtl;
    }
</style>
""", unsafe_allow_html=True)


# ============================================
# Exam Structure Data (Based on Israeli Gifted Program)
# ============================================
EXAM_STRUCTURE = {
    "stage_a": {
        "name": "שלב א׳ - מבחן הסינון",
        "description": "מבחן ארצי לכל תלמידי כיתה ב׳. בודק הבנת הנקרא וחשיבה כמותית.",
        "duration": "40 דקות",
        "categories": {
            "reading_comprehension": {
                "name": "הבנת הנקרא",
                "icon": "📖",
                "description": "קטעי קריאה עם שאלות הבנה"
            },
            "quantitative": {
                "name": "חשיבה כמותית", 
                "icon": "🔢",
                "description": "תרגילי חשבון, בעיות מילוליות, סדרות מספרים"
            }
        }
    },
    "stage_b": {
        "name": "שלב ב׳ - מבחן האיתור",
        "description": "מבחן מתקדם ל-15% שעברו את שלב א׳. בודק חשיבה מילולית, כמותית וצורנית.",
        "duration": "60 דקות",
        "categories": {
            "sentence_completion": {
                "name": "השלמת משפטים",
                "icon": "✏️",
                "description": "השלמת מילים חסרות במשפט"
            },
            "word_relations": {
                "name": "יחסי מילים (אנלוגיות)",
                "icon": "🔗",
                "description": "זיהוי קשרים בין זוגות מילים"
            },
            "number_shapes": {
                "name": "מספרים בצורות",
                "icon": "🔷",
                "description": "מציאת מספר חסר בצורות"
            },
            "word_problems": {
                "name": "בעיות בחשבון",
                "icon": "🧮",
                "description": "בעיות מילוליות מאתגרות"
            },
            "pattern_recognition": {
                "name": "חשיבה צורנית",
                "icon": "🎯",
                "description": "מטריצות וסדרות צורות"
            }
        }
    }
}


def get_openai_client():
    """
    Initialize OpenAI client with proper error handling.
    Import is done inside function to prevent crashes.
    """
    try:
        # Dynamic import to prevent crash if not installed
        from openai import OpenAI
    except ImportError:
        return None, "❌ ספריית openai לא מותקנת. יש לוודא שה-requirements.txt מכיל את הספריה."
    except Exception as e:
        return None, f"❌ שגיאה בטעינת הספריה: {str(e)}"
    
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        if not api_key or api_key == "your-api-key-here":
            return None, "🔑 מפתח ה-API לא הוגדר! יש להוסיף OPENAI_API_KEY בהגדרות Secrets."
        client = OpenAI(api_key=api_key)
        return client, None
    except KeyError:
        return None, "🔑 מפתח ה-API לא נמצא! יש להוסיף OPENAI_API_KEY ב-Settings → Secrets בפורמט:\nOPENAI_API_KEY = \"sk-...\""
    except Exception as e:
        return None, f"❌ שגיאה באתחול: {str(e)}"


def generate_stage_a_questions(client, category: str, num_questions: int) -> tuple:
    """
    Generate Stage A questions (Screening Test).
    Categories: reading_comprehension, quantitative
    """
    random_seed = random.randint(1000, 99999)
    
    prompts = {
        "reading_comprehension": f"""אתה מומחה ביצירת מבחני הבנת הנקרא לילדים בכיתה ב׳ בישראל.

צור {num_questions} שאלות הבנת הנקרא בסגנון מבחן מחוננים שלב א׳.

הנחיות:
1. כתוב קטע קריאה קצר (80-120 מילים) על נושא מעניין לילדים
2. הקטע יכול להיות על: טבע, בעלי חיים, מדע, היסטוריה, גיאוגרפיה
3. לאחר הקטע, צור {num_questions} שאלות אמריקאיות (4 תשובות לכל שאלה)
4. השאלות צריכות לבדוק: הבנה מילולית, הסקת מסקנות, משמעות מילים בהקשר
5. סמן את התשובה הנכונה

פורמט התשובה (JSON):
{{
    "passage": "קטע הקריאה כאן",
    "questions": [
        {{
            "question": "שאלה 1",
            "options": ["א. תשובה 1", "ב. תשובה 2", "ג. תשובה 3", "ד. תשובה 4"],
            "correct": "א"
        }}
    ]
}}

מזהה ייחודי: #{random_seed}
צור תוכן מקורי וייחודי!""",

        "quantitative": f"""אתה מומחה ביצירת שאלות חשיבה כמותית לילדים בכיתה ב׳ בישראל.

צור {num_questions} שאלות בסגנון מבחן מחוננים שלב א׳.

סוגי השאלות (ערבב ביניהם):
1. תרגילי חשבון עם מספר חסר (__ + 15 = 23)
2. בעיות מילוליות (בשפה פשוטה לכיתה ב׳)
3. סדרות מספרים פשוטות (2, 5, 8, 11, __)
4. השוואות (איזה תרגיל תוצאתו גדולה יותר?)
5. חידות בציורים (🍎 + 🍎 = 6, 🍎 = ?)

הנחיות:
- שפה פשוטה וברורה
- מספרים עד 100
- 4 אפשרויות תשובה לכל שאלה
- סמן את התשובה הנכונה

פורמט התשובה (JSON):
{{
    "questions": [
        {{
            "question": "שאלה עם אימוג׳י רלוונטי",
            "options": ["א. תשובה 1", "ב. תשובה 2", "ג. תשובה 3", "ד. תשובה 4"],
            "correct": "ב",
            "type": "סוג השאלה"
        }}
    ]
}}

מזהה ייחודי: #{random_seed}
צור שאלות מקוריות ומגוונות!"""
    }
    
    return _call_openai(client, prompts.get(category, prompts["quantitative"]))


def generate_stage_b_questions(client, category: str, num_questions: int) -> tuple:
    """
    Generate Stage B questions (Identification Test).
    Categories: sentence_completion, word_relations, number_shapes, word_problems, pattern_recognition
    """
    random_seed = random.randint(1000, 99999)
    
    prompts = {
        "sentence_completion": f"""אתה מומחה ביצירת שאלות השלמת משפטים למבחן מחוננים שלב ב׳.

צור {num_questions} שאלות השלמת משפטים ברמה מתאימה לילדי כיתה ב׳-ג׳ מחוננים.

הנחיות:
1. כל משפט חסר מילה אחת
2. המילה החסרה יכולה להיות: פועל, שם עצם, תואר, מילת קישור
3. 4 אפשרויות תשובה - רק אחת מתאימה להקשר
4. המשפטים צריכים להיות הגיוניים ומעניינים
5. חלק מהמילים יכולות להיות ברמת שפה גבוהה יותר

דוגמאות לסגנון:
- "הילד ______ את הספר בהנאה רבה." (קרא/אכל/זרק/שבר)
- "האוויר הקר גרם לי ______." (לצחוק/לרעוד/לשיר/לרקוד)

פורמט התשובה (JSON):
{{
    "questions": [
        {{
            "question": "משפט עם ______ במקום המילה החסרה",
            "options": ["א. מילה 1", "ב. מילה 2", "ג. מילה 3", "ד. מילה 4"],
            "correct": "ג"
        }}
    ]
}}

מזהה ייחודי: #{random_seed}""",

        "word_relations": f"""אתה מומחה ביצירת שאלות אנלוגיות (יחסי מילים) למבחן מחוננים שלב ב׳.

צור {num_questions} שאלות אנלוגיות ברמה מתאימה לילדי כיתה ב׳-ג׳ מחוננים.

סוגי הקשרים (ערבב ביניהם):
1. ניגודים (גדול:קטן = חם:?)
2. חלק מכלל (עלה:עץ = אצבע:?)
3. פעולה ומבצע (מספריים:גוזר = עיפרון:?)
4. קטגוריה (כלב:יונק = נשר:?)
5. מיקום (דג:מים = ציפור:?)
6. סיבה ותוצאה
7. כלי ופעולה

הנחיות:
- הציגו זוג מילים ראשון
- בקשו למצוא זוג עם אותו קשר
- 4 אפשרויות - רק זוג אחד נכון

פורמט התשובה (JSON):
{{
    "questions": [
        {{
            "question": "מילה1 : מילה2 = ? 🤔",
            "pair": "מילה1:מילה2",
            "options": ["א. זוג 1", "ב. זוג 2", "ג. זוג 3", "ד. זוג 4"],
            "correct": "א",
            "relation_type": "סוג הקשר"
        }}
    ]
}}

מזהה ייחודי: #{random_seed}""",

        "number_shapes": f"""אתה מומחה ביצירת שאלות "מספרים בצורות" למבחן מחוננים שלב ב׳.

צור {num_questions} שאלות מספרים בצורות ברמה מתאימה לילדי כיתה ב׳-ג׳.

הנחיות:
1. הצג צורה (משולש/ריבוע/עיגול) מחולקת לחלקים עם מספרים
2. אחד המספרים חסר (?)
3. יש חוקיות מתמטית בין המספרים
4. 4 אפשרויות תשובה

סוגי חוקיות:
- סכום המספרים שווה למספר מסוים
- מכפלה של שני מספרים
- חיבור/חיסור בין מספרים סמוכים

דוגמה לתיאור:
"במשולש: בפינה העליונה 5, בפינה השמאלית 3, בפינה הימנית ?. החוקיות: סכום כל המספרים הוא 15"

פורמט התשובה (JSON):
{{
    "questions": [
        {{
            "question": "תיאור הצורה והמספרים עם אימוג׳י 🔷",
            "shape_description": "תיאור ויזואלי של הצורה",
            "options": ["א. 5", "ב. 7", "ג. 9", "ד. 11"],
            "correct": "ב",
            "rule": "החוקיות"
        }}
    ]
}}

מזהה ייחודי: #{random_seed}""",

        "word_problems": f"""אתה מומחה ביצירת בעיות מילוליות בחשבון למבחן מחוננים שלב ב׳.

צור {num_questions} בעיות מילוליות ברמה מתאימה לילדי כיתה ב׳-ג׳ מחוננים.

הנחיות:
1. בעיות מעניינות עם סיפור קצר
2. דורשות 2-3 שלבי פתרון
3. מספרים עד 100-200
4. 4 אפשרויות תשובה

סוגי בעיות (ערבב):
- בעיות עם כסף
- בעיות עם זמן
- בעיות עם חלוקה
- בעיות עם השוואה
- בעיות הכוללות "יותר מ..." או "פחות מ..."

פורמט התשובה (JSON):
{{
    "questions": [
        {{
            "question": "בעיה מילולית מעניינת עם אימוג׳י 🎯",
            "options": ["א. תשובה 1", "ב. תשובה 2", "ג. תשובה 3", "ד. תשובה 4"],
            "correct": "ד",
            "solution_hint": "רמז קצר לפתרון"
        }}
    ]
}}

מזהה ייחודי: #{random_seed}""",

        "pattern_recognition": f"""אתה מומחה ביצירת שאלות חשיבה צורנית (מטריצות וסדרות) למבחן מחוננים שלב ב׳.

צור {num_questions} שאלות חשיבה צורנית בתיאור מילולי ברמה מתאימה לילדי כיתה ב׳-ג׳.

סוגי שאלות (ערבב):
1. סדרת צורות בשורה - מצאו את האיבר הבא
2. מטריצה 3x3 - מצאו את הצורה החסרה

חוקיות אפשריות:
- סיבוב צורות (90°, 180°)
- שינוי צבע (לבן↔שחור↔אפור)
- הוספה/הסרה של אלמנטים
- שינוי גודל
- מיקום אלמנטים (פנימי/חיצוני)
- תנועה בכיוון השעון או נגדו

תאר את הצורות באמצעות:
- שמות צורות: עיגול ⚪, ריבוע ⬛, משולש 🔺, כוכב ⭐
- צבעים: שחור, לבן, אפור, מלא, ריק
- מיקום: למעלה, למטה, בפנים, בחוץ

פורמט התשובה (JSON):
{{
    "questions": [
        {{
            "question": "תיאור הסדרה/מטריצה עם סימונים",
            "visual_description": "תיאור מפורט של מה רואים",
            "options": ["א. תיאור צורה 1", "ב. תיאור צורה 2", "ג. תיאור צורה 3", "ד. תיאור צורה 4"],
            "correct": "ג",
            "pattern_rule": "החוקיות"
        }}
    ]
}}

מזהה ייחודי: #{random_seed}"""
    }
    
    return _call_openai(client, prompts.get(category, prompts["sentence_completion"]))


def _call_openai(client, prompt: str) -> tuple:
    """
    Make API call to OpenAI with error handling.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """אתה מומחה ביצירת מבחנים לאיתור ילדים מחוננים בישראל.
אתה מכיר היטב את מבנה מבחני המחוננים של משרד החינוך - שלב א׳ ושלב ב׳.
אתה יוצר שאלות מקוריות, מגוונות ומאתגרות בהתאם לרמת הגיל.
תמיד החזר תשובה בפורמט JSON תקין בלבד, ללא טקסט נוסף."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=1.0,
            max_tokens=3000,
            presence_penalty=0.7,
            frequency_penalty=0.7
        )
        
        content = response.choices[0].message.content
        
        # Clean and parse JSON
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        try:
            data = json.loads(content)
            return data, None
        except json.JSONDecodeError as e:
            return None, f"שגיאה בפענוח התשובה: {str(e)}"
            
    except Exception as e:
        error_msg = str(e)
        if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
            return None, "🔑 בעיה עם מפתח ה-API. אנא בדקו שהמפתח תקין."
        elif "rate_limit" in error_msg.lower():
            return None, "⏳ יותר מדי בקשות! אנא המתינו מעט ונסו שוב."
        elif "timeout" in error_msg.lower():
            return None, "⌛ הבקשה לקחה יותר מדי זמן. אנא נסו שוב."
        else:
            return None, f"❌ שגיאה: {error_msg}"


def display_questions_with_answers(data: dict, show_passage: bool = False):
    """
    Display questions in beautiful format with answer options.
    """
    # Show passage if exists (for reading comprehension)
    if show_passage and "passage" in data:
        st.markdown(f"""
        <div class="info-box">
            <h4>📖 קטע הקריאה:</h4>
            <p style="font-size: 1.2rem; line-height: 2;">{data['passage']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    questions = data.get("questions", [])
    
    for i, q in enumerate(questions, 1):
        question_text = q.get("question", "")
        options = q.get("options", [])
        correct = q.get("correct", "")
        
        # Additional info based on question type
        extra_info = ""
        if "type" in q:
            extra_info = f"<span class='category-badge badge-quantitative'>{q['type']}</span>"
        if "relation_type" in q:
            extra_info = f"<span class='category-badge badge-verbal'>{q['relation_type']}</span>"
        if "rule" in q:
            extra_info = f"<br><small>💡 חוקיות: {q['rule']}</small>"
        if "pattern_rule" in q:
            extra_info = f"<br><small>💡 חוקיות: {q['pattern_rule']}</small>"
        
        st.markdown(f"""
        <div class="question-card">
            <span class="question-number">שאלה {i} 📝</span>
            {extra_info}
            <div class="question-text">{question_text}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display options
        for option in options:
            st.markdown(f"""
            <div class="answer-option">{option}</div>
            """, unsafe_allow_html=True)
        
        # Show answer in expander
        with st.expander("🔍 הצג תשובה"):
            st.success(f"✅ התשובה הנכונה: **{correct}**")
            if "solution_hint" in q:
                st.info(f"💡 רמז: {q['solution_hint']}")
        
        st.markdown("<br>", unsafe_allow_html=True)


def main():
    """
    Main application function.
    """
    # ============================================
    # Header
    # ============================================
    st.markdown("""
    <div class="main-header">
        <h1>🧠 הכנה למבחני מחוננים 🌟</h1>
        <p>תרגול אינטראקטיבי לשלב א׳ ושלב ב׳ | שאלות חדשות בכל פעם!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ============================================
    # Sidebar - Stage Selection
    # ============================================
    with st.sidebar:
        st.markdown("## 🎯 בחירת מבחן")
        
        stage = st.radio(
            "בחרו שלב:",
            options=["stage_a", "stage_b"],
            format_func=lambda x: "📗 שלב א׳ - מבחן הסינון" if x == "stage_a" else "📙 שלב ב׳ - מבחן האיתור",
            index=0
        )
        
        st.markdown("---")
        
        # Category selection based on stage
        stage_info = EXAM_STRUCTURE[stage]
        st.markdown(f"### {stage_info['name']}")
        st.markdown(f"⏱️ משך המבחן: {stage_info['duration']}")
        
        st.markdown("---")
        st.markdown("### 📚 בחרו קטגוריה:")
        
        categories = stage_info["categories"]
        category_options = list(categories.keys())
        category_names = [f"{categories[k]['icon']} {categories[k]['name']}" for k in category_options]
        
        selected_category = st.selectbox(
            "קטגוריה:",
            options=category_options,
            format_func=lambda x: f"{categories[x]['icon']} {categories[x]['name']}"
        )
        
        st.markdown(f"""
        <div class="tip-box">
            <strong>{categories[selected_category]['name']}</strong><br>
            {categories[selected_category]['description']}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        num_questions = st.slider(
            "🔢 מספר שאלות:",
            min_value=3,
            max_value=10,
            value=5
        )
        
        st.markdown("---")
        
        st.markdown("""
        <div class="tip-box">
            <strong>💡 טיפ:</strong><br>
            במבחן האמיתי אין "קנס" על תשובות שגויות - תמיד כדאי לנחש!
        </div>
        """, unsafe_allow_html=True)
    
    # ============================================
    # Main Content Area
    # ============================================
    
    # Stage info cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="stage-card stage-a">
            <h3>📗 שלב א׳ - מבחן הסינון</h3>
            <p><strong>לכל תלמידי כיתה ב׳</strong></p>
            <ul>
                <li>📖 הבנת הנקרא</li>
                <li>🔢 חשיבה כמותית</li>
            </ul>
            <p>⏱️ 40 דקות | 🎯 ~15% עוברים לשלב ב׳</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stage-card stage-b">
            <h3>📙 שלב ב׳ - מבחן האיתור</h3>
            <p><strong>למי שעבר את שלב א׳</strong></p>
            <ul>
                <li>✏️ השלמת משפטים</li>
                <li>🔗 יחסי מילים</li>
                <li>🔷 מספרים בצורות</li>
                <li>🧮 בעיות בחשבון</li>
                <li>🎯 חשיבה צורנית</li>
            </ul>
            <p>⏱️ 60 דקות | 🎯 אחוזון 97 = מחונן</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ============================================
    # Generate Button
    # ============================================
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    
    with col_btn2:
        generate_clicked = st.button(
            f"✨ צור {num_questions} שאלות חדשות! ✨",
            type="primary",
            use_container_width=True
        )
    
    # ============================================
    # Question Generation
    # ============================================
    if generate_clicked:
        # Initialize client
        client, error = get_openai_client()
        
        if error:
            st.markdown(f"""
            <div class="error-banner">
                {error}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            ### 🔧 הוראות הגדרה:
            
            1. היכנסו להגדרות האפליקציה ב-Streamlit Cloud
            2. לחצו על **Settings** → **Secrets**
            3. הוסיפו את השורה הבאה:
            ```
            OPENAI_API_KEY = "sk-your-api-key-here"
            ```
            4. החליפו את `sk-your-api-key-here` במפתח האמיתי שלכם
            5. לחצו **Save** ורעננו את הדף
            """)
            return
        
        category_name = categories[selected_category]['name']
        
        with st.spinner(f"🪄 יוצר {num_questions} שאלות {category_name}... רגע קטן!"):
            if stage == "stage_a":
                data, gen_error = generate_stage_a_questions(client, selected_category, num_questions)
            else:
                data, gen_error = generate_stage_b_questions(client, selected_category, num_questions)
        
        if gen_error:
            st.markdown(f"""
            <div class="error-banner">
                {gen_error}
            </div>
            """, unsafe_allow_html=True)
            return
        
        # Success!
        st.markdown(f"""
        <div class="success-banner">
            🎉 המבחן מוכן! {num_questions} שאלות ב{category_name} | בהצלחה! 🎉
        </div>
        """, unsafe_allow_html=True)
        
        # Store in session
        st.session_state['last_data'] = data
        st.session_state['last_category'] = selected_category
        st.session_state['last_stage'] = stage
        
        # Display questions
        show_passage = (selected_category == "reading_comprehension")
        display_questions_with_answers(data, show_passage)
        
        # Regenerate hint
        st.markdown("""
        <div class="tip-box">
            💡 <strong>רוצים עוד שאלות?</strong> לחצו שוב על הכפתור למעלה - כל פעם מתקבלות שאלות חדשות ושונות!
        </div>
        """, unsafe_allow_html=True)
    
    # Display previous questions if exist
    elif 'last_data' in st.session_state:
        st.markdown("""
        <div class="success-banner">
            📚 השאלות האחרונות שיצרתם 📚
        </div>
        """, unsafe_allow_html=True)
        
        show_passage = (st.session_state.get('last_category') == "reading_comprehension")
        display_questions_with_answers(st.session_state['last_data'], show_passage)
    
    # ============================================
    # Footer
    # ============================================
    st.markdown("""
    <div class="footer">
        <p>🌟 נוצר באהבה לילדים מחוננים בישראל 🌟</p>
        <p>📚 מבוסס על מבנה מבחני המחוננים של משרד החינוך</p>
        <p>💡 <strong>זכרו:</strong> במבחן האמיתי - תמיד כדאי לנחש! אין קנס על טעויות.</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# Entry Point
# ============================================
if __name__ == "__main__":
    main()