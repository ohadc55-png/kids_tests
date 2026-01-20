"""
🧠 הכנה למבחני מחוננים - שלב א׳ ושלב ב׳
Gifted Children Exam Preparation App
"""

import streamlit as st
import random
import json
import sys
import subprocess

# ============================================
# Page Configuration
# ============================================
st.set_page_config(
    page_title="הכנה למבחני מחוננים 🧠",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CRITICAL: Install openai if missing
# ============================================
def install_openai():
    """Install openai package if not available"""
    try:
        import openai
        return True, openai.__version__
    except ImportError:
        st.warning("⏳ מתקין את ספריית OpenAI... אנא המתן")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "openai>=1.0.0"])
            st.success("✅ ההתקנה הושלמה! אנא רענן את הדף.")
            st.rerun()
        except Exception as e:
            return False, str(e)
    return True, "installed"

# Check and install openai
openai_ok, openai_status = install_openai()

if not openai_ok:
    st.error(f"""
    ❌ לא ניתן להתקין את ספריית OpenAI
    
    **שגיאה:** {openai_status}
    
    **פתרון אפשרי:**
    1. ודא שקובץ `requirements.txt` קיים ב-repository
    2. ודא שהוא מכיל את השורה: `openai`
    3. נסה לעשות redeploy לאפליקציה
    """)
    st.stop()

# Now safely import openai
from openai import OpenAI

