import requests
import streamlit as st
import os

# =============================
# CONFIG
# =============================
# Note: Use Render URL for cloud deployment, localhost for local docker testing
API_BASE = "http://localhost:8000"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# =============================
# API KEY & STYLES
# =============================
# Retrieval of API Key from Environment
api_key = os.getenv("TMDB_API_KEY")

st.markdown(
    """
<style>
.block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1400px; }
.small-muted { color:#6b7280; font-size: 0.92rem; }
.movie-title { font-size: 0.9rem; line-height: 1.15rem; height: 2.3rem; overflow: hidden; }
.card { border: 1px solid rgba(0,0,0,0.08); border-radius: 16px; padding: 14px; background: rgba(255,255,255,0.7); }
</style>
""",
    unsafe_allow_html=True,
)

# Check if API Key exists (Optional: display warning if missing)
if not api_key:
    st.sidebar.warning("⚠️ TMDB_API_KEY not found in Environment Variables.")

# =============================
# STATE + ROUTING
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")

if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass

def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()

def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()

# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=30)
def api_get_json(path: str, params: dict | None = None):
    try:
        # Pass API Key in params if your backend requires it
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"

def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols)
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")

            with colset[c]:
                # FIXED: Replaced use_container_width with width="stretch"
                if poster:
                    st.image(poster, width="stretch") 
                else:
                    st.write("🖼️ No poster")

                if st.button("Open", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                    if tmdb_id:
                        goto_details(tmdb_id)

                st.markdown(
                    f"<div class='movie-title'>{title}</div>", unsafe_allow_html=True
                )

def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append({
                "tmdb_id": tmdb["tmdb_id"],
                "title": tmdb.get("title") or x.get("title") or "Untitled",
                "poster_url": tmdb.get("poster_url"),
            })
    return cards

def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    keyword_l = keyword.strip().lower()
    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id: continue
            raw_items.append({
                "tmdb_id": int(tmdb_id),
                "title": title,
                "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                "release_date": m.get("release_date", ""),
            })
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id: continue
            raw_items.append({
                "tmdb_id": int(tmdb_id),
                "title": title,
                "poster_url": poster_url,
                "release_date": m.get("release_date", ""),
            })
    else:
        return [], []

    matched = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items

    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    cards = [{"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]} for x in final_list[:limit]]
    return suggestions, cards

# =============================
# SIDEBAR & HEADER
# =============================
with st.sidebar:
    st.markdown("## 🎬 Menu")
    if st.button("🏠 Home"):
        goto_home()
    st.markdown("---")
    home_category = st.selectbox("Category", ["trending", "popular", "top_rated", "now_playing", "upcoming"], index=0)
    grid_cols = st.slider("Grid columns", 4, 8, 6)

st.title("🎬 Movie Recommender")
st.divider()

# =============================
# VIEW: HOME
# =============================
if st.session_state.view == "home":
    typed = st.text_input("Search by movie title", placeholder="Type: avenger, batman...")
    st.divider()

    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters.")
        else:
            data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})
            if err: st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(data, typed.strip())
                if suggestions:
                    labels = ["-- Select a movie --"] + [s[0] for s in suggestions]
                    selected = st.selectbox("Suggestions", labels, index=0)
                    if selected != "-- Select a movie --":
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                poster_grid(cards, cols=grid_cols, key_prefix="search_results")
        st.stop()

    home_cards, err = api_get_json("/home", params={"category": home_category, "limit": 24})
    if err: st.error(f"Home feed failed: {err}")
    else: poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")

# =============================
# VIEW: DETAILS
# =============================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    col_a, col_b = st.columns([3, 1])
    with col_b:
        if st.button("← Back"): goto_home()

    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err: st.error(f"Error: {err}"); st.stop()

    left, right = st.columns([1, 2.4], gap="large")
    with left:
        if data.get("poster_url"): st.image(data["poster_url"], width="stretch")
    with right:
        st.markdown(f"## {data.get('title','')}")
        st.write(data.get("overview", "No overview."))

    st.divider()
    st.markdown("### ✅ Recommendations")
    # TF-IDF & Genre Recommendations...
    # (Rest of the recommendation logic remains the same but with FIXED image width)
    title = (data.get("title") or "").strip()
    if title:
        bundle, err2 = api_get_json("/movie/search", params={"query": title, "tfidf_top_n": 12})
        if not err2 and bundle:
            st.markdown("#### 🔎 Similar Movies")
            poster_grid(to_cards_from_tfidf_items(bundle.get("tfidf_recommendations")), cols=grid_cols, key_prefix="rec_tfidf")