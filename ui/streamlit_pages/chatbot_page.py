from services.session_manager import init_chat_state
from ui.handlers.chat_input_handler import handle_agent_input
from ui.components.system_status_display import system_infos
from ui.components.chat_render import render_chat_history, render_chat_controls, render_example_questions
from ui.ui_helpers.headers import create_main_header

def show_chatbot_page():
    """ YA-DA chat sayfasını görüntüler ve kullanıcı etkileşimlerini yönetir """

    create_main_header("YA-DA - Yapay Zeka Destekli Yatırım Danışmanınız", "🤖")

    # Session durumlarını başlatır
    init_chat_state()

    # Sohbet geçmişini gösterir
    render_chat_history()

    # Kullanıcıdan yeni mesaj alır
    handle_agent_input()

    # Sohbet yönetim araçları
    render_chat_controls()

    # Örnek Sorular
    render_example_questions()

    # Sistem bilgilerini getirir
    system_infos()

