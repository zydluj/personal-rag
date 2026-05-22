"""DocMind Demo — standalone demo with pre-built answers. No API keys needed."""

import json
from flask import Flask, request, Response

app = Flask(__name__)

# ──────────────────────────────────────────────
# Demo knowledge base — pre-built Q&A
# ──────────────────────────────────────────────

DEMO_QA = {
    "метрик": {
        "answer": (
            "По данным отчёта за Q2 2025, основные метрики email-кампаний:\n\n"
            "**Общие показатели:**\n"
            "• Всего отправлено писем: 45,000\n"
            "• Open rate (средний): 28.5%\n"
            "• Click rate (средний): 4.2%\n"
            "• Unsubscribe rate: 0.3%\n"
            "• Конверсия в демо: 2.1%\n\n"
            "**Лучшая кампания** — «Безопасность данных 2025»:\n"
            "• Open rate: 32%, Click rate: 5.8%, 87 конверсий в демо\n\n"
            "**Вывод:** кампании про безопасность работают лучше всего. "
            "Таргетированные кампании дают высокий CTR."
        ),
        "sources": [
            {"filename": "email_campaign_q2.txt", "relevance": "95%",
             "section": "Общие метрики, раздел по кампаниям"},
            {"filename": "strategy_notes.md", "relevance": "62%",
             "section": "Решения по каналам"},
        ],
    },
    "конкурент": {
        "answer": (
            "На основе документов, вот что известно о конкурентах:\n\n"
            "**Конкурент Y (DataShield Pro):**\n"
            "• Позиционирование: скорость обработки данных\n"
            "• Слабые стороны: нет ISO 27001, слабая поддержка\n"
            "• Цена: $500/мес базовый, $2000/мес enterprise\n"
            "• Клиенты жалуются на медленную работу и плохой onboarding\n"
            "• Доля рынка: ~20% в среднем бизнесе\n\n"
            "**Конкурент Z (SecureFlow):**\n"
            "• Позиционирование: «всё в одном»\n"
            "• Слабые стороны: сложный интерфейс, интеграция 8-12 недель\n"
            "• Цена: $800/мес базовый, $3500/мес enterprise\n\n"
            "**Наше преимущество:** безопасность (ISO 27001, 152-ФЗ), "
            "быстрая интеграция (2-4 недели), цена ниже ($400/$1500)."
        ),
        "sources": [
            {"filename": "competitor_analysis.txt", "relevance": "98%",
             "section": "Конкурент Y, Конкурент Z, Наши преимущества"},
            {"filename": "meeting_transcript.txt", "relevance": "71%",
             "section": "Упоминание проблем клиента с конкурентом Y"},
            {"filename": "strategy_notes.md", "relevance": "65%",
             "section": "Позиционирование — дифференциация от конкурента Y"},
        ],
    },
    "альфа": {
        "answer": (
            "Встреча с Альфа-Банком состоялась 15 марта 2025.\n\n"
            "**Участники:** Анна (менеджер), Дмитрий (техлид клиента), "
            "Марина (маркетинг)\n\n"
            "**Ключевые моменты:**\n"
            "• Главное требование клиента — соответствие 152-ФЗ ✅\n"
            "• Сроки интеграции: 2-4 недели для банковского сектора\n"
            "• У клиента был негативный опыт с конкурентом Y — медленная работа\n"
            "• Наша производительность: до 10 млн записей/сек\n"
            "• SLA: 99.9%, ответ на критические инциденты в течение 1 часа\n\n"
            "**Итоги:** запланировано техническое демо на 22 марта. "
            "Дмитрий пришлёт тестовые данные."
        ),
        "sources": [
            {"filename": "meeting_transcript.txt", "relevance": "99%",
             "section": "Полный транскрипт встречи"},
            {"filename": "competitor_analysis.txt", "relevance": "45%",
             "section": "Сравнение с конкурентом Y"},
        ],
    },
    "бюджет": {
        "answer": (
            "Бюджет на запуск SecureVault v3.0 составляет **$10,000**.\n\n"
            "**Разбивка:**\n"
            "• Вебинар «Что нового в v3.0»: $2,000\n"
            "• PR-агентство (пресс-релиз): $5,000\n"
            "• Контент — кейсы и посты: $3,000\n\n"
            "**Каналы запуска:**\n"
            "• Email-рассылка (сегментированная)\n"
            "• Вебинар — 28 августа\n"
            "• Пресс-релиз\n"
            "• Кейс-стади с бета-клиентом (Сбербанк)\n"
            "• LinkedIn — серия из 5 постов\n\n"
            "**Дата запуска:** 1 сентября 2025"
        ),
        "sources": [
            {"filename": "product_brief.txt", "relevance": "97%",
             "section": "Бюджет, Каналы запуска"},
        ],
    },
    "позиционирован": {
        "answer": (
            "Команда выбрала позиционирование через **безопасность (safety)**, "
            "а не через скорость (speed).\n\n"
            "**Аргументы за это решение:**\n"
            "1. Клиенты из банковского сектора ставят безопасность на первое место\n"
            "2. Конкурент Y уже занял нишу «скорость» — мы дифференцируемся\n"
            "3. Наш продукт объективно сильнее в безопасности (ISO 27001)\n\n"
            "**Подтверждение в практике:**\n"
            "• Кампания «Безопасность данных 2025» показала лучший engagement\n"
            "• Главный слоган v3.0: «Безопасность без компромиссов»\n"
            "• На встрече с Альфа-Банком безопасность и 152-ФЗ были главным требованием"
        ),
        "sources": [
            {"filename": "strategy_notes.md", "relevance": "99%",
             "section": "Позиционирование"},
            {"filename": "email_campaign_q2.txt", "relevance": "58%",
             "section": "Кампания «Безопасность данных»"},
            {"filename": "product_brief.txt", "relevance": "52%",
             "section": "Ключевые сообщения"},
        ],
    },
    "kpi": {
        "answer": (
            "**KPI на Q1 2025** (установлены на стратегической сессии):\n\n"
            "• Конверсия лидов: целевая **15%**\n"
            "• CAC (стоимость привлечения клиента): не более **$300**\n"
            "• NPS: целевой **45+**\n"
            "• Количество демо: **50 в месяц**\n\n"
            "**Фактические результаты Q2 2025 (email-канал):**\n"
            "• Конверсия email → демо: 2.1%\n"
            "• Лучший результат: кампания «Миграция с конкурента Y» — 52 демо\n\n"
            "**Решения по каналам:**\n"
            "• Email-маркетинг — основной канал лидогенерации\n"
            "• Холодные звонки отменены (конверсия всего 2%)\n"
            "• Запуск блога с кейсами клиентов"
        ),
        "sources": [
            {"filename": "strategy_notes.md", "relevance": "96%",
             "section": "KPI на Q1 2025"},
            {"filename": "email_campaign_q2.txt", "relevance": "72%",
             "section": "Общие метрики"},
        ],
    },
    "securevault": {
        "answer": (
            "**SecureVault v3.0** — запуск запланирован на **1 сентября 2025**.\n\n"
            "**Новые возможности:**\n"
            "• Шифрование end-to-end для всех типов данных\n"
            "• Новый дашборд аналитики безопасности\n"
            "• API v3 с поддержкой GraphQL\n"
            "• Мультирегиональное хранение данных (EU, US, Asia)\n\n"
            "**Целевая аудитория:**\n"
            "• Enterprise в финансовом секторе\n"
            "• Компании с требованиями GDPR и 152-ФЗ\n"
            "• Текущие клиенты v2.x (автоматический мигратор)\n\n"
            "**Ключевое сообщение:** «Безопасность без компромиссов»"
        ),
        "sources": [
            {"filename": "product_brief.txt", "relevance": "99%",
             "section": "Что нового в v3.0, Целевая аудитория"},
        ],
    },
}

