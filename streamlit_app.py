import pandas as pd
import requests
import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Canlı Gerçek Veri Maç & Bahis Analizi",
    page_icon="⚽",
    layout="wide",
)


# Ücretsiz ve açık kaynaklı futbol verilerini sunan public API üzerinden gerçek maçları çeken fonksiyon
def fetch_real_football_data(team_name):
  cleaned_name = team_name.strip().lower()

  # Açık futbol veritabanı uç noktası (Public API)
  # Bu servis dünyadaki major liglerin son maçlarını ve skorlarını açık olarak sunar
  url = "https://raw.githubusercontent.com/openfootball/football.json/master/2023-24/en.1.json"

  try:
    response = requests.get(
        "https://raw.githubusercontent.com/openfootball/football.json/master/2025-26/en.1.json",
        timeout=5,
    )
    if response.status_code != 200:
      # Alternatif sezon verisi
      response = requests.get(
          "https://raw.githubusercontent.com/openfootball/football.json/master/2024-25/en.1.json",
          timeout=5,
      )

    data = response.json()
    matches = data.get("matches", [])

    team_matches = []
    for m in matches:
      home = m.get("team1", "").lower()
      away = m.get("team2", "").lower()

      if cleaned_name in home or cleaned_name in away:
        score = m.get("score", {})
        h_ft = score.get("ft", [None, None])[0]
        a_ft = score.get("ft", [None, None])[1]

        is_home = cleaned_name in home
        opponent = m.get("team2") if is_home else m.get("team1")
        scored = h_ft if is_home else a_ft
conced = a_ft if is_home else h_ft

        team_matches.append({
            "Maç Tarihi": m.get("date", "Bilinmiyor"),
            "Rakip": f"vs {opponent}",
            "Yer": "İç Saha" if is_home else "Dış Saha",
            "Atılan Gol": scored if scored is not None else 0,
            "Yenilen Gol": conced if conced is not None else 0,
        })

    # Eğer açık veritabanında maç bulunduysa son 3 maçı döndür
    if team_matches:
      return team_matches[-3:]

  except Exception:
    pass

  return None


# Arayüz
st.title("⚽ Canlı Gerçek Veri Maç & Bahis Analiz Sistemi")
st.markdown(
    "Gerçek takım adlarını girin (Örn: Arsenal, Chelsea, Manchester United"
    " vb.). Sistem açık veritabanından gerçek maç sonuçlarını çeker."
)

with st.form("analysis_form"):
  col1, col2, col3 = st.columns(3)
  with col1:
    sport_type = st.selectbox("Branş Seçin", ["Futbol"])
  with col2:
    team1 = st.text_input("1. Takım Adı", "Arsenal")
  with col3:
    team2 = st.text_input("2. Takım Adı", "Chelsea")

  submitted = st.form_submit_button("Gerçek Verileri Getir ve Analiz Et 🚀")

if submitted:
  if not team1 or not team2:
    st.warning("Lütfen takımları eksiksiz girin.")
  else:
    with st.spinner("Gerçek maç verileri internetten sorgulanıyor..."):
      t1_matches = fetch_real_football_data(team1)
      t2_matches = fetch_real_football_data(team2)

    # Eğer gerçek veritabanında bulunamazsa kullanıcıya net hata ver (Uydurma sonuç göstermez)
    if not t1_matches:
      st.error(
          f"'{team1}' için internet üzerinde güncel resmi maç verisi"
          " bulunamadı! Lütfen İngilizce tam adını yazın (Örn: Arsenal, Liverpool"
          " vb.)."
      )
    elif not t2_matches:
      st.error(
          f"'{team2}' için internet üzerinde güncel resmi maç verisi"
          " bulanamadı! Lütfen İngilizce tam adını yazın."
      )
    else:
      st.success("Gerçek maç verileri başarıyla çekildi!")

      col_a, col_b = st.columns(2)
      with col_a:
        st.subheader(f"🔴 {team1}")
        df1 = pd.DataFrame(t1_matches)
        st.dataframe(df1, use_container_width=True)

      with col_b:
        st.subheader(f"🔵 {team2}")
        df2 = pd.DataFrame(t2_matches)
        st.dataframe(df2, use_container_width=True)

      # Yapay Zeka Analizi ve Bahis Fikirleri
      st.markdown("---")
      st.markdown("### 🎯 Yapay Zeka Maç ve Bahis Tavsiye Raporu")

      t1_avg = sum([x["Atılan Gol"] for x in t1_matches]) / len(t1_matches)
      t2_avg = sum([x["Atılan Gol"] for x in t2_matches]) / len(t2_matches)

      if t1_avg > t2_avg:
        match_winner = (
            f"**{team1}** son maçlardaki gerçek gol yolları etkinliğiyle bir"
            " adım önde."
        )
        best_bet = "Maç Sonu 1 veya Çifte Şans (1X)"
        risk_status = "Orta Riskli"
      elif t2_avg > t1_avg:
        match_winner = (
            f"**{team2}** form grafiği ve rakip fileleri havalandırma"
            " oranlarıyla avantajlı."
        )
        best_bet = "Maç Sonu 2 veya Karşılıklı Gol Var"
        risk_status = "İdeal Risk"
      else:
        match_winner = (
            "İki takımın son karşılaşmalarındaki gol ortalamaları tamamen denk."
        )
        best_bet = "2.5 Gol Üstü / Karşılıklı Gol Var"
        risk_status = "⚠️ Yüksek Riskli Maç"

      st.info(f"🏆 **Analiz Özeti:** {match_winner}")

      r1, r2 = st.columns(2)
      with r1:
        st.metric(label="Önerilen En Mantıklı Tercih", value=best_bet)
      with r2:
        st.metric(label="Maçın Risk Durumu", value=risk_status)
