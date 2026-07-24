import streamlit as st

st.set_page_config(page_title="المساعد الشامل للتخدير 💉", page_icon="👨‍⚕️", layout="centered")

# --- CSS Styling ---
st.markdown('''
<style>
    .info-box { background-color: #e8f4f8; color: #000000; padding: 15px; border-radius: 10px; border-left: 5px solid #2196F3; margin-bottom: 15px; }
    .success-box { background-color: #e8f5e9; color: #000000; padding: 15px; border-radius: 10px; border-left: 5px solid #4CAF50; margin-bottom: 15px; }
    .warning-box { background-color: #fff3e0; color: #000000; padding: 15px; border-radius: 10px; border-left: 5px solid #ff9800; margin-bottom: 15px; }
    .danger-box { background-color: #ffebee; color: #000000; padding: 15px; border-radius: 10px; border-left: 5px solid #f44336; margin-bottom: 15px; }
</style>
''', unsafe_allow_html=True)

st.title("المساعد الشامل لطبيب التخدير 👨‍⚕️💉")
st.markdown("تطبيقك الاحترافي والمتكامل لإدارة التخدير في صالة العمليات.")

# --- TABS (7 Tabs) ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📋 التقييم قبل التخدير", 
    "💊 أدوية التخدير", 
    "🚨 الطوارئ", 
    "💧 السوائل", 
    "🫁 مجرى الهواء", 
    "👶 الأطفال", 
    "⚙️ حاسبة TIVA"
])