# ============================================
# Custom CSS
# ============================================
st.markdown("""
<style>
    .stApp { direction: rtl; }
    
    .main-header {
        text-align: center;
        padding: 25px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
        border-radius: 25px;
        margin-bottom: 30px;
        color: white;
        box-shadow: 0 10px 40px rgba(99, 102, 241, 0.3);
    }
    
    .main-header h1 { font-size: 2.5rem; margin-bottom: 10px; }
    .main-header p { font-size: 1.1rem; opacity: 0.95; }
    
    .stage-card {
        background: #f8fafc;
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        border: 3px solid transparent;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        direction: rtl;
        text-align: right;
    }
    
    .stage-a { border-color: #10b981; background: linear-gradient(145deg, #ecfdf5, #d1fae5); }
    .stage-b { border-color: #f59e0b; background: linear-gradient(145deg, #fffbeb, #fef3c7); }
    
    .question-card {
        background: linear-gradient(145deg, #ffffff, #f0f4f8);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        border-right: 6px solid #6366f1;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        direction: rtl;
        text-align: right;
    }
    
    .question-number {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 15px;
    }
    
    .question-text { font-size: 1.3rem; color: #1e293b; line-height: 2; margin-top: 15px; }
    
    .answer-option {
        background: #f1f5f9;
        border-radius: 12px;
        padding: 12px 20px;
        margin: 8px 0;
        border: 2px solid #e2e8f0;
    }
    
    .success-banner {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        font-size: 1.2rem;
    }
    
    .error-banner {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
    }
    
    .info-box {
        background: linear-gradient(145deg, #eff6ff, #dbeafe);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        border-right: 4px solid #3b82f6;
        direction: rtl;
        text-align: right;
    }
    
    .tip-box {
        background: linear-gradient(145deg, #fdf4ff, #fae8ff);
        border-radius: 15px;
        padding: 15px 20px;
        margin: 15px 0;
        border-right: 4px solid #a855f7;
        direction: rtl;
    }
    
    .footer {
        text-align: center;
        padding: 30px;
        color: #64748b;
        margin-top: 50px;
        border-top: 2px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)


# ============================================
# Exam Structure
# ============================================
EXAM_STRUCTURE = {
    "stage_a": {
        "name": "שלב א׳ - מבחן הסינון",
        "description": "מבחן ארצי לכל תלמידי כיתה ב׳",
        "duration": "40 דקות",
        "categories": {
            "reading_comprehension": {"name": "הבנת הנקרא", "icon": "📖", "description": "קטעי קריאה עם שאלות הבנה"},
            "quantitative": {"name": "חשיבה כמותית", "icon": "🔢", "description": "תרגילי חשבון, סדרות, בעיות מילוליות"}
        }
    },
    "stage_b": {
        "name": "שלב ב׳ - מבחן האיתור",
        "description": "מבחן מתקדם ל-15% שעברו שלב א׳",
        "duration": "60 דקות",
        "categories": {
            "sentence_completion": {"name": "השלמת משפטים", "icon": "✏️", "description": "השלמת מילים חסרות"},
            "word_relations": {"name": "יחסי מילים", "icon": "🔗", "description": "אנלוגיות מילוליות"},
            "number_shapes": {"name": "מספרים בצורות", "icon": "🔷", "description": "מציאת מספר חסר"},
            "word_problems": {"name": "בעיות בחשבון", "icon": "🧮", "description": "בעיות מילוליות מאתגרות"},
            "pattern_recognition": {"name": "חשיבה צורנית", "icon": "🎯", "description": "מטריצות וסדרות צורות"}
        }
    }
}


def get_openai_client():
    """Initialize OpenAI client"""
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        if not api_key or len(api_key) < 10:
            return None, "🔑 מפתח ה-API ריק או לא תקין"
        client = OpenAI(api_key=api_key)
        return client, None
    except KeyError:
        return None, "🔑 מפתח ה-API לא נמצא! הוסיפו OPENAI_API_KEY ב-Secrets"
    except Exception as e:
        return None, f"❌ שגיאה: {str(e)}"


def generate_questions(client, stage: str, category: str, num_questions: int):
    """Generate questions based on stage and category"""
    random_seed = random.randint(1000, 99999)
    
    # Build prompt based on category
    if category == "reading_comprehension":
        prompt = f"""צור מבחן הבנת הנקרא לילדי כיתה ב׳ עם {num_questions} שאלות.
כתוב קטע קריאה קצר (80-100 מילים) ואז שאלות אמריקאיות.
מזהה: #{random_seed}

החזר JSON בפורמט:
{{"passage": "הקטע", "questions": [{{"question": "שאלה", "options": ["א. ...", "ב. ...", "ג. ...", "ד. ..."], "correct": "א"}}]}}"""

    elif category == "quantitative":
        prompt = f"""צור {num_questions} שאלות חשיבה כמותית לכיתה ב׳.
סוגים: סדרות מספרים, תרגילים עם מספר חסר, בעיות מילוליות פשוטות.
מזהה: #{random_seed}

החזר JSON:
{{"questions": [{{"question": "שאלה", "options": ["א. ...", "ב. ...", "ג. ...", "ד. ..."], "correct": "ב"}}]}}"""

    elif category == "sentence_completion":
        prompt = f"""צור {num_questions} שאלות השלמת משפטים למבחן מחוננים שלב ב׳.
כל משפט חסר מילה אחת, 4 אפשרויות תשובה.
מזהה: #{random_seed}

החזר JSON:
{{"questions": [{{"question": "משפט עם ______ ", "options": ["א. מילה1", "ב. מילה2", "ג. מילה3", "ד. מילה4"], "correct": "ג"}}]}}"""

    elif category == "word_relations":
        prompt = f"""צור {num_questions} שאלות אנלוגיות (יחסי מילים) למבחן מחוננים.
דוגמה: כלב:יונק = נשר:? תשובה: עוף
מזהה: #{random_seed}

החזר JSON:
{{"questions": [{{"question": "מילה1 : מילה2 = מילה3 : ?", "options": ["א. ...", "ב. ...", "ג. ...", "ד. ..."], "correct": "א"}}]}}"""

    elif category == "number_shapes":
        prompt = f"""צור {num_questions} שאלות "מספרים בצורות" למבחן מחוננים.
תאר צורה (משולש/ריבוע) עם מספרים, אחד חסר, יש חוקיות.
מזהה: #{random_seed}

החזר JSON:
{{"questions": [{{"question": "תיאור הצורה והחוקיות", "options": ["א. 5", "ב. 7", "ג. 9", "ד. 11"], "correct": "ב"}}]}}"""

    elif category == "word_problems":
        prompt = f"""צור {num_questions} בעיות מילוליות בחשבון למבחן מחוננים שלב ב׳.
בעיות עם 2-3 שלבי פתרון, מספרים עד 100.
מזהה: #{random_seed}

החזר JSON:
{{"questions": [{{"question": "בעיה מילולית", "options": ["א. ...", "ב. ...", "ג. ...", "ד. ..."], "correct": "ד"}}]}}"""

    else:  # pattern_recognition
        prompt = f"""צור {num_questions} שאלות חשיבה צורנית למבחן מחוננים.
תאר סדרת צורות או מטריצה, הילד צריך למצוא את הצורה הבאה/חסרה.
מזהה: #{random_seed}

החזר JSON:
{{"questions": [{{"question": "תיאור הסדרה", "options": ["א. תיאור צורה", "ב. ...", "ג. ...", "ד. ..."], "correct": "ג"}}]}}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "אתה מומחה ביצירת מבחנים למחוננים בישראל. החזר רק JSON תקין."},
                {"role": "user", "content": prompt}
            ],
            temperature=1.0,
            max_tokens=2500
        )
        
        content = response.choices[0].message.content.strip()
        
        # Clean JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        data = json.loads(content.strip())
        return data, None
        
    except json.JSONDecodeError as e:
        return None, f"שגיאה בפענוח: {str(e)}"
    except Exception as e:
        return None, f"שגיאה: {str(e)}"


