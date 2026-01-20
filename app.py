import streamlit as st
from openai import OpenAI

# כותרת האפליקציה
st.title("מחולל מבחנים ושאלות (OpenAI)")

# 1. בדיקה שהמפתח קיים בסיקרטס כדי למנוע קריסה
if "OPENAI_API_KEY" not in st.secrets:
    st.error("נא להגדיר OPENAI_API_KEY ב-Streamlit Secrets")
    st.stop()

# 2. אתחול הלקוח של OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 3. ממשק המשתמש - קבלת נושא או בקשה
user_input = st.text_area("על מה תרצה לייצר שאלות/מבחן היום?", "לדוגמה: מבחן בחשבון לכיתה ד' בנושא שברים")

# 4. כפתור לפעולה
if st.button("צור תוכן"):
    if not user_input:
        st.warning("אנא כתוב משהו בתיבת הטקסט.")
    else:
        with st.spinner("חושב ומייצר..."):
            try:
                # 5. הקריאה ל-OpenAI API
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",  # או gpt-4o אם יש לך גישה
                    messages=[
                        # כאן אתה מגדיר לבוט מי הוא. שיניתי את זה למורה/מחנך לאור שם הקובץ שלך
                        {"role": "system", "content": "אתה עוזר חינוכי מומחה ביצירת מבחנים ושאלות לילדים."},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.7, # יצירתיות (0 = מקובע, 1 = יצירתי מאוד)
                )

                # 6. הצגת התשובה
                generated_text = response.choices[0].message.content
                st.markdown("### התוצאה:")
                st.write(generated_text)

            except Exception as e:
                st.error(f"אירעה שגיאה: {e}")

# תוספת קטנה לצד (Sidebar)
st.sidebar.info("אפליקציה זו משתמשת במודל של OpenAI")