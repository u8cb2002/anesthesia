import streamlit as st
import re

st.set_page_config(page_title="حاسبة أدوية التخدير 💉", page_icon="💉", layout="centered")

# --- CSS Styling ---
st.markdown('''
<style>
    .info-box {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2196F3;
        margin-bottom: 15px;
    }
    .success-box {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin-bottom: 15px;
    }
</style>
''', unsafe_allow_html=True)

st.title("حاسبة أدوية التخدير والتخفيف 💉")
st.markdown("تطبيق عملي لحساب الجرعات وتخفيف الأدوية في صالة العمليات.")

# --- Database ---
drugs_db = {
    "Propofol (بروبوفول)": {"ampoule_mg": 200, "ampoule_ml": 20, "type": "induction", "dose_range": "1.5 - 2.5 mg/kg"},
    "Thiopental (ثيوبنتال)": {"ampoule_mg": 500, "ampoule_ml": 20, "type": "induction", "dose_range": "3 - 5 mg/kg (بعد التخفيف)"}, 
    "Etomidate (إيتوميدات)": {"ampoule_mg": 20, "ampoule_ml": 10, "type": "induction", "dose_range": "0.2 - 0.3 mg/kg"},
    "Ketamine (كيتامين)": {"ampoule_mg": 500, "ampoule_ml": 10, "type": "induction", "dose_range": "1 - 2 mg/kg (IV)"},
    "Midazolam (ميدازولام)": {"ampoule_mg": 15, "ampoule_ml": 3, "type": "sedative", "dose_range": "0.01 - 0.1 mg/kg"}, 
    "Fentanyl (فينتانيل)": {"ampoule_mg": 0.5, "ampoule_ml": 10, "type": "analgesic", "dose_range": "1 - 2 mcg/kg", "unit": "mcg", "ampoule_mcg": 500},
    "Succinylcholine (سكسنيل كولين)": {"ampoule_mg": 100, "ampoule_ml": 2, "type": "muscle_relaxant", "dose_range": "1 - 1.5 mg/kg"}, 
    "Rocuronium (روكورونيوم)": {"ampoule_mg": 50, "ampoule_ml": 5, "type": "muscle_relaxant", "dose_range": "0.6 - 1.2 mg/kg"},
    "Atracurium (أتراكوريوم)": {"ampoule_mg": 50, "ampoule_ml": 5, "type": "muscle_relaxant", "dose_range": "0.5 mg/kg"},
    "Cisatracurium (سيس-أتراكوريوم)": {"ampoule_mg": 10, "ampoule_ml": 5, "type": "muscle_relaxant", "dose_range": "0.15 - 0.2 mg/kg"}
}

# --- UI: Patient Data ---
st.header("1. بيانات المريض 📋")
col1, col2 = st.columns(2)
with col1:
    weight = st.number_input("الوزن (كغم):", min_value=1.0, value=70.0, step=1.0)
with col2:
    age = st.number_input("العمر (سنة):", min_value=1, value=30, step=1)

# --- UI: Drug Selection ---
st.header("2. اختيار الدواء والتخفيف 💊")
selected_drug = st.selectbox("اختر الدواء:", list(drugs_db.keys()))

drug_info = drugs_db[selected_drug]
is_mcg = drug_info.get("unit") == "mcg"

total_drug_amount = drug_info['ampoule_mcg'] if is_mcg else drug_info['ampoule_mg']
unit_str = "ميكروغرام (mcg)" if is_mcg else "ملغم (mg)"

st.markdown(f'''
<div class="info-box">
    <b>معلومات الأمبولة القياسية:</b><br>
    تحتوي الأمبولة على <b>{total_drug_amount} {unit_str}</b> في حجم <b>{drug_info['ampoule_ml']} مل (cc)</b>.<br>
    التركيز الأصلي: <b>{total_drug_amount / drug_info['ampoule_ml']:.1f} {unit_str} / مل</b>.
</div>
''', unsafe_allow_html=True)

# --- UI: Dilution ---
st.subheader("خيارات تخفيف الدواء بالسرنجة 💧")
col_syr1, col_syr2 = st.columns([1, 2])
with col_syr1:
     syringe_size = st.selectbox("حجم السرنجة:", [5, 10, 20, 50], index=1, format_func=lambda x: f"{x} ml (cc)")

dilute_checkbox = st.checkbox("تفعيل ميزة تخفيف الجرعة بالنورمل سلاين (Normal Saline)")
final_volume = drug_info['ampoule_ml']

if dilute_checkbox:
    max_saline = syringe_size - drug_info['ampoule_ml']
    if max_saline > 0:
        added_saline = st.number_input("حجم النورمل سلاين المضاف (ml):", min_value=0.0, max_value=float(max_saline), value=float(max_saline), step=1.0)
        final_volume = drug_info['ampoule_ml'] + added_saline
        st.markdown(f'''
        <div class="success-box">
            <b>التركيز بعد التخفيف:</b><br>
            الحجم الكلي: <b>{final_volume} مل</b>.<br>
            التركيز النهائي أصبح: <b>{total_drug_amount / final_volume:.1f} {unit_str} / مل</b>.
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.warning(f"السرنجة ({syringe_size} مل) صغيرة، اختر سرنجة أكبر للتخفيف.")
else:
    st.info(f"التركيز الحالي: **{total_drug_amount / final_volume:.1f} {unit_str} / مل**")

# --- UI: Dose Calculation ---
st.header("3. الجرعة المقترحة 💉")
st.write(f"الجرعة المعتادة: {drug_info['dose_range']}")

if st.button("احسب الجرعة المطلوبة للحالة"):
    try:
        min_dose_factor_match = re.search(r"([0-9.]+)", drug_info['dose_range'])
        if min_dose_factor_match:
             min_dose_factor = float(min_dose_factor_match.group(1))
             required_amount = min_dose_factor * weight
             concentration_per_ml = total_drug_amount / final_volume
             required_ml = required_amount / concentration_per_ml
             
             st.success(f"الجرعة المطلوبة للوزن ({weight} كغم): **{required_amount:.1f} {unit_str}**")
             st.info(f"👉 يجب إعطاء **{required_ml:.1f} مل (cc)** من السرنجة.")
        else:
             st.warning("يرجى الرجوع للمراجع الطبية لحساب هذا الدواء.")
    except Exception as e:
         st.error(f"حدث خطأ في الحساب.")

st.markdown("---")
st.caption("إخلاء مسؤولية طبية: هذا التطبيق تعليمي ولا يعتبر بديلاً عن القرار السريري.")