def display_questions(data: dict, show_passage: bool = False):
    """Display questions nicely"""
    if show_passage and "passage" in data:
        st.markdown(f"""
        <div class="info-box">
            <h4>📖 קטע הקריאה:</h4>
            <p style="font-size: 1.2rem; line-height: 2;">{data['passage']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    for i, q in enumerate(data.get("questions", []), 1):
        st.markdown(f"""
        <div class="question-card">
            <span class="question-number">שאלה {i} 📝</span>
            <div class="question-text">{q.get('question', '')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        for option in q.get("options", []):
            st.markdown(f'<div class="answer-option">{option}</div>', unsafe_allow_html=True)
        
        with st.expander("🔍 הצג תשובה"):
            st.success(f"✅ התשובה הנכונה: **{q.get('correct', '?')}**")
        
        st.markdown("<br>", unsafe_allow_html=True)


def main():
    """Main app"""
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🧠 הכנה למבחני מחוננים 🌟</h1>
        <p>תרגול אינטראקטיבי לשלב א׳ ושלב ב׳ | שאלות חדשות בכל פעם!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Debug info (can be removed later)
    with st.expander("🔧 מידע טכני (לאבחון בעיות)"):
        st.write(f"Python version: {sys.version}")
        st.write(f"OpenAI status: {openai_status}")
        try:
            import openai
            st.write(f"OpenAI version: {openai.__version__}")
        except:
            st.write("OpenAI: Not loaded")
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎯 בחירת מבחן")
        
        stage = st.radio(
            "שלב:",
            ["stage_a", "stage_b"],
            format_func=lambda x: "📗 שלב א׳" if x == "stage_a" else "📙 שלב ב׳"
        )
        
        st.markdown("---")
        
        stage_info = EXAM_STRUCTURE[stage]
        categories = stage_info["categories"]
        
        selected_category = st.selectbox(
            "📚 קטגוריה:",
            list(categories.keys()),
            format_func=lambda x: f"{categories[x]['icon']} {categories[x]['name']}"
        )
        
        st.info(f"💡 {categories[selected_category]['description']}")
        
        num_questions = st.slider("🔢 מספר שאלות:", 3, 10, 5)
        
        st.markdown("---")
        st.markdown("💡 **טיפ:** במבחן אין קנס על טעויות - תמיד כדאי לנחש!")
    
    # Main area - Stage cards
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="stage-card stage-a">
            <h3>📗 שלב א׳</h3>
            <p>📖 הבנת הנקרא | 🔢 חשיבה כמותית</p>
            <p>⏱️ 40 דקות | 🎯 ~15% עוברים</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="stage-card stage-b">
            <h3>📙 שלב ב׳</h3>
            <p>✏️ משפטים | 🔗 אנלוגיות | 🔷 צורות | 🧮 חשבון</p>
            <p>⏱️ 60 דקות | 🎯 אחוזון 97 = מחונן</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Generate button
    col_btn = st.columns([1, 2, 1])[1]
    with col_btn:
        generate = st.button("✨ צור שאלות חדשות! ✨", type="primary", use_container_width=True)
    
    if generate:
        client, error = get_openai_client()
        
        if error:
            st.markdown(f'<div class="error-banner">{error}</div>', unsafe_allow_html=True)
            st.markdown("""
            ### 🔧 הוראות:
            1. ב-Streamlit Cloud לחצו על **Settings** (גלגל שיניים)
            2. בחרו **Secrets**
            3. הוסיפו:
            ```
            OPENAI_API_KEY = "sk-proj-your-key-here"
            ```
            4. לחצו **Save** ורעננו
            """)
            return
        
        with st.spinner("🪄 יוצר שאלות..."):
            data, gen_error = generate_questions(client, stage, selected_category, num_questions)
        
        if gen_error:
            st.markdown(f'<div class="error-banner">{gen_error}</div>', unsafe_allow_html=True)
            return
        
        st.markdown('<div class="success-banner">🎉 המבחן מוכן! בהצלחה! 🎉</div>', unsafe_allow_html=True)
        
        st.session_state['last_data'] = data
        st.session_state['last_cat'] = selected_category
        
        display_questions(data, selected_category == "reading_comprehension")
    
    elif 'last_data' in st.session_state:
        st.markdown('<div class="success-banner">📚 השאלות האחרונות 📚</div>', unsafe_allow_html=True)
        display_questions(st.session_state['last_data'], st.session_state.get('last_cat') == "reading_comprehension")
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>🌟 נוצר באהבה לילדים מחוננים בישראל 🌟</p>
        <p>💡 כל לחיצה = שאלות חדשות!</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()