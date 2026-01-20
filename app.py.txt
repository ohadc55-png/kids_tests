import streamlit as st
import google.generativeai as genai
import json

# --- הגדרות עיצוב ודף ---
st.set_page_config(
    page_title="הכנה למחוננים - משחקים ולומדים",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS להתאמה לילדים ולעברית ---
st.markdown("""
<style>
    /* יישור לימין וכיוון כתיבה */
    .stApp {
        direction: rtl;
        text-align: right;
    }
    
    /* עיצוב כותרות */
    h1 {
        color: #4B0082; /* אינדיגו */
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* עיצוב כפתורי רדיו (התשובות) שיהיו גדולים ונוחים */
    .stRadio > div {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #ffffff;
    }
    
    /* הסתרת אלמנטים מיותרים של סטרימליט */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* עיצוב כפתור בדיקה */
    div.stButton > button {
        width: 100%;
        background-color: #FFD700;
        color: black;
        font-weight: bold;
        border-radius: 12px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- הגדרת ה-API ---
# הערה: בסביבת ייצור עדיף להשתמש ב-st.secrets
API_KEY = "YOUR_API_KEY_HERE" 

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("נא להגדיר API KEY בקוד")

# --- פונקציה ליצירת שאלה מה-AI ---
def get_ai_question(stage):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    if stage == "שלב א' (סינון)":
        topic_prompt = "חשבון בסיסי (כפל/חילוק עד 100), השלמת משפטים פשוטה, או ידע כללי לילדים."
        difficulty = "רמה בסיסית מותאמת לכיתה ב'."
    else:
        topic_prompt = "צורות (יוצא דופן), אנלוגיות מילוליות, סדרות לוגיות, או בעיות מילוליות."
        difficulty = "רמה גבוהה המותאמת למבחן איתור מחוננים (מאתגר)."

    # הפרומפט המדויק שמבקש JSON
    prompt = f"""
    אתה מורה המכין תלמידים למבחן מחוננים בישראל.
    צור שאלה אמריקאית אחת חדשה ומקורית בנושא: {topic_prompt}
    רמת הקושי: {difficulty}
    
    עליך להחזיר פלט בפורמט JSON בלבד, ללא טקסט נוסף לפני או אחרי.
    המבנה חייב להיות כזה:
    {{
        "question": "השאלה עצמה...",
        "options": ["אפשרות 1", "אפשרות 2", "אפשרות 3", "אפשרות 4"],
        "correct_answer": "האפשרות הנכונה (העתק מדויק של הטקסט)",
        "explanation": "הסבר קצר וידידותי לילד למה זו התשובה"
    }}
    וודא שהעברית תקינה לחלוטין.
    """
    
    try:
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        return json.loads(response.text)
    except Exception as e:
        return None

# --- ניהול מצב (Session State) ---
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game_active' not in st.session_state:
    st.session_state.game_active = False
if 'selected_stage' not in st.session_state:
    st.session_state.selected_stage = None
if 'answered' not in st.session_state:
    st.session_state.answered = False

# --- מסך ראשי ---
if not st.session_state.game_active:
    st.title("🚀 מוכנים לאתגר המחוננים?")
    st.markdown("### בחרו את המבחן שלכם:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🌟 שלב ב' - האתגר האמיתי", use_container_width=True):
            st.session_state.selected_stage = "שלב ב' (איתור)"
            st.session_state.game_active = True
            st.rerun()
            
    with col2:
        if st.button("📝 שלב א' - חימום", use_container_width=True):
            st.session_state.selected_stage = "שלב א' (סינון)"
            st.session_state.game_active = True
            st.rerun()

    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=150) # תמונה נחמדה להוסיף צבע

# --- מסך השאלות ---
else:
    # כותרת עם כפתור חזרה
    col_header, col_back = st.columns([3, 1])
    with col_header:
        st.subheader(f"🎯 מבחן {st.session_state.selected_stage}")
    with col_back:
        if st.button("🏠 יציאה"):
            st.session_state.game_active = False
            st.session_state.current_question = None
            st.session_state.answered = False
            st.rerun()
            
    st.progress(st.session_state.score % 100) # סתם בר התקדמות ויזואלי

    # אם אין שאלה כרגע - טוענים חדשה
    if st.session_state.current_question is None:
        with st.spinner('🤖 ה-AI מכין שאלה מיוחדת בשבילך...'):
            q_data = get_ai_question(st.session_state.selected_stage)
            if q_data:
                st.session_state.current_question = q_data
                st.session_state.answered = False
            else:
                st.error("אופס, הייתה בעיה בטעינת השאלה. נסה שוב.")
                if st.button("נסה שוב"):
                    st.rerun()
    
    # הצגת השאלה
    if st.session_state.current_question:
        q = st.session_state.current_question
        
        st.markdown(f"#### ❓ {q['question']}")
        
        # טופס הבחירה
        user_choice = st.radio(
            "בחר את התשובה הנכונה:",
            q['options'],
            index=None,
            key="radio_choice",
            disabled=st.session_state.answered
        )

        # כפתור בדיקה
        if not st.session_state.answered:
            if st.button("בדוק תשובה 👈"):
                if user_choice:
                    st.session_state.answered = True
                    st.rerun() # טוען מחדש כדי להציג את התוצאה
                else:
                    st.warning("יש לבחור תשובה לפני הבדיקה")
        
        # הצגת התוצאה
        else:
            if st.session_state.radio_choice == q['correct_answer']:
                st.balloons()
                st.success(f"**כל הכבוד!** תשובה נכונה. 🎉")
                st.session_state.score += 10
            else:
                st.error(f"לא נורא! התשובה הנכונה היא: **{q['correct_answer']}**")
            
            st.info(f"💡 הסבר: {q['explanation']}")
            
            if st.button("לשאלה הבאה ➡️"):
                st.session_state.current_question = None
                st.session_state.answered = False
                st.rerun()