ALIASES = {
    "email": "метрик", "кампани": "метрик", "open rate": "метрик",
    "рассылк": "метрик", "письм": "метрик",
    "datashield": "конкурент", "secureflow": "конкурент", "соперник": "конкурент",
    "банк": "альфа", "встреч": "альфа", "дмитрий": "альфа", "клиент": "альфа",
    "деньг": "бюджет", "стоим": "бюджет", "запуск": "бюджет", "расход": "бюджет",
    "safety": "позиционирован", "безопасност": "позиционирован",
    "почему": "позиционирован", "стратеги": "позиционирован",
    "v3": "securevault", "версия": "securevault", "новинк": "securevault",
    "продукт": "securevault", "релиз": "securevault",
    "показател": "kpi", "цел": "kpi", "конверси": "kpi", "метрик": "метрик",
}

NO_ANSWER = {
    "answer": (
        "Я не нашёл информации по этому вопросу в загруженных документах.\n\n"
        "Попробуйте спросить о:\n"
        "• Метриках email-кампаний\n"
        "• Конкурентах (DataShield Pro, SecureFlow)\n"
        "• Встрече с Альфа-Банком\n"
        "• Бюджете на запуск v3.0\n"
        "• Позиционировании продукта\n"
        "• KPI и целях\n"
        "• SecureVault v3.0"
    ),
    "sources": [],
}


