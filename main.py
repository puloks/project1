import streamlit as st
import requests
from deep_translator import GoogleTranslator

st.set_page_config(page_title='Leaf Disease Detection', layout='wide')

if 'lang' not in st.session_state:
    st.session_state.lang='English'

translations={
'English':{'title':'Leaf Disease Detection','desc':'Upload a leaf image and detect diseases instantly.','upload':'Upload Leaf Image','detect':'🔍 Detect Disease','preview':'Preview','loading':'Analyzing image...'},
'বাংলা':{'title':'পাতার রোগ শনাক্তকরণ','desc':'পাতার ছবি আপলোড করুন এবং সাথে সাথে রোগ শনাক্ত করুন।','upload':'পাতার ছবি আপলোড করুন','detect':'🔍 পরীক্ষা করুন','preview':'প্রিভিউ','loading':'ছবি বিশ্লেষণ করা হচ্ছে...'},
'हिन्दी':{'title':'पत्ती रोग पहचान','desc':'पत्ती की फोटो अपलोड करें और तुरंत रोग पहचानें।','upload':'पत्ती की फोटो अपलोड करें','detect':'🔍 जांच करें','preview':'पूर्वावलोकन','loading':'छवि का विश्लेषण हो रहा है...'}
}

def tr(text):
    lang_map={'English':'en','বাংলা':'bn','हिन्दी':'hi'}
    target=lang_map[st.session_state.lang]
    if target=='en':
        return str(text)
    try:
        return GoogleTranslator(source='auto', target=target).translate(str(text))
    except:
        return str(text)

t=translations[st.session_state.lang]

st.markdown("""
<style>
.stApp{background:linear-gradient(135deg,#eef7ee,#f7fbff);} 
.stButton button{border-radius:12px;padding:10px 14px;font-weight:700}
.block{background:white;padding:24px;border-radius:22px;box-shadow:0 10px 30px rgba(0,0,0,.08)}
</style>
""", unsafe_allow_html=True)

c1,c2,c3=st.columns(3)
with c1:
    if st.button('English',use_container_width=True): st.session_state.lang='English'; st.rerun()
with c2:
    if st.button('বাংলা',use_container_width=True): st.session_state.lang='বাংলা'; st.rerun()
with c3:
    if st.button('हिन्दी',use_container_width=True): st.session_state.lang='हिन्दी'; st.rerun()

st.markdown(f"<div class='block'><h1>{t['title']}</h1><p>{t['desc']}</p></div>", unsafe_allow_html=True)

api_url='http://leaf-diseases-detect.vercel.app'

left,right=st.columns([1,2])
with left:
    file=st.file_uploader(t['upload'],type=['jpg','jpeg','png'])
    if file:
        st.image(file,caption=t['preview'])

with right:
    if file and st.button(t['detect'],use_container_width=True):
        with st.spinner(t['loading']):
            files={'file':(file.name,file.getvalue(),file.type)}
            r=requests.post(f'{api_url}/disease-detection-file',files=files)
            if r.status_code==200:
                result=r.json()
                st.markdown("<div class='block'>",unsafe_allow_html=True)
                for k,v in result.items():
                    if isinstance(v,list):
                        st.subheader(tr(k))
                        for item in v:
                            st.write('• '+tr(item))
                    else:
                        st.write(f"**{tr(k)}:** {tr(v)}")
                st.markdown("</div>",unsafe_allow_html=True)
            else:
                st.error('API Error')
