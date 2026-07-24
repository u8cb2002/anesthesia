import streamlit as st
from PIL import Image
from google import genai

st.set_page_config(page_title="المساعد الشامل للتخدير 💉", page_icon="👨‍⚕️", layout="centered")

# --- CSS Styling ---
st.markdown('''
<style>
    .info-box { background-color: #e8f4f8; color: #000000; padding: 15px; border-radius: 10px; border-left: 5px solid #2196F3; margin-bottom: 15px; }
    .success-box { background-color: #e8f5e9; color: #000000; padding: 15px; border-radius: 10px; border-left: 5px solid #4CAF50; margin-bottom: 15px; }
    .warning-box { background-color: #fff3e0; color: #000000; padding: 15px; border-radius: 10px; border-left: 5px solid #ff9800; margin-bottom: 15px; }
    .danger-box { background-color: #ffebee; color: #000000; padding: 15px; border-radius: 10px; border-left: 5px solid #f44336; margin-bottom: 15px; }
    .card-box { background-color: #f8f9fa; color: #000000; padding: 15px; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 15px; }
</style>
''', unsafe_allow_html=True)

st.title("المساعد الشامل لطبيب التخدير 👨‍⚕️💉")
st.markdown("منصتك الأكاديمية والعملية المعتمدة في صالة العمليات.")

# --- TABS (8 Tabs) ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📋 التقييم قبل التخدير", 
    "💊 موسوعة الأدوية", 
    "🚨 الطوارئ", 
    "💧 السوائل", 
    "🫁 مجرى الهواء", 
    "👶 الأطفال", 
    "⚙️ حاسبة TIVA",
    "🤖 مساعد التخدير الذكي"
])

