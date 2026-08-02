import random
import pandas as pd
import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="AI Maç İstatistik ve Analiz Asistanı",
    page_icon="⚽",
    layout="wide",
)


# Örnek Veri Üretici (Gerçek projede buraya API veya Web Scraping entegre edilir)
def fetch_team_stats(team_name, sport_type):
  # Simüle edilmiş son 3 maç verisi
  matches = []
  for i in range(1, 4):
    if sport_type == "Futbol":
      match = {
          "Maç": f"Maç {i}",
          "Yer": "İç Saha" if i % 2 != 0 else "Dış Saha",
          "Atılan Gol/Sayı": random.randint(0, 4),
          "Korner": random.randint(3, 9),
          "Toplam Şut": random.randint(10, 22),
          "İsabetli Şut": random.randint(3, 10),
          "Kale Vuruşu (Aut)": random.randint(5, 12),
          "2.5 Alt/Üst": (
              "Üst" if random.random() > 0.4 else "Alt"
          ),  # Futbol için alt/üst
      }
    elif sport_type == "Basketbol":
      match = {
          "Maç": f"Maç {i}",
          "Yer": "İç Saha" if i % 2 != 0 else "Dış Saha",
          "Atılan Gol/Sayı": random.randint(75, 115),
          "Korner": "Yok",  # Basketbolda korner yok
          "Toplam Şut": random.randint(60, 90),  # Şut yerine şut atma girişimi
          "İsabetli Şut": random.randint(25, 45),
          "Kale Vuruşu (Aut)": "Yok",
          "2.5 Alt/Üst": (
              "175.5 Üst" if random.random() > 0.4 else "160.5 Alt"
          ),
      }
    else:  # Buz Hokeyi
      match = {
          "Maç": f"Maç {i}",
          "Yer": "İç Saha" if i % 2 != 0 else "Dış Saha",
          "Atılan Gol/Sayı": random.randint(1, 6),
          "Korner": "Yok",
          "Toplam Şut": random.randint(25, 45),
          "İsabetli Şut": random.randint(10, 22),
          "Kale Vuruşu (Aut)": "Yok",
          "5.5 Alt/Üst": "Üst" if random.random() > 0.4 else "Alt",
      }
    matches.append(match)
  return matches


# Arayüz Tasarımı
st.title("🤖 Otomatik Maç ve İstatistik Analiz Sistemi")
st.markdown(
    "İki takım adı girin, sistem internet tabanlı verileri tarayarak son 3"
    " maçın detaylı dökümünü çıkarsın."
)

with st.form("analysis_form"):
  col1, col2, col3 = st.columns(3)

  with col1:
    sport_type = st.selectbox(
        "Branş Seçin", ["Futbol", "Basketbol", "Buz Hokeyi"]
    )
  with col2:
    team1 = st.text_input("1. Takım Adı", "Galatasaray")
  with col3:
    team2 = st.text_input("2. Takım Adı", "Fenerbahçe")

  submitted = st.form_submit_button("Analizi Başlat 🚀")

if submitted:
  if not team1 or not team2:
    st.warning("Lütfen her iki takım adını da eksiksiz girin.")
  else:
    with st.spinner(
        f"{team1} ve {team2} için internet verileri taranıyor ve son 3 maç"
        " analiz ediliyor..."
    ):
      # Verileri simüle et / çek
      t1_data = fetch_team_stats(team1, sport_type)
      t2_data = fetch_team_stats(team2, sport_type)

    st.success("Analiz tamamlandı!")

    # Sonuçları Göster
    col_a, col_b = st.columns(2)

    with col_a:
      st.subheader(f"🔴 {team1} (Son 3 Maç İstatistikleri)")
      df1 = pd.DataFrame(t1_data)
      st.dataframe(df1, use_container_width=True)

      # Özet Metrikler
      if sport_type == "Futbol":
        avg_goals = sum([x["Atılan Gol/Sayı"] for x in t1_data]) / 3
        avg_corners = sum([x["Korner"] for x in t1_data]) / 3
        st.info(
            f"**Ortalamalar:** Maç Başı Gol: {avg_goals:.2f} | Maç Başı Korner:"
            f" {avg_corners:.2f}"
        )

    with col_b:
      st.subheader(f"🔵 {team2} (Son 3 Maç İstatistikleri)")
      df2 = pd.DataFrame(t2_data)
      st.dataframe(df2, use_container_width=True)

      # Özet Metrikler
      if sport_type == "Futbol":
        avg_goals_2 = sum([x["Atılan Gol/Sayı"] for x in t2_data]) / 3
        avg_corners_2 = sum([x["Korner"] for x in t2_data]) / 3
        st.info(
            f"**Ortalamalar:** Maç Başı Gol: {avg_goals_2:.2f} | Maç Başı"
            f" Korner: {avg_corners_2:.2f}"
        )

    st.markdown("---")
    st.markdown("### 📊 Yapay Zeka Karşılaştırma Özeti")
    st.write(
        f"Yapılan son 3 maçlık otomatik tarama sonucuna göre; **{team1}** ve"
        f" **{team2**} takımlarının hücum hattı performansları incelendi."
        " Özellikle iç/dış saha form durumları göz önüne alındığında maçın"
        " çekişmeli geçmesi bekleniyor."
    )