def find_answer(question):
    q = question.lower()
    for key in DEMO_QA:
        if key in q:
            return DEMO_QA[key]
    for alias, key in ALIASES.items():
        if alias in q:
            return DEMO_QA[key]
    return NO_ANSWER


# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────

@app.after_request
def headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.route("/")
def index():
    return Response(PAGE_HTML, content_type="text/html; charset=utf-8")


@app.route("/ask")
def ask():
    question = request.args.get("q", "").strip()
    if not question:
        return _json({"answer": "Введите вопрос.", "sources": []})
    return _json(find_answer(question))


def _json(data):
    return Response(
        json.dumps(data, ensure_ascii=False),
        content_type="application/json; charset=utf-8",
    )


# ──────────────────────────────────────────────
# HTML — single page app
# ──────────────────────────────────────────────

PAGE_HTML = r"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<title>DocMind — AI-поиск по документам</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter',-apple-system,sans-serif;background:#0a0a0f;color:#e0e0e0;min-height:100vh}

/* ── NAV ── */
.nav{display:flex;align-items:center;justify-content:space-between;padding:16px 32px;border-bottom:1px solid #1e1e30;background:#0d0d14}
.nav-logo{display:flex;align-items:center;gap:10px;font-size:18px;font-weight:700;color:#fff;text-decoration:none}
.nav-icon{width:32px;height:32px;background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px;color:#fff}
.nav-links{display:flex;gap:24px}
.nav-links a{color:#9ca3af;font-size:13px;text-decoration:none;transition:color .2s}
.nav-links a:hover{color:#fff}
.nav-badge{background:#1e1b4b;color:#a5b4fc;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600}

/* ── HERO ── */
.hero{padding:64px 32px 56px;text-align:center;position:relative;overflow:hidden;
  background:linear-gradient(135deg,#0f1029 0%,#1a0a2e 50%,#0a1628 100%);border-bottom:1px solid #1e1e3a}
.hero::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;
  background:radial-gradient(circle at 30% 50%,rgba(99,102,241,.08) 0%,transparent 50%),
  radial-gradient(circle at 70% 50%,rgba(139,92,246,.06) 0%,transparent 50%);animation:shimmer 8s ease-in-out infinite alternate}
@keyframes shimmer{0%{transform:translate(0,0)}100%{transform:translate(-5%,3%)}}
.hero-content{position:relative;z-index:1;max-width:680px;margin:0 auto}
.hero h1{font-size:40px;font-weight:700;color:#fff;margin-bottom:16px;line-height:1.2}
.hero h1 span{background:linear-gradient(135deg,#818cf8,#c084fc);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero-sub{font-size:17px;color:#9ca3af;line-height:1.7;margin-bottom:28px}
.hero-features{display:flex;gap:20px;justify-content:center;flex-wrap:wrap}
.feat{display:flex;align-items:center;gap:8px;font-size:13px;color:#a5b4fc;background:#111128;border:1px solid #1e1e3a;padding:8px 16px;border-radius:20px}
.feat-dot{width:6px;height:6px;border-radius:50%;background:#6366f1}

/* ── STATS ── */
.stats{display:flex;justify-content:center;gap:48px;padding:24px 32px;border-bottom:1px solid #1e1e30;background:#0d0d14}
.stat{text-align:center}
.stat-num{font-size:24px;font-weight:700;color:#fff}
.stat-label{font-size:12px;color:#6b7280;margin-top:2px}

/* ── CHAT ── */
.chat-container{max-width:800px;margin:0 auto;padding:0 24px;display:flex;flex-direction:column;min-height:60vh}
.chat-area{flex:1;padding:24px 0;overflow-y:auto}
.message{margin-bottom:20px;animation:fadeUp .4s ease}
@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
.message.user{display:flex;justify-content:flex-end}
.bubble-user{background:linear-gradient(135deg,#4f46e5,#6366f1);color:#fff;border-radius:18px 18px 4px 18px;padding:12px 18px;max-width:75%;font-size:15px;line-height:1.5}
.bot-card{background:#111118;border:1px solid #1e1e30;border-radius:16px;padding:20px 24px}
.bot-card .answer{font-size:14px;line-height:1.7;white-space:pre-wrap}
.bot-card .answer strong,.bot-card .answer b{color:#c4b5fd}
.sources-block{margin-top:16px;border-top:1px solid #1e1e30;padding-top:12px}
.sources-label{font-size:11px;color:#6b7280;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px}
.src{display:flex;align-items:center;gap:10px;padding:8px 12px;background:#0d0d1a;border:1px solid #1a1a2e;border-radius:8px;margin-bottom:4px;font-size:12px}
.src-icon{color:#6366f1;font-size:14px;flex-shrink:0}
.src-name{color:#a5b4fc;font-weight:600}
.src-section{color:#6b7280;margin-left:4px}
.src-rel{margin-left:auto;background:#1e1b4b;color:#a5b4fc;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600;flex-shrink:0}

/* ── INPUT ── */
.input-area{padding:16px 0 32px;position:sticky;bottom:0;background:linear-gradient(transparent,#0a0a0f 20%)}
.input-wrap{display:flex;gap:10px;background:#111118;border:1px solid #1e1e30;border-radius:14px;padding:6px 6px 6px 18px;align-items:center;transition:border-color .2s}
.input-wrap:focus-within{border-color:#4f46e5}
.input-wrap input{flex:1;background:none;border:none;color:#fff;font-size:15px;outline:none;font-family:inherit}
.input-wrap input::placeholder{color:#4b5563}
.send-btn{background:linear-gradient(135deg,#4f46e5,#6366f1);color:#fff;border:none;border-radius:10px;padding:10px 20px;font-size:14px;font-weight:600;cursor:pointer;transition:opacity .2s;font-family:inherit}
.send-btn:hover{opacity:.9}
.send-btn:disabled{opacity:.4;cursor:not-allowed}

/* ── EXAMPLES ── */
.empty-state{text-align:center;padding:40px 0 20px}
.empty-state h2{font-size:16px;color:#9ca3af;font-weight:500;margin-bottom:20px}
.examples{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
.ex-btn{padding:10px 16px;background:#111118;border:1px solid #1e1e30;border-radius:12px;color:#9ca3af;font-size:13px;cursor:pointer;transition:all .2s;font-family:inherit}
.ex-btn:hover{border-color:#4f46e5;color:#e0e0e0;background:#15152a}

/* ── LOADING ── */
.typing{display:flex;gap:4px;padding:8px 0}
.typing span{width:8px;height:8px;background:#4f46e5;border-radius:50%;animation:bounce 1.4s ease-in-out infinite}
.typing span:nth-child(2){animation-delay:.2s}
.typing span:nth-child(3){animation-delay:.4s}
@keyframes bounce{0%,80%,100%{transform:scale(.6);opacity:.4}40%{transform:scale(1);opacity:1}}

/* ── HOW IT WORKS ── */
.section{max-width:800px;margin:0 auto;padding:48px 24px}
.section-title{font-size:22px;font-weight:700;color:#fff;text-align:center;margin-bottom:8px}
.section-sub{font-size:14px;color:#6b7280;text-align:center;margin-bottom:36px}
.steps{display:flex;gap:16px;flex-wrap:wrap;justify-content:center}
.step{flex:1;min-width:170px;max-width:200px;background:#111118;border:1px solid #1e1e30;border-radius:14px;padding:24px 16px;text-align:center}
.step-icon{font-size:28px;margin-bottom:12px}
.step h3{font-size:14px;color:#e0e0e0;margin-bottom:6px}
.step p{font-size:12px;color:#6b7280;line-height:1.5}

/* ── USE CASES ── */
.usecases{display:flex;gap:16px;flex-wrap:wrap;justify-content:center;margin-top:36px}
.usecase{background:#111118;border:1px solid #1e1e30;border-radius:14px;padding:20px;flex:1;min-width:220px;max-width:260px}
.usecase-icon{font-size:24px;margin-bottom:8px}
.usecase h3{font-size:14px;color:#e0e0e0;margin-bottom:6px}
.usecase p{font-size:12px;color:#6b7280;line-height:1.5}

/* ── FOOTER ── */
.footer{text-align:center;padding:32px;border-top:1px solid #1e1e30;color:#4b5563;font-size:12px}
.footer a{color:#6366f1;text-decoration:none}
</style>
</head>
<body>

<!-- NAV -->
<nav class="nav">
  <a href="#" class="nav-logo"><div class="nav-icon">D</div>DocMind</a>
  <div class="nav-links">
    <a href="#demo">Демо</a>
    <a href="#how">Как работает</a>
    <a href="#usecases">Кейсы</a>
    <span class="nav-badge">Beta</span>
  </div>
</nav>

<!-- HERO -->
<div class="hero">
  <div class="hero-content">
    <h1>Задайте вопрос —<br>получите <span>точный ответ</span></h1>
    <p class="hero-sub">
      DocMind — AI-ассистент, который ищет ответы в ваших корпоративных документах.
      Загрузите файлы, спросите на естественном языке — получите ответ с указанием источника и страницы.
    </p>
    <div class="hero-features">
      <div class="feat"><div class="feat-dot"></div>PDF, DOCX, TXT, MD</div>
      <div class="feat"><div class="feat-dot"></div>Семантический поиск</div>
      <div class="feat"><div class="feat-dot"></div>Источники в ответе</div>
      <div class="feat"><div class="feat-dot"></div>100% локально</div>
    </div>
  </div>
</div>

<!-- STATS -->
<div class="stats">
  <div class="stat"><div class="stat-num">5</div><div class="stat-label">документов загружено</div></div>
  <div class="stat"><div class="stat-num">28</div><div class="stat-label">фрагментов в базе</div></div>
  <div class="stat"><div class="stat-num">&lt;2с</div><div class="stat-label">время ответа</div></div>
  <div class="stat"><div class="stat-num">0</div><div class="stat-label">данных на сервер</div></div>
</div>

<!-- DEMO CHAT -->
<div id="demo" class="chat-container">
  <div class="chat-area" id="chat">
    <div class="empty-state" id="empty">
      <h2>Попробуйте — задайте вопрос по загруженным документам</h2>
      <div class="examples">
        <button class="ex-btn" onclick="askEx(this)">Какие метрики по email-кампаниям в Q2?</button>
        <button class="ex-btn" onclick="askEx(this)">Что мы знаем про конкурента Y?</button>
        <button class="ex-btn" onclick="askEx(this)">Что обсуждали на встрече с Альфа-Банком?</button>
        <button class="ex-btn" onclick="askEx(this)">Какой бюджет на запуск v3.0?</button>
        <button class="ex-btn" onclick="askEx(this)">Почему выбрали безопасность?</button>
        <button class="ex-btn" onclick="askEx(this)">Какие KPI на квартал?</button>
      </div>
    </div>
  </div>
  <div class="input-area">
    <div class="input-wrap">
      <input type="text" id="q" placeholder="Задайте вопрос по документам..." autofocus
             onkeydown="if(event.key==='Enter')ask()">
      <button class="send-btn" id="btn" onclick="ask()">Отправить</button>
    </div>
  </div>
</div>

<!-- HOW IT WORKS -->
<div id="how" class="section" style="border-top:1px solid #1e1e30">
  <div class="section-title">Как это работает</div>
  <div class="section-sub">Четыре шага от документа до ответа</div>
  <div class="steps">
    <div class="step"><div class="step-icon">📄</div><h3>Загрузка</h3><p>Загрузите документы любого формата — PDF, Word, текст, Markdown</p></div>
    <div class="step"><div class="step-icon">🧠</div><h3>Индексация</h3><p>AI разбивает текст на фрагменты и создаёт векторные представления смысла</p></div>
    <div class="step"><div class="step-icon">🔍</div><h3>Поиск</h3><p>При вопросе система находит самые релевантные фрагменты по смыслу, а не по словам</p></div>
    <div class="step"><div class="step-icon">💬</div><h3>Ответ</h3><p>AI формирует понятный ответ и указывает точные источники</p></div>
  </div>
</div>

<!-- USE CASES -->
<div id="usecases" class="section">
  <div class="section-title">Для кого это</div>
  <div class="section-sub">DocMind решает задачи команд, которые работают с большим объёмом документов</div>
  <div class="usecases">
    <div class="usecase"><div class="usecase-icon">📊</div><h3>Маркетинг</h3><p>Быстро найти метрики прошлых кампаний, результаты A/B тестов, конкурентный анализ</p></div>
    <div class="usecase"><div class="usecase-icon">💼</div><h3>Продажи</h3><p>Поднять историю переговоров с клиентом, найти условия сделки, подготовиться к звонку</p></div>
    <div class="usecase"><div class="usecase-icon">⚖️</div><h3>Юристы</h3><p>Поиск по договорам, регламентам и политикам — ответ с номером пункта и страницы</p></div>
    <div class="usecase"><div class="usecase-icon">🏗️</div><h3>Управление</h3><p>Протоколы встреч, стратегические решения, KPI — всё в одном месте с мгновенным доступом</p></div>
  </div>
</div>

<!-- FOOTER -->
<div class="footer">
  DocMind &copy; 2025 — AI-поиск по корпоративным документам
</div>

<script>
var BASE = window.location.href.replace(/\/+$/,'');

function esc(t){var d=document.createElement('div');d.textContent=t;return d.innerHTML}
function fmt(t){return t.replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>').replace(/\n/g,'<br>')}

function askEx(btn){document.getElementById('q').value=btn.textContent;ask()}

function ask(){
  var input=document.getElementById('q'),btn=document.getElementById('btn');
  var q=input.value.trim();if(!q)return;

  var el=document.getElementById('empty');if(el)el.remove();
  var chat=document.getElementById('chat');

  var u=document.createElement('div');u.className='message user';
  u.innerHTML='<div class="bubble-user">'+esc(q)+'</div>';chat.appendChild(u);

  var ld=document.createElement('div');ld.className='message';
  ld.innerHTML='<div class="bot-card"><div class="typing"><span></span><span></span><span></span></div></div>';
  chat.appendChild(ld);chat.scrollTop=chat.scrollHeight;

  input.value='';btn.disabled=true;

  // Fake delay for realism
  setTimeout(function(){
    var xhr=new XMLHttpRequest();
    xhr.open('GET',BASE+'/ask?q='+encodeURIComponent(q),true);
    xhr.onreadystatechange=function(){
      if(xhr.readyState!==4)return;
      btn.disabled=false;input.focus();
      if(xhr.status===200){
        try{
          var data=JSON.parse(xhr.responseText);
          var html='<div class="bot-card"><div class="answer">'+fmt(data.answer)+'</div>';
          if(data.sources&&data.sources.length>0){
            html+='<div class="sources-block"><div class="sources-label">Источники</div>';
            for(var i=0;i<data.sources.length;i++){
              var s=data.sources[i];
              html+='<div class="src"><span class="src-icon">&#128196;</span>'
                +'<span class="src-name">'+esc(s.filename)+'</span>'
                +'<span class="src-section">'+esc(s.section||'')+'</span>'
                +'<span class="src-rel">'+esc(s.relevance)+'</span></div>';
            }
            html+='</div>';
          }
          html+='</div>';ld.innerHTML=html;
        }catch(e){ld.innerHTML='<div class="bot-card"><div class="answer" style="color:#f87171;">'+esc(xhr.responseText.substring(0,300))+'</div></div>'}
      }else{ld.innerHTML='<div class="bot-card"><div class="answer" style="color:#f87171;">HTTP '+xhr.status+'</div></div>'}
      chat.scrollTop=chat.scrollHeight;
    };
    xhr.send();
  }, 800 + Math.random()*700);
}
</script>
</body>
</html>"""


if __name__ == "__main__":
    print("DocMind Demo running: http://localhost:5001")
    app.run(host="0.0.0.0", port=5001)