# ==========================================
# TAB 1: PRE-ANESTHESIA ASSESSMENT
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
# TAB 2: COMPREHENSIVE DRUGS ENCYCLOPEDIA
# ==========================================
with tab2:
    st.subheader("موسوعة الأدوية الأكاديمية والشاملة 💊")
    
    drugs_db = {
        "Propofol (بروبوفول)": {
            "generic": "Propofol", "trade": "Diprivan, Fresofol", "class": "Intravenous Sedative / Hypnotic",
            "total_amount": 200, "ampoule_ml": 20, "default_dose": 2.0, "unit": "mg",
            "pediatric_dose": "2.5 - 3.5 mg/kg (للإحداث)", "route": "Intravenous (IV) Bolus / Infusion",
            "mechanism": "تعزيز تأثير الناقل العصبي المثبط GABA في الدماغ.",
            "onset": "30 - 45 ثانية", "duration": "5 - 10 دقائق", "half_life": "1.5 - 3 ساعات",
            "contraindications": "حساسية من الصويا أو البيض، هبوط حاد غير مصلح في ضغط الدم.",
            "side_effects": "هبوط ضغط الدم، توسع الأوعية الدموية، ألم في مكان الحقن.",
            "interactions": "يزيد تأثير الأدوية المثبطة للجهاز العصبي المركزي.",
            "storage": "يحفظ في درجة حرارة الغرفة ولا يجمد."
        },
        "Thiopental (ثيوبنتال)": {
            "generic": "Thiopental Sodium", "trade": "Pentothal", "class": "Barbiturate Anesthetic",
            "total_amount": 500, "ampoule_ml": 20, "default_dose": 4.0, "unit": "mg",
            "pediatric_dose": "5 - 6 mg/kg", "route": "Intravenous (IV) Bolus",
            "mechanism": "تثبيط التوصيل العصبي الشبكي وزيادة تأثير GABA.",
            "onset": "30 ثانية", "duration": "5 - 10 دقائق", "half_life": "5 - 11 ساعة",
            "contraindications": "مرض البورفيريا الحاد (Porphyria)، انخفاض ضغط الدم الشديد.",
            "side_effects": "هبوط حاد بالضغط، تثبيط تنفسي، تقرحات شديدة عند الحقن خارج العرق.",
            "interactions": "يتفاعل مع مسكنات الأفيون مسبباً هبوطاً مضاعفاً.",
            "storage": "يحفظ على شكل بودرة ويحلل قبل الاستخدام مباشرة."
        },
        "Etomidate (إيتوميدات)": {
            "generic": "Etomidate", "trade": "Amidate", "class": "Carboxylated Imidazole (Hypnotic)",
            "total_amount": 20, "ampoule_ml": 10, "default_dose": 0.25, "unit": "mg",
            "pediatric_dose": "0.2 - 0.3 mg/kg", "route": "Intravenous (IV) Bolus",
            "mechanism": "منوم سريع يعمل على مستقبلات GABA بدون تأثير أفيوني أو مسكن.",
            "onset": "30 - 60 ثانية", "duration": "3 - 5 دقائق", "half_life": "2.5 - 5 ساعات",
            "contraindications": "فرط الحساسية، تثبيط قشرة الكظر المزمن (في التسريب الطويل).",
            "side_effects": "رعشة عضلية مؤقتة (Myoclonus)، ألم في مكان الحقن، تثبيط مؤقت للكورتيزول.",
            "interactions": "يزيد تأثيره مع المهديات العصبية.",
            "storage": "يحفظ في درجة حرارة الغرفة بعيداً عن الضوء."
        },
        "Ketamine (كيتامين)": {
            "generic": "Ketamine Hydrochloride", "trade": "Ketalar", "class": "Dissociative Anesthetic",
            "total_amount": 500, "ampoule_ml": 10, "default_dose": 1.5, "unit": "mg",
            "pediatric_dose": "1 - 2 mg/kg (IV) أو 4 - 5 mg/kg (IM)", "route": "Intravenous / Intramuscular",
            "mechanism": "مستقبلات NMDA antagonist، يسبب انفصال الوظائف العصبية.",
            "onset": "45 - 60 ثانية", "duration": "10 - 20 دقيقة", "half_life": "2 - 3 ساعات",
            "contraindications": "ارتفاع ضغط الدم الشديد، أمراض الشريان التاجي، ارتفاع ضغط الدماغ.",
            "side_effects": "ارتفاع ضغط الدم، زيادة نبض القلب، هلوسة عند الاستيقاظ.",
            "interactions": "يتفاعل مع أدوية الغدة الدرقية مسبباً ارتفاعاً خطيراً بالضغط.",
            "storage": "يحفظ بعيداً عن الضوء في درجات الحرارة العادية."
        },
        "Midazolam (ميدازولام)": {
            "generic": "Midazolam", "trade": "Versed", "class": "Benzodiazepine",
            "total_amount": 15, "ampoule_ml": 3, "default_dose": 0.05, "unit": "mg",
            "pediatric_dose": "0.05 - 0.1 mg/kg", "route": "Intravenous / Intramuscular / Oral",
            "mechanism": "يزيد تدفق أيونات الكلور عبر مستقبلات GABA-A.",
            "onset": "1 - 3 دقائق", "duration": "30 - 60 دقيقة", "half_life": "1.5 - 2.5 ساعة",
            "contraindications": "الجلوكوما زاوية الإغلاق الحادة، التثبيط التنفسي الحاد.",
            "side_effects": "نعاس طويل، هبوط خفيف بالضغط، ضعف الذاكرة المؤقت (Amnesia).",
            "interactions": "تزداد خطورة تثبيط التنفس عند خلطه مع الأفيونات.",
            "storage": "يحفظ في مكان بارد ومظلم."
        },
        "Fentanyl (فينتانيل)": {
            "generic": "Fentanyl Citrate", "trade": "Sublimaze", "class": "Opioid Analgesic",
            "total_amount": 500, "ampoule_ml": 10, "default_dose": 1.5, "unit": "mcg",
            "pediatric_dose": "1 - 2 mcg/kg", "route": "Intravenous (IV) / Epidural",
            "mechanism": "يرتبط بمستقبلات الأفيون (Mu-opioid receptors) في الجهاز العصبي المركزي.",
            "onset": "1 - 2 دقائق", "duration": "30 - 60 دقيقة", "half_life": "2 - 4 ساعات",
            "contraindications": "القصور التنفسي الحاد، الحساسية المفرطة للمركب.",
            "side_effects": "توقف التنفس، بطء القلب، تصلب جدار الصدر عند الحقن السريع.",
            "interactions": "يثبط التنفس بشدة مع المهدئات.",
            "storage": "يحفظ في مكان مظلم وبارد وتحت الرقابة."
        },
        "Succinylcholine (سكسنيل كولين)": {
            "generic": "Succinylcholine Chloride", "trade": "Anectine", "class": "Depolarizing Neuromuscular Blocker",
            "total_amount": 100, "ampoule_ml": 2, "default_dose": 1.0, "unit": "mg",
            "pediatric_dose": "1.5 - 2 mg/kg", "route": "Intravenous (IV) Bolus",
            "mechanism": "يحاكي الأسيتيل كولين مسبباً إزالة استقطاب مستمرة وعجز عضلي سريع.",
            "onset": "30 - 60 ثانية", "duration": "4 - 6 دقائق", "half_life": "قصير جداً (دقائق معدودة)",
            "contraindications": "مرضى الحروق المتقدمة، ارتفاع بوتاسيوم الدم، تاريخ عائلي لفرط الحرارة الخبيث.",
            "side_effects": "ارتفاع البوتاسيوم بالدم، آلام عضلية بعد الإفاقة، ارتفاع حرارة خبيث.",
            "interactions": "تتداخل أدوية الفوسفور العضوي لزيادة مدة تأثيره.",
            "storage": "يحفظ حصراً في الثلاجة (2-8 درجات مئوية)."
        },
        "Rocuronium (روكورونيوم)": {
            "generic": "Rocuronium Bromide", "trade": "Esmeron", "class": "Non-depolarizing Neuromuscular Blocker",
            "total_amount": 50, "ampoule_ml": 5, "default_dose": 0.6, "unit": "mg",
            "pediatric_dose": "0.6 mg/kg", "route": "Intravenous (IV) Bolus",
            "mechanism": "منافسة الأسيتيل كولين على مستقبلات العضلات الهيكلية لمنع التقلص.",
            "onset": "60 - 90 ثانية", "duration": "30 - 40 دقيقة", "half_life": "1 - 2 ساعة",
            "contraindications": "فرط الحساسية للمادة.",
            "side_effects": "ردود فعل تحسسية نادرة، ارتفاع طفيف بمعدل ضربات القلب.",
            "interactions": "تطيل أمد تأثيره المضادات الحيوية (Aminoglycosides).",
            "storage": "يحفظ في الثلاجة حصراً لتجنب تلفه."
        },
        "Atracurium (أتراكوريوم)": {
            "generic": "Atracurium Besylate", "trade": "Tracrium", "class": "Non-depolarizing Neuromuscular Blocker",
            "total_amount": 50, "ampoule_ml": 5, "default_dose": 0.5, "unit": "mg",
            "pediatric_dose": "0.4 - 0.5 mg/kg", "route": "Intravenous (IV) Bolus",
            "mechanism": "يحصر مستقبلات الأسيتيل كولين ويتحلل ذاتياً في الدم (Hofmann elimination).",
            "onset": "2 - 3 دقائق", "duration": "20 - 35 دقيقة", "half_life": "20 دقيقة",
            "contraindications": "فرط الحساسية للمادة.",
            "side_effects": "تحرير الهيستامين، احمرار خفيف بالجلد، هبوط خفيف مؤقت بالضغط.",
            "interactions": "يتأثر بالوسط الحامضي والقاعدي للمحاليل الوريدية.",
            "storage": "يحفظ في الثلاجة حصراً لتجنب تلفه."
        }
    }

    selected_drug = st.selectbox("اختر الدواء لاستعراض بطاقته الأكاديمية الكاملة:", list(drugs_db.keys()))
    d = drugs_db[selected_drug]
    is_mcg = d["unit"] == "mcg"
    unit_str = "ميكروغرام (mcg)" if is_mcg else "ملغم (mg)"

    st.markdown(f'''
    <div class="card-box">
        <h3>📖 البطاقة الأكاديمية: {selected_drug}</h3>
        <hr>
        • <b>الاسم العلمي (Generic):</b> {d['generic']}<br>
        • <b>الاسم التجاري (Trade Name):</b> {d['trade']}<br>
        • <b>التصنيف العلمي (Class):</b> {d['class']}<br>
        • <b>طريقة الإعطاء (Route):</b> {d['route']}<br>
        • <b>جرعة الأطفال (Pediatric Dose):</b> {d['pediatric_dose']}<br>
        <br>
        <b>⚙️ الفارماكولوجي وميكانيزم العمل:</b><br>
        • {d['mechanism']}<br>
        • <b>بداية التأثير (Onset):</b> {d['onset']} | <b>المدة (Duration):</b> {d['duration']}<br>
        • <b>نصف العمر (Half-life):</b> {d['half_life']}<br>
        <br>
        ⚠️ <b>موانع الاستخدام (Contraindications):</b> {d['contraindications']}<br>
        🛑 <b>الآثار الجانبية (Side Effects):</b> {d['side_effects']}<br>
        🔄 <b>التداخلات الدوائية (Interactions):</b> {d['interactions']}<br>
        📦 <b>كيفية الحفظ (Storage):</b> {d['storage']}
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🧮 حاسبة الجرعات والتخفيف السريرية")
    
    st.markdown(f'''
    <div class="info-box">
        <b>معلومات الأمبولة القياسية:</b><br>
        تحتوي الأمبولة على <b>{d['total_amount']} {unit_str}</b> في حجم <b>{d['ampoule_ml']} مل (cc)</b>.<br>
        التركيز الأصلي: <b>{d['total_amount'] / d['ampoule_ml']:.1f} {unit_str} / مل</b>.
    </div>
    ''', unsafe_allow_html=True)

    dilute_checkbox = st.checkbox("تفعيل ميزة التخفيف بالنورمل سلاين")
    final_volume = d['ampoule_ml']

    if dilute_checkbox:
        added_saline = st.number_input("حجم النورمل سلاين المضاف (ml):", min_value=0.0, value=0.0, step=1.0)
        final_volume = d['ampoule_ml'] + added_saline
        st.markdown(f'<div class="success-box">التركيز بعد التخفيف أصبح: <b>{d["total_amount"] / final_volume:.1f} {unit_str} / مل</b> (بحجم كلي {final_volume} مل).</div>', unsafe_allow_html=True)

    custom_dose = st.number_input(f"الجرعة المطلوبة ({d['unit']}/kg):", min_value=0.01, value=float(d['default_dose']), step=0.1)

    if st.button("احسب الجرعة وكمية الحقن"):
        required_amount = custom_dose * weight
        concentration_per_ml = d['total_amount'] / final_volume
        required_ml = required_amount / concentration_per_ml
        
        st.success(f"الجرعة المطلوبة للوزن ({weight} كغم): **{required_amount:.1f} {unit_str}**")
        st.info(f"👉 يجب إعطاء **{required_ml:.1f} مل (cc)** من السرنجة بدقة.")

# ==========================================
# TAB 3: EMERGENCY DRUGS
# ==========================================
with tab3:
    st.subheader("أدوية الطوارئ والإنعاش 🚨")
    st.markdown('''
    <div class="danger-box">
        <b>1. Ephedrine (إيفيدرين)</b><br>
        • الاستخدام: لرفع ضغط الدم الهابط أثناء التخدير.<br>
        • التخفيف: اسحب 1ml وضيف 9ml سلاين = التركيز (5mg / ml).<br>
        • الجرعة: 1 إلى 2 ml حسب الاستجابة.
    </div>
    <div class="warning-box">
        <b>2. Atropine (أتروبين)</b><br>
        • الاستخدام: لعلاج البطء القلبي الشديد (Bradycardia).<br>
        • الجرعة للبالغين: 0.5mg كل 3-5 دقائق.
    </div>
    <div class="danger-box">
        <b>3. Adrenaline (أدرينالين)</b><br>
        • الاستخدام: صدمة الحساسية أو توقف القلب.<br>
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

# ==========================================
# TAB 8: AI ANESTHESIA ASSISTANT (GEMINI)
# ==========================================
with tab8:
    st.subheader("🤖 مساعد التخدير الذكي (مدعوم بـ Google Gemini)")
    st.markdown("اسأل عن أي موضوع طبي، أو ارفع صورة (تخطيط قلب، أدوية، شاشة مراقبة) ليتم تحليلها فوراً.")

    api_key_input = st.text_input("أدخل مفتاح Google Gemini API Key الخاص بك:", type="password")

    uploaded_image = st.file_uploader("اختر صورة للتحليل (اختياري - PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"])

    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption="الصورة المرفوعة للمراجعة", use_container_width=True)

    user_query = st.text_area("اكتب سؤالك الطبي هنا:", placeholder="مثلاً: ما هي دواعي استعمال دواء كذا؟ أو اشرح لي هذا التخطيط...")

    if st.button("إرسال للمساعد الذكي"):
        if not api_key_input:
            st.error("الرجاء إدخال مفتاح الـ API الخاص بـ Gemini أولاً.")
        elif not user_query and not uploaded_image:
            st.warning("الرجاء كتابة سؤال أو رفع صورة على الأقل.")
        else:
            try:
                # استخدام SDK الحديث google-genai
                client = genai.Client(api_key=api_key_input)

                system_instruction = (
                    "أنت مساعد ذكي ومحترف متخصص حصراً في مجال التخدير، العناية المركزة، والإنعاش الطبي. "
                    "يجب أن تجيب فقط على الأسئلة والاستفسارات المتعلقة بهذا المجال الطبي والأدوية والعمليات. "
                    "إذا سأل المستخدم عن أي موضوع خارج التخدير والطب، اعتذر بلطف ورفض الإجابة. "
                    "دائماً أضف تنبيه في نهاية إجابتك بأن هذه المعلومات تعليمية ومساعدة وليست بديلاً عن القرار السريري الطبي المباشر."
                )

                contents = [system_instruction, f"سؤال المستخدم: {user_query}"]
                if uploaded_image is not None:
                    contents.append(image)

                with st.spinner("جاري تحليل الطلب بواسطة الذكاء الاصطناعي..."):
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=contents,
                    )
                    st.markdown("### 💡 الإجابة والتحليل:")
                    st.success(response.text)

            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")

st.markdown("---")
st.caption("إخلاء مسؤولية طبية: هذا التطبيق تعليمي ولا يعتبر بديلاً عن القرار السريري في صالة العمليات.")
