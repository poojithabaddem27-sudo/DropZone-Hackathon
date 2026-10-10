import streamlit as st
from datetime import datetime, timedelta
import uuid

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="DropZone | Local Community",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #0b1020;
    --panel: #131b30;
    --border: #26334f;
    --text: #edf2ff;
    --muted: #9ba9c7;
    --blue: #6485ff;
    --purple: #a78bfa;
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, #18254b 0%, transparent 40%),
        var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #0e1528;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * {
    color: var(--text);
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: var(--text) !important;
    letter-spacing: -0.6px;
}

p, label, .stCaption {
    color: var(--muted);
}

.hero {
    padding: 30px;
    border: 1px solid #34466c;
    border-radius: 24px;
    background: linear-gradient(120deg, #19294b, #28204b 75%, #171b37);
    margin-bottom: 24px;
}

.eyebrow {
    color: #aabaff;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hero h1 {
    font-size: clamp(32px, 4vw, 48px);
    font-weight: 800;
    margin: 10px 0;
    line-height: 1.15;
}

.hero p {
    font-size: 15px;
    line-height: 1.7;
    max-width: 680px;
    margin-bottom: 0;
}

.pill {
    display: inline-block;
    background: #24365f;
    color: #c8d4ff;
    border: 1px solid #42588c;
    border-radius: 30px;
    padding: 7px 12px;
    margin-top: 18px;
    margin-right: 7px;
    font-size: 12px;
    font-weight: 600;
}

.section-label {
    font-size: 12px;
    color: #91a7ff;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 800;
    margin-bottom: 6px;
}

.metric-card {
    background: linear-gradient(145deg, #17233c, #11192b);
    border: 1px solid var(--border);
    border-radius: 17px;
    padding: 18px;
    min-height: 115px;
}

.metric-label {
    color: #aab7d2;
    font-size: 12px;
    font-weight: 600;
}

.metric-number {
    font-size: 28px;
    font-weight: 800;
    color: #ffffff;
    margin-top: 9px;
}

.post-card {
    background: linear-gradient(145deg, #151f35, #11192b);
    border: 1px solid #2b3957;
    border-radius: 18px;
    padding: 20px;
    margin: 12px 0;
}

.post-category {
    color: #b6c4ff;
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.post-message {
    color: #f1f4ff;
    font-size: 15px;
    line-height: 1.7;
    margin: 12px 0;
    overflow-wrap: anywhere;
}

.post-meta {
    color: #94a3c4;
    font-size: 12px;
}

div.stButton > button {
    border-radius: 11px;
    border: 1px solid #394b75;
    background: #1b2945;
    color: #eef2ff;
    font-weight: 600;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    border-color: #8196ff;
    background: #283b63;
    color: white;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(100deg, #5478ff, #8964f6);
    border: none;
    color: white;
}

div.stButton > button[kind="primary"]:hover {
    filter: brightness(1.12);
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] {
    background: #111a2d;
    border-color: #354361;
    border-radius: 10px;
}

div[data-baseweb="select"] *,
div[data-baseweb="input"] *,
div[data-baseweb="textarea"] * {
    color: #edf2ff;
}

div[data-testid="stForm"] {
    background: #131c30;
    border: 1px solid #2b3957;
    border-radius: 18px;
    padding: 22px;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

hr {
    border-color: #283550;
}

.footer {
    text-align: center;
    color: #7888a9;
    font-size: 12px;
    padding: 25px 0 5px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SESSION DATA ----------------
if "posts" not in st.session_state:
    st.session_state.posts = []

if "reports" not in st.session_state:
    st.session_state.reports = []

if "reported_ids" not in st.session_state:
    st.session_state.reported_ids = set()

if "zone" not in st.session_state:
    st.session_state.zone = "Campus"

ZONES = ["Campus", "Library", "Cafeteria", "Hackathon"]

CATEGORIES = {
    "Lost & Found": "🔎",
    "Study Group": "📚",
    "Event Q&A": "🎪"
}


# ---------------- HELPER FUNCTIONS ----------------
def active_posts():
    now = datetime.now()
    return [
        post for post in st.session_state.posts
        if post["expires"] > now
    ]


def format_time(value):
    return value.strftime("%I:%M %p")


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown(
        "<div style='font-size:32px;font-weight:800;'>"
        "📍 DropZone</div>",
        unsafe_allow_html=True
    )
    st.caption("LOCAL COMMUNITY NETWORK")
    st.divider()

    st.markdown("### 🗺️ Your test zone")

    selected_zone = st.selectbox(
        "Choose a location",
        ZONES,
        index=ZONES.index(st.session_state.zone),
        key="zone_selector",
        label_visibility="collapsed"
    )
    st.session_state.zone = selected_zone

    st.markdown("### ✨ Explore")
    st.markdown("📢 Community feed")
    st.markdown("🔎 Lost & Found")
    st.markdown("📚 Study groups")
    st.markdown("🎪 Event questions")

    st.divider()
    st.markdown("### 🛡️ Privacy first")
    st.caption(
        "This prototype uses manually selected test zones. "
        "It does not track your GPS location."
    )

    st.markdown("### ⏳ Temporary by design")
    st.caption(
        "Posts leave the active feed after their expiry time."
    )

    st.divider()
    st.caption("SAMARTHA HACKATHON • DROPZONE")


# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <div class="eyebrow">YOUR PLACE. YOUR PEOPLE.</div>
    <h1>Good things happen<br>when communities connect.</h1>
    <p>
        A local space to find lost items, connect with classmates
        and get answers about nearby activities — without a
        permanent follower network.
    </p>
    <span class="pill">📍 Zone-based</span>
    <span class="pill">⏳ Time-limited posts</span>
    <span class="pill">🛡️ Privacy-conscious</span>
</div>
""", unsafe_allow_html=True)


# ---------------- METRICS ----------------
posts = active_posts()
zone_posts = [
    post for post in posts
    if post["zone"] == selected_zone
]

lost_count = sum(
    post["category"] == "Lost & Found"
    for post in zone_posts
)

study_count = sum(
    post["category"] == "Study Group"
    for post in zone_posts
)

m1, m2, m3, m4 = st.columns(4)

metrics = [
    (m1, "ACTIVE POSTS", len(zone_posts), "📢"),
    (m2, "LOST & FOUND", lost_count, "🔎"),
    (m3, "STUDY GROUPS", study_count, "📚"),
    (m4, "YOUR ZONE", selected_zone, "📍")
]

for column, label, value, emoji in metrics:
    with column:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{emoji} {label}</div>
                <div class="metric-number">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.write("")


# ---------------- MAIN LAYOUT ----------------
feed_col, create_col = st.columns(
    [1.55, 1],
    gap="large"
)

# ---------------- COMMUNITY FEED ----------------
with feed_col:
    st.markdown(
        '<div class="section-label">THE NEIGHBOURHOOD</div>',
        unsafe_allow_html=True
    )
    st.header(f"Community Feed")
    st.caption(f"Showing active posts in {selected_zone}")

    filter_category = st.selectbox(
        "Filter posts",
        ["All categories"] + list(CATEGORIES.keys()),
        key="feed_filter"
    )

    filtered_posts = sorted(
        zone_posts,
        key=lambda post: post["created"],
        reverse=True
    )

    if filter_category != "All categories":
        filtered_posts = [
            post for post in filtered_posts
            if post["category"] == filter_category
        ]

    if not filtered_posts:
        st.markdown("""
        <div class="post-card">
            <div style="font-size:35px;">🌱</div>
            <h3>It's quiet around here!</h3>
            <p>
                No active posts match this view yet.
                Share something useful and start the conversation.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for post in filtered_posts:
            emoji = CATEGORIES.get(post["category"], "📌")
            remaining = max(
                0,
                int((post["expires"] - datetime.now()).total_seconds() / 60)
            )

            st.markdown(
                f"""
                <div class="post-card">
                    <div class="post-category">
                        {emoji} {post["category"]}
                    </div>
                    <div class="post-message">
                        {post["message"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")}
                    </div>
                    <div class="post-meta">
                        📍 {post["zone"]} &nbsp; • &nbsp;
                        🕒 {format_time(post["created"])} &nbsp; • &nbsp;
                        ⏳ {remaining} min left
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            report_key = f"report_{post['id']}"

            if post["id"] not in st.session_state.reported_ids:
                if st.button(
                    "🚩 Report post",
                    key=report_key
                ):
                    st.session_state.reports.append({
                        "post_id": post["id"],
                        "message": post["message"],
                        "zone": post["zone"],
                        "reported_at": datetime.now()
                    })
                    st.session_state.reported_ids.add(post["id"])
                    st.success("Report submitted for moderator review.")
                    st.rerun()
            else:
                st.caption("Report submitted for this post.")


# ---------------- CREATE POST ----------------
with create_col:
    st.markdown(
        '<div class="section-label">ADD SOMETHING USEFUL</div>',
        unsafe_allow_html=True
    )
    st.header("Create a post")
    st.caption("Share information with people in your selected zone.")

    with st.form("create_post_form", clear_on_submit=True):
        category = st.selectbox(
            "What is this about?",
            list(CATEGORIES.keys())
        )

        message = st.text_area(
            "Your message",
            placeholder=(
                "Example: Found a blue water bottle "
                "near the library..."
            ),
            max_chars=500,
            height=140
        )

        expiry_minutes = st.selectbox(
            "Post duration",
            [5, 15, 30, 60],
            index=2,
            format_func=lambda x: f"{x} minutes"
        )

        st.caption(
            "Your post will leave the active feed when it expires."
        )

        publish = st.form_submit_button(
            "🚀 Publish to zone",
            type="primary",
            use_container_width=True
        )

        if publish:
            if not message.strip():
                st.warning("Please enter a message first.")
            else:
                now = datetime.now()

                st.session_state.posts.append({
                    "id": str(uuid.uuid4()),
                    "zone": selected_zone,
                    "category": category,
                    "message": message.strip(),
                    "created": now,
                    "expires": now + timedelta(
                        minutes=expiry_minutes
                    )
                })

                st.success("Your post is now live in this zone!")
                st.rerun()

    st.write("")

    st.markdown("""
    <div class="post-card">
        <div class="section-label">COMMUNITY GUIDELINES</div>
        <h3>Keep your zone welcoming.</h3>
        <p>✓ Share useful, respectful information.</p>
        <p>✓ Never post private details or precise coordinates.</p>
        <p>✓ Report inappropriate or suspicious posts.</p>
        <p>✓ Remember: screenshots may outlast a post.</p>
    </div>
    """, unsafe_allow_html=True)


# ---------------- MODERATOR REVIEW ----------------
with st.expander("🛡️ Demo moderator review queue"):
    st.caption(
        "Prototype only: this queue is not authenticated "
        "and must not be exposed as a production moderator tool."
    )

    if not st.session_state.reports:
        st.info("No reports submitted yet.")
    else:
        for index, report in enumerate(
            st.session_state.reports
        ):
            st.markdown(
                f"**Report {index + 1} · {report['zone']}**"
            )
            st.write(report["message"])
            st.caption(
                "Submitted at "
                + format_time(report["reported_at"])
            )

            if st.button(
                "Dismiss report",
                key=f"dismiss_{index}"
            ):
                st.session_state.reports.pop(index)
                st.rerun()


# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
    DROPZONE · Your community. Your zone. Your moment.<br>
    Hackathon prototype • Simulated zones • Session-based storage
</div>
""", unsafe_allow_html=True)