# ==========================================
# TAB 1: PRE-ANESTHESIA ASSESSMENT (التقييم)
# ==========================================
with tab1:
    st.subheader("التقييم ما قبل التخدير 📋")
    
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("الوزن (كغم):", min_value=1.0, max_value=250.0, value=70.0, step=1.0)
        height = st.number_input("الطول (سم):", min_value=50.0, max_value=220.0, value=170.0, step=1.0)
    with col2:
        age = st.number_input("العمر (سنة):", min_value=0.1, max_value=120.0, value=30.0, step=1.0)
        asa_class = st.selectbox("تصنيف ASA:", [
            "ASA I - مريض سليم طبيعياً",
            "ASA II - مرض جهازى خفيف",
            "ASA III - مرض جهازى شديد محدود الحركة",
            "ASA IV - مرض جِهازى مهدد للحياة",
            "ASA V - مريض ميؤوس من شفائه"
        ])

    # BMI Calculation
    height_m = height / 100.0
    bmi = weight / (height_m ** 2)
    
    if bmi < 18.5: bmi_status = "نحيف (Underweight)"
    elif bmi < 25: bmi_status = "وزن طبيعي (Normal)"
    elif bmi < 30: bmi_status = "زيادة وزن (Overweight)"
    else: bmi_status = "سمنة مفرطة (Obese - تنبيب صعب محتمل)"

    st.markdown(f'''
    <div class="info-box">
        <b>مؤشر كتلة الجسم (BMI):</b> {bmi:.1f} ({bmi_status})
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("### 🫁 تقييم مجرى الهواء والفحوصات السريرية")
    mallampati = st.selectbox("تصنيف مالامباتي (Mallampati):", [
        "Class I - رؤية الحنك الكامل (سهل جداً)",
        "Class II - رؤية سقف الحلق اللين",
        "Class III - رؤية قاعدة اللهاة فقط",
        "Class IV - اللهاة غير مرئية تماماً (تنبيب صعب جداً)"
    ])
    
    npo_status = st.selectbox("حالة الصيام (NPO):", [
        "صائم كلياً للفترة الموصى بها (أمان كامل)",
        "غير صائم / أكل طعام صلب مؤخراً (خطر الاستنشاق Aspiration)"
    ])

    if "غير صائم" in npo_status:
        st.markdown('<div class="danger-box">⚠️ <b>تحذير خطر استنشاق (Aspiration Risk):</b> يفضل تأجيل الجراحة أو اتخاذ احتياطات التخدير السريع (RSI).</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="success-box">✅ حالة الصيام ممتازة وجاهزة للتخدير.</div>', unsafe_allow_html=True)

# ==========================================
# TAB 2: ANESTHESIA DRUGS
# ==========================================
with tab2:
    st.subheader("حاسبة أدوية التخدير والتخفيف 💊")
    
    drugs_db = {
        "Propofol (بروبوفول)": {"total_amount": 200, "ampoule_ml": 20, "default_dose": 2.0, "unit": "mg"},
        "Thiopental (ثيوبنتال)": {"total_amount": 500, "ampoule_ml": 20, "default_dose": 4.0, "unit": "mg"}, 
        "Etomidate (إيتوميدات)": {"total_amount": 20, "ampoule_ml": 10, "default_dose": 0.25, "unit": "mg"},
        "Ketamine (كيتامين)": {"total_amount": 500, "ampoule_ml": 10, "default_dose": 1.5, "unit": "mg"},
        "Midazolam (ميدازولام)": {"total_amount": 15, "ampoule_ml": 3, "default_dose": 0.05, "unit": "mg"}, 
        "Fentanyl (فينتانيل)": {"total_amount": 500, "ampoule_ml": 10, "default_dose": 1.5, "unit": "mcg"},
        "Succinylcholine (سكسنيل كولين)": {"total_amount": 100, "ampoule_ml": 2, "default_dose": 1.0, "unit": "mg"}, 
        "Rocuronium (روكورونيوم)": {"total_amount": 50, "ampoule_ml": 5, "default_dose": 0.6, "unit": "mg"},
        "Atracurium (أتراكوريوم)": {"total_amount": 50, "ampoule_ml": 5, "default_dose": 0.5, "unit": "mg"}
    }

    selected_drug = st.selectbox("اختر الدواء:", list(drugs_db.keys()))
    drug_info = drugs_db[selected_drug]
    is_mcg = drug_info["unit"] == "mcg"
    unit_str = "ميكروغرام (mcg)" if is_mcg else "ملغم (mg)"

    st.markdown(f'''
    <div class="info-box">
        <b>معلومات الأمبولة القياسية:</b><br>
        تحتوي الأمبولة على <b>{drug_info['total_amount']} {unit_str}</b> في حجم <b>{drug_info['ampoule_ml']} مل (cc)</b>.<br>
        التركيز الأصلي: <b>{drug_info['total_amount'] / drug_info['ampoule_ml']:.1f} {unit_str} / مل</b>.
    </div>
    ''', unsafe_allow_html=True)

    dilute_checkbox = st.checkbox("تفعيل ميزة التخفيف بالنورمل سلاين")
    final_volume = drug_info['ampoule_ml']

    if dilute_checkbox:
        added_saline = st.number_input("حجم النورمل سلاين المضاف (ml):", min_value=0.0, value=0.0, step=1.0)
        final_volume = drug_info['ampoule_ml'] + added_saline
        st.markdown(f'<div class="success-box">التركيز بعد التخفيف أصبح: <b>{drug_info["total_amount"] / final_volume:.1f} {unit_str} / مل</b> (بحجم كلي {final_volume} مل).</div>', unsafe_allow_html=True)

    custom_dose = st.number_input(f"الجرعة المطلوبة ({drug_info['unit']}/kg):", min_value=0.01, value=float(drug_info['default_dose']), step=0.1)

    if st.button("احسب جرعة التخدير المطلوبة"):
        required_amount = custom_dose * weight
        concentration_per_ml = drug_info['total_amount'] / final_volume
        required_ml = required_amount / concentration_per_ml
        
        st.success(f"الجرعة المطلوبة للوزن ({weight} كغم): **{required_amount:.1f} {unit_str}**")
        st.info(f"👉 يجب إعطاء **{required_ml:.1f} مل (cc)** من السرنجة.")

# ==========================================
# TAB 3: EMERGENCY DRUGS
# ==========================================
with tab3:
    st.subheader("أدوية الطوارئ والإنعاش 🚨")
    st.markdown('''
    <div class="danger-box">
        <b>1. Ephedrine (إيفيدرين)</b><br>
        • اسحب 1ml وضيف 9ml سلاين = التركيز (5mg / ml).<br>
        • الجرعة: 1 إلى 2 ml حسب الاستجابة لرفع الضغط.
    </div>
    <div class="warning-box">
        <b>2. Atropine (أتروبين)</b><br>
        • الجرعة للبالغين: 0.5mg كل 3-5 دقائق لعلاج البطء القلبي.
    </div>
    <div class="danger-box">
        <b>3. Adrenaline (أدرينالين)</b><br>
        • طوارئ عادية: يخفف إلى 10ml (100mcg/ml).<br>
        • إنعاش قلبي (CPR): 1mg كامل بدون تخفيف.
    </div>
    ''', unsafe_allow_html=True)

# ==========================================
# TAB 4: FLUID MANAGEMENT
# ==========================================
with tab4:
    st.subheader("حاسبة السوائل الوريدية (Fluids) 💧")
    if weight <= 10: maintenance_fluid = weight * 4
    elif weight <= 20: maintenance_fluid = 40 + ((weight - 10) * 2)
    else: maintenance_fluid = 60 + (weight - 20)
        
    st.markdown(f'<div class="info-box">الاحتياج الأساسي للسوائل: <br><h3>{maintenance_fluid} مل / ساعة (ml/hr)</h3></div>', unsafe_allow_html=True)
    
    fasting_hours = st.number_input("عدد ساعات الصيام (Fasting Hours):", min_value=0, max_value=24, value=8, step=1)
    if fasting_hours > 0:
        deficit = maintenance_fluid * fasting_hours
        st.markdown(f'<div class="warning-box"><b>تعويض الصيام:</b> {deficit} مل.<br>الساعة الأولى: <b>{deficit / 2} مل</b><br>الساعة الثانية والثالثة: <b>{deficit / 4} مل</b> لكل ساعة.</div>', unsafe_allow_html=True)

# ==========================================
# TAB 5: AIRWAY EQUIPMENT
# ==========================================
with tab5:
    st.subheader("أدوات مجرى الهواء المقترحة 🫁")
    if age < 1: ett_size = "3.5 - 4.0"
    elif age < 16: ett_size = f"{(age / 4) + 4:.1f} (بدون بالون) / {(age / 4) + 3.5:.1f} (مع بالون)"
    else: ett_size = "7.0 للنسـاء / 8.0 للرجـال (بشكل عام)"

    if weight < 5: lma_size = "1"
    elif weight < 10: lma_size = "1.5"
    elif weight < 20: lma_size = "2"
    elif weight < 30: lma_size = "2.5"
    elif weight < 50: lma_size = "3"
    elif weight < 70: lma_size = "4"
    else: lma_size = "5"

    st.markdown(f'<div class="success-box"><b>الأنبوب الرغامي (ETT):</b> {ett_size}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-box"><b>القناع الحنجري (LMA):</b> {lma_size}</div>', unsafe_allow_html=True)

# ==========================================
# TAB 6: PEDIATRIC ANESTHESIA
# ==========================================
with tab6:
    st.subheader("حسابات الأطفال الخاصة 👶")
    
    if age >= 1 and age <= 10:
        est_weight = (age * 2) + 8
        st.info(f"⚖️ الوزن التقديري المعتاد لعمر {age} سنة هو: **{est_weight} كغم**")
    
    if age <= 1: ebv = weight * 85
    elif age <= 6: ebv = weight * 75
    else: ebv = weight * 70
    
    tube_depth = (age / 2) + 12

    st.markdown(f'''
    <div class="success-box">
        <b>حجم الدم الكلي التقديري (EBV):</b><br>
        • {ebv} مل (لحساب الحد الأقصى للنزيف المسموح).
    </div>
    <div class="info-box">
        <b>عمق تثبيت الأنبوب الرغامي:</b><br>
        • {tube_depth:.1f} سم (عند الشفة الأمامية).
    </div>
    <div class="danger-box">
        <b>جرعات الطوارئ الخاصة بوزن ({weight} كغم):</b><br>
        • <b>Atropine:</b> {weight * 0.02:.2f} mg (الحد الأدنى 0.1 mg).<br>
        • <b>Adrenaline:</b> {weight * 10:.0f} mcg (مايكروغرام).
    </div>
    ''', unsafe_allow_html=True)

# ==========================================
# TAB 7: TIVA PUMP CALCULATOR
# ==========================================
with tab7:
    st.subheader("حاسبة التسريب الوريدي المستمر (TIVA Infusion Pump) ⚙️")
    st.markdown("تحويل جرعة الدواء إلى سرعة مضخة التسريب بالـ (ml/hr).")
    
    tiva_drug = st.selectbox("اختر دواء التسريب:", ["Propofol (1%) - 10 mg/ml"])
    tiva_dose = st.number_input("الجرعة المطلوبة (mg/kg/hr):", min_value=1.0, max_value=20.0, value=6.0, step=0.5)
    
    concentration = 10.0 # mg/ml for Propofol 1%
    
    if st.button("احسب سرعة المضخة (Pump Rate)"):
        pump_rate = (tiva_dose * weight) / concentration
        st.markdown(f'''
        <div class="success-box">
            ضبط مضخة التسريب (Syringe Pump):<br>
            <h2>{pump_rate:.1f} ml / hr</h2>
        </div>
        ''', unsafe_allow_html=True)

st.markdown("---")
st.caption("إخلاء مسؤولية طبية: هذا التطبيق تعليمي ولا يعتبر بديلاً عن القرار السريري في صالة العمليات.")
