"""
אפליקציה ליצירת מבחנים חינוכיים לילדים
Educational Test Generator for Children
Built with Streamlit and OpenAI API
"""

import streamlit as st
import random

# ============================================
# Page Configuration - MUST be first Streamlit command
# ============================================
st.set_page_config(
    page_title="יוצר המבחנים הקסום 🌟",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed"
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
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 30px;
        color: white;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 10px;
    }
    
    /* Question card styling */
    .question-card {
        background: linear-gradient(145deg, #ffffff 0%, #f0f4f8 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border-right: 5px solid #667eea;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        direction: rtl;
        text-align: right;
    }
    
    .question-number {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    
    .question-text {
        font-size: 1.3rem;
        color: #2d3748;
        line-height: 1.8;
        margin-top: 10px;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 25px;
        padding: 15px 30px;
        font-size: 1.2rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        direction: rtl;
        text-align: right;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        direction: rtl;
        text-align: right;
    }
    
    /* Success message */
    .success-banner {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
    }
    
    /* Error message styling */
    .error-banner {
        background: linear-gradient(135deg, #fc8181 0%, #f56565 100%);
        color: white;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #718096;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)


def import_openai():
    """
    Safely import OpenAI library with error handling.
    This prevents app crash if the library is not installed.
    """
    try:
        from openai import OpenAI
        return OpenAI, None
    except ImportError as e:
        return None, f"שגיאה בטעינת ספריית OpenAI: {str(e)}"
    except Exception as e:
        return None, f"שגיאה לא צפויה: {str(e)}"


def get_openai_client():
    """
    Initialize OpenAI client with API key from Streamlit secrets.
    Returns client and error message (if any).
    """
    OpenAI, import_error = import_openai()
    
    if import_error:
        return None, import_error
    
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        client = OpenAI(api_key=api_key)
        return client, None
    except KeyError:
        return None, "🔑 מפתח ה-API לא נמצא! יש להוסיף OPENAI_API_KEY בהגדרות הסודות של Streamlit."
    except Exception as e:
        return None, f"❌ שגיאה באתחול: {str(e)}"


def generate_questions(client, topic: str, difficulty: str, num_questions: int) -> tuple:
    """
    Generate educational questions using OpenAI API.
    
    Args:
        client: OpenAI client instance
        topic: The subject/topic for questions
        difficulty: Grade level (כיתה ב, כיתה ג, מחוננים)
        num_questions: Number of questions to generate
    
    Returns:
        tuple: (questions_text, error_message)
    """
    
    # Map difficulty to Hebrew descriptions
    difficulty_map = {
        "כיתה ב׳ (קל)": "ילדים בכיתה ב׳, בגילאי 7-8. השתמש במילים פשוטות מאוד, משפטים קצרים, ודוגמאות מהחיים היומיומיים של ילדים",
        "כיתה ג׳ (בינוני)": "ילדים בכיתה ג׳, בגילאי 8-9. השתמש בשפה ברורה, אפשר להוסיף מעט מורכבות",
        "מחוננים (מאתגר)": "ילדים מחוננים בכיתות ב-ג, שאוהבים אתגרים. אפשר להוסיף שאלות חשיבה ופתרון בעיות"
    }
    
    difficulty_desc = difficulty_map.get(difficulty, difficulty_map["כיתה ב׳ (קל)"])
    
    # Add randomization seed to ensure uniqueness
    random_seed = random.randint(1, 10000)
    random_style = random.choice([
        "עם דמויות מצחיקות",
        "עם חיות חמודות", 
        "עם גיבורי על",
        "עם נסיכות ונסיכים",
        "עם רובוטים",
        "עם דינוזאורים",
        "עם כדורגלנים",
        "עם אסטרונאוטים"
    ])
    
    prompt = f"""אתה מורה חביב ויצירתי שמכין מבחנים מהנים לילדים.

הנחיות חשובות:
- הנושא: {topic}
- רמת הקושי מותאמת ל{difficulty_desc}
- מספר שאלות: {num_questions}
- סגנון: {random_style}
- מזהה ייחודי: #{random_seed}

כללים:
1. כתוב בעברית פשוטה וברורה
2. כל שאלה חייבת להיות שונה לחלוטין
3. הוסף אימוג׳ים רלוונטיים לכל שאלה 🌟
4. השאלות צריכות להיות מעניינות ומהנות
5. התאם את המורכבות לגיל הילדים
6. אל תחזור על דפוסים - היה יצירתי!

פורמט התשובה:
שאלה 1: [תוכן השאלה עם אימוג׳י]

שאלה 2: [תוכן השאלה עם אימוג׳י]

(וכן הלאה...)

צור {num_questions} שאלות ייחודיות, מקוריות ומהנות על הנושא "{topic}":"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Cost-effective and good for educational content
            messages=[
                {
                    "role": "system",
                    "content": "אתה מומחה ליצירת תוכן חינוכי לילדים בעברית. אתה יצירתי, חביב, ויודע להתאים את השפה לגיל הילדים. כל מבחן שאתה יוצר הוא ייחודי ומקורי."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=1.0,  # Maximum creativity for unique questions
            max_tokens=2000,
            presence_penalty=0.6,  # Encourage diverse content
            frequency_penalty=0.6  # Avoid repetition
        )
        
        questions = response.choices[0].message.content
        return questions, None
        
    except Exception as e:
        error_msg = str(e)
        if "api_key" in error_msg.lower():
            return None, "🔑 בעיה עם מפתח ה-API. אנא בדוק שהמפתח תקין."
        elif "rate_limit" in error_msg.lower():
            return None, "⏳ יותר מדי בקשות! אנא המתן מעט ונסה שוב."
        elif "timeout" in error_msg.lower():
            return None, "⌛ הבקשה לקחה יותר מדי זמן. אנא נסה שוב."
        else:
            return None, f"❌ שגיאה ביצירת השאלות: {error_msg}"


def display_questions(questions_text: str):
    """
    Display questions in a beautiful, child-friendly format.
    """
    # Split questions and display each in a card
    lines = questions_text.strip().split('\n')
    
    question_num = 0
    current_question = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this is a new question
        if line.startswith('שאלה') or (len(line) > 2 and line[0].isdigit() and ('.' in line[:3] or ':' in line[:3])):
            # Display previous question if exists
            if current_question:
                st.markdown(f"""
                <div class="question-card">
                    <span class="question-number">שאלה {question_num} 📝</span>
                    <div class="question-text">{current_question}</div>
                </div>
                """, unsafe_allow_html=True)
            
            question_num += 1
            # Remove the "שאלה X:" prefix for cleaner display
            if ':' in line:
                current_question = line.split(':', 1)[1].strip()
            else:
                current_question = line
        else:
            # Continuation of current question
            current_question += " " + line if current_question else line
    
    # Display last question
    if current_question:
        st.markdown(f"""
        <div class="question-card">
            <span class="question-number">שאלה {question_num} 📝</span>
            <div class="question-text">{current_question}</div>
        </div>
        """, unsafe_allow_html=True)


def main():
    """
    Main application function.
    """
    # ============================================
    # Header Section
    # ============================================
    st.markdown("""
    <div class="main-header">
        <h1>🌟 יוצר המבחנים הקסום 🌟</h1>
        <p>בואו ניצור מבחן מהנה ומיוחד רק בשבילכם!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ============================================
    # Input Section
    # ============================================
    st.markdown("### 📚 בחרו את הנושא והרמה")
    
    col1, col2 = st.columns(2)
    
    with col1:
        topic = st.text_input(
            "🎯 על מה תרצו ללמוד?",
            placeholder="למשל: מערכת השמש, חיבור וחיסור, בעלי חיים...",
            help="כתבו נושא שמעניין אתכם!"
        )
    
    with col2:
        difficulty = st.selectbox(
            "📊 בחרו רמת קושי",
            options=["כיתה ב׳ (קל)", "כיתה ג׳ (בינוני)", "מחוננים (מאתגר)"],
            index=0,
            help="בחרו את הרמה המתאימה לכם"
        )
    
    num_questions = st.select_slider(
        "🔢 כמה שאלות תרצו?",
        options=[3, 5, 7, 10],
        value=5,
        help="בחרו את מספר השאלות"
    )
    
    st.markdown("---")
    
    # ============================================
    # Generate Button Section
    # ============================================
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    
    with col_btn2:
        generate_clicked = st.button(
            "✨ צור מבחן קסום! ✨",
            type="primary",
            use_container_width=True
        )
    
    # ============================================
    # Generation Logic
    # ============================================
    if generate_clicked:
        if not topic or topic.strip() == "":
            st.markdown("""
            <div class="error-banner">
                ⚠️ אופס! שכחתם לכתוב נושא. בבקשה כתבו על מה תרצו ללמוד!
            </div>
            """, unsafe_allow_html=True)
            return
        
        # Initialize OpenAI client
        client, error = get_openai_client()
        
        if error:
            st.markdown(f"""
            <div class="error-banner">
                {error}
            </div>
            """, unsafe_allow_html=True)
            return
        
        # Show loading animation
        with st.spinner("🪄 הקוסם יוצר את המבחן שלכם... רגע קטן!"):
            questions, gen_error = generate_questions(
                client=client,
                topic=topic.strip(),
                difficulty=difficulty,
                num_questions=num_questions
            )
        
        if gen_error:
            st.markdown(f"""
            <div class="error-banner">
                {gen_error}
            </div>
            """, unsafe_allow_html=True)
            return
        
        # Success!
        st.markdown("""
        <div class="success-banner">
            🎉 המבחן מוכן! בהצלחה! 🎉
        </div>
        """, unsafe_allow_html=True)
        
        # Store questions in session state for regeneration
        st.session_state['last_questions'] = questions
        st.session_state['last_topic'] = topic
        st.session_state['last_difficulty'] = difficulty
        st.session_state['last_num'] = num_questions
        
        # Display questions
        st.markdown(f"### 📋 המבחן שלכם בנושא: {topic}")
        display_questions(questions)
        
        # Regenerate button
        st.markdown("---")
        col_regen1, col_regen2, col_regen3 = st.columns([1, 2, 1])
        with col_regen2:
            if st.button("🔄 רוצים שאלות אחרות? לחצו כאן!", use_container_width=True):
                st.rerun()
    
    # ============================================
    # Display previous questions if exist
    # ============================================
    elif 'last_questions' in st.session_state:
        st.markdown("""
        <div class="success-banner">
            📚 המבחן האחרון שיצרתם 📚
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"### 📋 המבחן בנושא: {st.session_state['last_topic']}")
        display_questions(st.session_state['last_questions'])
    
    # ============================================
    # Footer
    # ============================================
    st.markdown("""
    <div class="footer">
        <p>🌟 נוצר באהבה לילדים סקרנים 🌟</p>
        <p>💡 טיפ: כל פעם שתלחצו על הכפתור, תקבלו שאלות חדשות ושונות!</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# Entry Point
# ============================================
if __name__ == "__main__":
    main()