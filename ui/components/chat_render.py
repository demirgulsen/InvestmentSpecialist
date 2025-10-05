
import uuid
import streamlit as st
from ui.ui_helpers.headers import create_sub_header
from ui.handlers.chat_input_handler import process_user_question

def render_chat_history() -> None:
    """ Sohbet geçmişini kullanıcıya okunabilir ve etkileşimli bir biçimde gösterir. """

    create_sub_header("Sohbet Geçmişi", "💬")

    # Özel yüksekliğe sahip kaydırılabilir sohbet kutusu
    with st.container():
        chat_container = st.container(height=400)

        with chat_container:
            for i, msg in enumerate(st.session_state.messages):
                # Rol bazlı chat message
                with st.chat_message(msg.get("role")):
                    # sohbet içeriği
                    st.write(msg['content'])

                    # Timestamp
                    timestamp = msg.get('timestamp', 'Bilinmiyor')
                    if timestamp:
                        st.caption(f"📅 {timestamp}")


def render_chat_controls() -> None:
    """ Chat yönetim kontrollerini ve istatistiklerini görüntüler.

    Kontroller:
    - Sohbet geçmişini temizleme
    - Mesaj istatistiklerini görüntüleme
    - Yeni oturum başlatma
    """
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        # Sohbet geçmişini temizler
        if st.button("🗑️ Sohbeti Temizle", help="Tüm sohbet geçmişini sil"):
            st.session_state.messages = []
            st.success("✅ Sohbet geçmişi temizlendi!")
            st.rerun()

    with col2:
        # İstatistik bilgilerini görüntüler
        if st.button("📊 İstatistikler", help="Sohbet istatistiklerini göster"):
            msg_count = len(st.session_state.messages)
            user_count = len([m for m in st.session_state.messages if m["role"] == "user"])
            st.info(f"📈 Toplam {msg_count} mesaj ({user_count} soru)")

    with col3:
        # Yeni oturum başlatır - thread ID'yi yeniler
        if st.button("🔄 Yeni Oturum", help="Yeni bir sohbet oturumu başlat"):
            st.session_state.messages = []
            st.session_state.thread_id = str(uuid.uuid4())
            st.success("✅ Yeni oturum başlatıldı!")
            st.rerun()

def render_example_questions() -> None:
    """ Kullanıcıya hızlı başlangıç için örnek sorular sunar. """

    create_sub_header("Örnek Sorular", "🔖")

    # Örnek sorular
    example_questions = [
        "Dolar bugün kaç TL?",
        "Apple hisse fiyatı kaç TL?",
        "Altın hakkında son haberler nedir?",
        "Mevcut Portföy Bilgilerim Neler?",
        "Yatırım Önerilerin Neler?",
        "Amazon hisse bilgileri neler?",
        "Tesla ile Google hisse fiyatları karşılaştırması?"
    ]

    # Dinamik column yapısı - soru sayısına göre ayarlanabilir
    cols = st.columns(len(example_questions))

    for i, (col, question) in enumerate(zip(cols, example_questions)):
        # Kolonları döngüsel olarak kullanır
        with col:
            if st.button(
                    question,
                    key=f"example_{i + 1}",
                    help=f"'{question}' sorusunu sor",
                    type="primary",
                    use_container_width=True
            ):
                process_user_question(question)
