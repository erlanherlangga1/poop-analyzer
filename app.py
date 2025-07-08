import streamlit as st
from openai import OpenAI
import base64

# Inisialisasi client OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# UI
st.title("Analisis Feses Bayi dengan AI")
st.write("Upload gambar feses bayi untuk mengetahui kemungkinan kondisi, indikasi, dan saran penanganan.")

uploaded_file = st.file_uploader("Upload gambar feses bayi", type=["jpg", "jpeg", "png"], key="gambar_feses")

if uploaded_file:
    st.image(uploaded_file, caption="Gambar Feses Bayi", use_container_width=True)

    # Konversi gambar ke base64
    image_bytes = uploaded_file.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    # Prompt
    prompt = (
        "Analisis gambar feses bayi berikut ini:\n"
        "- Identifikasi warna, tekstur, dan bentuk feses secara umum.\n"
        "- Apakah terdapat lendir atau darah.\n"
        "- Tentukan skala Bristol dari 1 sampai 7 berdasarkan bentuk feses (jika memungkinkan).\n"
        "- Apakah tampilan ini normal untuk bayi secara umum.\n"
        "- Apakah mengarah pada sembelit, diare, infeksi, intoleransi laktosa, alergi susu sapi, atau gangguan pencernaan lainnya\n"
        "- Jelaskan indikasi medis yang mungkin terjadi.\n"
        "- Apakah ini kondisi yang normal dan tidak perlu dikhawatirkan\n"
        "- Apakah perlu diamati selama beberapa hari\n"
        "- Apakah ini termasuk kondisi yang harus segera dibawa ke dokter\n"
        "- Berikan saran atau penanganan awal untuk orang tua.\n"
        "- Misalnya menjaga hidrasi, menyesuaikan pola makan, mencatat kondisi selama beberapa hari\n"
        "- Kapan waktu yang tepat untuk membawa bayi ke dokter\n"
        "Gunakan bahasa Indonesia yang jelas, mudah dipahami oleh orang tua, tidak menggunakan istilah medis yang rumit. Jika kondisi tidak berbahaya, berikan penjelasan yang menenangkan."
    )


    with st.spinner("⏳ Sedang menganalisis gambar, mohon tunggu..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]}
                ],
                max_tokens=1000,
            )
            st.success("✅ Analisis selesai!")
            st.subheader("🧠 Hasil Analisis:")
            st.write(response.choices[0].message.content)

        except Exception as e:
            st.error(f"Terjadi kesalahan saat menganalisis: {str(e)}")
