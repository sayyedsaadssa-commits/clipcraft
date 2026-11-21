import json
import os
import time
from pathlib import Path
from . import config

CAMPAIGNS_FILE = config.DATA_DIR / "whop_campaigns.json"

DEFAULT_CAMPAIGNS = [
    {
        "id": "kai_cenat",
        "creator": "Kai Cenat",
        "avatar": "https://yt3.googleusercontent.com/ytc/AIdro_k3pW6M0UoO3pW1yQY0uX7P2v6Y_X9V4A=s176-c-k-c0x00ffffff-no-rj",
        "initials": "KC",
        "title": "Kai Cenat Mafiathon & Stream Reactions",
        "category": "IRL / Comedy",
        "badge": "Top Payout",
        "payout_rate": "$1.50 / 1K views",
        "cpm": 1.50,
        "budget_total": "$25,000",
        "budget_left": "$14,800 left (59%)",
        "min_payout": "$2.00 (2K views)",
        "max_cap": "$250 / clip",
        "requirements": [
            "Must be 30s to 75s long with dynamic word-by-word captions",
            "Opening 3 seconds must have an immediate curiosity hook",
            "Must tag @kaicenat and include #KaiCenat #Mafiathon in caption",
            "No copyrighted music (streamer voice and ambient game sound only)"
        ],
        "preferred_ratio": "9:16 Vertical (1080x1920)",
        "recommended_layout": "crop",
        "recommended_layout_name": "Fill Screen (Centre Crop)",
        "recommended_style": "hype",
        "eligible_platforms": ["Instagram Reels", "TikTok", "YouTube Shorts"],
        "materials": [
            {
                "platform": "YouTube",
                "label": "Kai Cenat VODs & Streams",
                "url": "https://www.youtube.com/@KaiCenat/streams"
            },
            {
                "platform": "Twitch",
                "label": "Kai Cenat Twitch Past Broadcasts",
                "url": "https://www.twitch.tv/kaicenat/videos"
            }
        ],
        "whop_url": "https://whop.com/contentrewards",
        "notes": "Fastest approval rate on Whop. High-energy guest interactions get the most views."
    },
    {
        "id": "gta6_bounties",
        "creator": "GTA 6 & NoPixel RP",
        "avatar": "https://media.rockstargames.com/rockstargames-newsite/img/global/favicon.ico",
        "initials": "G6",
        "title": "GTA 6 News, Heists & NoPixel RP Moments",
        "category": "GTA / Gaming",
        "badge": "High Demand",
        "payout_rate": "$1.80 / 1K views",
        "cpm": 1.80,
        "budget_total": "$15,000",
        "budget_left": "$9,200 left (61%)",
        "min_payout": "$2.00 (2K views)",
        "max_cap": "$200 / clip",
        "requirements": [
            "High-adrenaline police chases, heists, or funny RP character interactions",
            "Must feature gameplay as dominant visual with facecam in top/corner",
            "Caption must include #GTA6 #GTARP #NoPixel",
            "Opening frame must display the punchy hook title"
        ],
        "preferred_ratio": "9:16 Vertical (1080x1920)",
        "recommended_layout": "gameplay",
        "recommended_layout_name": "Gameplay fills screen + Facecam in corner",
        "recommended_style": "bounce",
        "eligible_platforms": ["Instagram Reels", "TikTok", "YouTube Shorts"],
        "materials": [
            {
                "platform": "YouTube",
                "label": "Top GTA RP Live Streams",
                "url": "https://www.youtube.com/results?search_query=gta+rp+live+stream"
            },
            {
                "platform": "Twitch",
                "label": "GTA V / RP Directory Streams",
                "url": "https://www.twitch.tv/directory/category/grand-theft-auto-v"
            }
        ],
        "whop_url": "https://whop.com/contentrewards",
        "notes": "Huge viral multiplier on Instagram Reels. Keep vehicle stunts under 45 seconds."
    },
    {
        "id": "ishowspeed",
        "creator": "IShowSpeed",
        "avatar": "https://yt3.googleusercontent.com/ytc/AIdro_mC2hH6fU7x5pE4W3=s176-c-k-c0x00ffffff-no-rj",
        "initials": "SP",
        "title": "Speed IRL World Tour & Football Reactions",
        "category": "IRL / Comedy",
        "badge": "Active Bounty",
        "payout_rate": "$1.40 / 1K views",
        "cpm": 1.40,
        "budget_total": "$20,000",
        "budget_left": "$11,500 left (57%)",
        "min_payout": "$2.00 (2K views)",
        "max_cap": "$180 / clip",
        "requirements": [
            "Genuine unfiltered reactions, fan moments, or sports encounters",
            "20s to 60s length; punchline must hit before the 45s mark",
            "Tag @ishowspeed and #ishowspeed in upload caption",
            "No dangerous stunts or prohibited content"
        ],
        "preferred_ratio": "9:16 Vertical (1080x1920)",
        "recommended_layout": "zoom",
        "recommended_layout_name": "Zoomed in + Blurred fill",
        "recommended_style": "hype",
        "eligible_platforms": ["Instagram Reels", "TikTok", "YouTube Shorts"],
        "materials": [
            {
                "platform": "YouTube",
                "label": "Speed Official Stream Replays",
                "url": "https://www.youtube.com/@IShowSpeed/streams"
            }
        ],
        "whop_url": "https://whop.com/contentrewards",
        "notes": "Football and country-visit streams consistently break 500k+ views on Reels."
    },
    {
        "id": "adin_ross",
        "creator": "Adin Ross",
        "avatar": "https://yt3.googleusercontent.com/ytc/AIdro_n4=s176-c-k-c0x00ffffff-no-rj",
        "initials": "AR",
        "title": "Adin Live Streams, Guest Debates & Podcasts",
        "category": "Just Chatting",
        "badge": "High Pool",
        "payout_rate": "$1.50 / 1K views",
        "cpm": 1.50,
        "budget_total": "$30,000",
        "budget_left": "$18,200 left (60%)",
        "min_payout": "$3.00 (2K views)",
        "max_cap": "$300 / clip",
        "requirements": [
            "Podcast discussions, celebrity guest interactions, rap battles",
            "Two-speaker moments must use Split-Screen layout so both faces show",
            "Tag #AdinRoss #Kick in the post",
            "Clean subtitles with highlighted keywords"
        ],
        "preferred_ratio": "9:16 Vertical (1080x1920)",
        "recommended_layout": "split",
        "recommended_layout_name": "Split Screen: Top & Bottom (Two People)",
        "recommended_style": "clean",
        "eligible_platforms": ["Instagram Reels", "TikTok", "YouTube Shorts"],
        "materials": [
            {
                "platform": "Kick",
                "label": "Adin Ross Kick Channel",
                "url": "https://kick.com/adinross"
            },
            {
                "platform": "YouTube",
                "label": "Adin Ross Stream Highlights & VODs",
                "url": "https://www.youtube.com/results?search_query=adin+ross+stream"
            }
        ],
        "whop_url": "https://whop.com/contentrewards",
        "notes": "Celebrity guest encounters qualify for maximum bonus multipliers."
    },
    {
        "id": "jynxzi",
        "creator": "Jynxzi",
        "avatar": "https://yt3.googleusercontent.com/ytc/AIdro_j1=s176-c-k-c0x00ffffff-no-rj",
        "initials": "JZ",
        "title": "Rainbow Six Siege Clutches & Podcast",
        "category": "Gaming",
        "badge": "Active Bounty",
        "payout_rate": "$1.30 / 1K views",
        "cpm": 1.30,
        "budget_total": "$12,000",
        "budget_left": "$7,800 left (65%)",
        "min_payout": "$2.00 (2K views)",
        "max_cap": "$150 / clip",
        "requirements": [
            "1v5 clutches, microphone rage reactions, or tournament banter",
            "Loud mic reaction punchline must not be muted or clipped early",
            "Tag @jynxzi #jynxzi #r6siege",
            "Must feature readable subtitles"
        ],
        "preferred_ratio": "9:16 Vertical (1080x1920)",
        "recommended_layout": "gameplay",
        "recommended_layout_name": "Gameplay fills screen + Facecam in corner",
        "recommended_style": "bounce",
        "eligible_platforms": ["Instagram Reels", "TikTok", "YouTube Shorts"],
        "materials": [
            {
                "platform": "Twitch",
                "label": "Jynxzi Past Broadcasts",
                "url": "https://www.twitch.tv/jynxzi/videos"
            }
        ],
        "whop_url": "https://whop.com/contentrewards",
        "notes": "Best hours to clip: immediately following Sunday tournament matches."
    },
    {
        "id": "tarik_val",
        "creator": "Tarik",
        "avatar": "https://yt3.googleusercontent.com/ytc/AIdro_t7=s176-c-k-c0x00ffffff-no-rj",
        "initials": "TK",
        "title": "VCT Watch Parties & Valorant Radiant Ranked",
        "category": "Esports",
        "badge": "Competitive",
        "payout_rate": "$1.25 / 1K views",
        "cpm": 1.25,
        "budget_total": "$10,000",
        "budget_left": "$6,100 left (61%)",
        "min_payout": "$2.00 (2K views)",
        "max_cap": "$140 / clip",
        "requirements": [
            "Pro player banter, clutch defuses, hilarious ranked whiffs",
            "Killfeed and radar must remain visible with gameplay preset",
            "Tag #tarik #valorant in post",
            "Include viral question in the first 5 seconds"
        ],
        "preferred_ratio": "9:16 Vertical (1080x1920)",
        "recommended_layout": "gameplay",
        "recommended_layout_name": "Gameplay fills screen + Facecam in corner",
        "recommended_style": "clean",
        "eligible_platforms": ["Instagram Reels", "TikTok", "YouTube Shorts"],
        "materials": [
            {
                "platform": "YouTube",
                "label": "Tarik YouTube Highlights",
                "url": "https://www.youtube.com/@tarik/videos"
            },
            {
                "platform": "Twitch",
                "label": "Tarik Twitch VODs",
                "url": "https://www.twitch.tv/tarik/videos"
            }
        ],
        "whop_url": "https://whop.com/contentrewards",
        "notes": "VCT match days have 3x engagement spike across YouTube Shorts."
    }
]


def load_campaigns() -> list:
    """Loads campaigns from disk, seeding with initial high-converting campaigns if not present."""
    if not CAMPAIGNS_FILE.is_file():
        save_campaigns(DEFAULT_CAMPAIGNS)
        return DEFAULT_CAMPAIGNS
    try:
        data = json.loads(CAMPAIGNS_FILE.read_text(encoding="utf-8"))
        if isinstance(data, list) and len(data) > 0:
            return data
    except Exception:
        pass
    return DEFAULT_CAMPAIGNS


def save_campaigns(campaigns: list):
    """Saves campaigns to JSON on disk."""
    CAMPAIGNS_FILE.parent.mkdir(parents=True, exist_ok=True)
    CAMPAIGNS_FILE.write_text(json.dumps(campaigns, indent=2, ensure_ascii=False), encoding="utf-8")


def add_or_update_campaign(campaign: dict) -> list:
    """Adds or updates a campaign and persists to disk."""
    items = load_campaigns()
    cid = campaign.get("id") or f"c_{int(time.time())}"
    campaign["id"] = cid
    found = False
    for i, it in enumerate(items):
        if it.get("id") == cid:
            items[i] = {**it, **campaign}
            found = True
            break
    if not found:
        items.insert(0, campaign)
    save_campaigns(items)
    return items


def delete_campaign(cid: str) -> list:
    """Deletes a campaign by id."""
    items = [x for x in load_campaigns() if x.get("id") != cid]
    save_campaigns(items)
    return items
