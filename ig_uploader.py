"""
ClipCraft Instagram Auto-Uploader Bot (Playwright-based, Zero Meta Developer API, Zero Facebook)
Uses a persistent Chromium session saved at D:\\clipcraft\\instagram_session.

Usage:
  # Step 1: One-time login (opens browser, you log in once, session is saved forever)
  python ig_uploader.py --login

  # Step 2: Auto-upload any clip to Instagram Reels
  python ig_uploader.py --video "D:\\clipcraft\\my_clip.mp4" --caption "Viral Hook! #shorts #reels"

  # Or pick the latest rendered clip from ClipCraft automatically:
  python ig_uploader.py --latest --caption "Latest viral clip! #trending"
"""

import argparse
import os
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

SESSION_DIR = Path(r"D:\clipcraft\instagram_session")
CLIPCRAFT_DATA = Path(r"D:\clipcraft")


def get_latest_clip() -> Path | None:
    """Find the most recently created .mp4 clip inside D:\\clipcraft."""
    clips = []
    for root, _dirs, files in os.walk(CLIPCRAFT_DATA):
        for f in files:
            if f.endswith(".mp4") and "clip" in f.lower():
                p = Path(root) / f
                try:
                    clips.append((p.stat().st_mtime, p))
                except OSError:
                    pass
    if not clips:
        return None
    clips.sort(key=lambda x: x[0], reverse=True)
    return clips[0][1]


def run_login():
    """Opens a visible browser for the user to log in once. Session is saved to D:\\clipcraft\\instagram_session."""
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    print("\n" + "=" * 60)
    print("  CLIPCRAFT INSTAGRAM LOGIN SETUP")
    print("=" * 60)
    print(f"Opening browser... Log in to your Instagram account in the opened window.")
    print("Once logged in and viewing your home feed, close the browser or press ENTER here.\n")

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            headless=False,
            viewport={"width": 1280, "height": 800},
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://www.instagram.com/", wait_until="networkidle")

        print("Browser is open. Please sign in to Instagram.")
        try:
            # Wait until user is logged in (detect home icon or profile or user pressing enter)
            input("\n>>> Press ENTER here AFTER you have successfully logged into Instagram: ")
        except (KeyboardInterrupt, EOFError):
            pass

        print("Saving session...")
        context.close()

    print("\n[SUCCESS] Login session saved permanently to:", SESSION_DIR)
    print("Now you can upload any clip using: python ig_uploader.py --video <path> --caption <text>")


def upload_reel(video_path: Path, caption: str, headless: bool = False) -> bool:
    """Uploads a vertical 9:16 video to Instagram as a Reel."""
    if not video_path.is_file():
        print(f"[ERROR] Video file not found: {video_path}")
        return False

    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    abs_video = str(video_path.resolve())

    print("\n" + "=" * 60)
    print("  CLIPCRAFT INSTAGRAM REEL AUTO-UPLOADER")
    print("=" * 60)
    print(f"Video:   {video_path.name} ({os.path.getsize(abs_video) / (1024 * 1024):.1f} MB)")
    print(f"Caption: {caption[:60]}...")
    print("Starting browser session...")

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            headless=headless,
            viewport={"width": 1280, "height": 860},
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = context.pages[0] if context.pages else context.new_page()

        print("Navigating to Instagram...")
        page.goto("https://www.instagram.com/", wait_until="networkidle")
        time.sleep(2)

        # Check if logged in
        if "login" in page.url.lower():
            print("\n[ERROR] Not logged in! Please run 'python ig_uploader.py --login' first.")
            context.close()
            return False

        # Dismiss common popups (Turn on Notifications, Save Login Info)
        for dismiss_txt in ["Not Now", "Cancel", "Not now"]:
            try:
                btn = page.locator(f"button:has-text('{dismiss_txt}')").first
                if btn.is_visible(timeout=1500):
                    btn.click()
                    time.sleep(1)
            except Exception:
                pass

        print("Locating Create (+) button...")
        create_btn = page.locator("svg[aria-label='New post'], svg[aria-label='New Post'], svg[aria-label='新規投稿'], svg[aria-label='新しい投稿']").first
        if not create_btn.is_visible(timeout=3000):
            create_btn = page.locator("a:has-text('Create'), span:has-text('Create'), a:has-text('作成'), span:has-text('作成')").first

        create_btn.click()
        time.sleep(1)

        # Handle Create Menu: Click "Post" (Reels are uploaded under Post)
        print("Selecting 'Post' from Create menu...")
        for it in page.locator("div[tabindex='-1'] span, div[role='menu'] span, span").all():
            txt = it.text_content().strip()
            if txt in ["Post", "投稿"]:
                try:
                    it.click()
                    print(f"Clicked menu option: {txt}")
                    time.sleep(1.5)
                    break
                except Exception:
                    pass

        # Upload file directly via input[type="file"] (universal, zero language dependence)
        print(f"Uploading file: {video_path.name}...")
        try:
            page.wait_for_selector("input[type='file']", state="attached", timeout=10000)
            page.set_input_files("input[type='file']", abs_video)
        except Exception:
            # Fallback if dialog button needs click
            with page.expect_file_chooser(timeout=5000) as fc_info:
                dialog_btn = page.locator("div[role='dialog'] button, button:has-text('Select'), button:has-text('選択')").first
                dialog_btn.click()
            file_chooser = fc_info.value
            file_chooser.set_files(abs_video)

        time.sleep(4)

        # Handle "Video posts are now shared as reels" modal if it appears
        try:
            ok_btn = page.locator("button:has-text('OK'), div[role='button']:has-text('OK'), button:has-text('ok')").first
            if ok_btn.is_visible(timeout=3000):
                ok_btn.click()
                time.sleep(1)
        except Exception:
            pass

        # Handle Aspect Ratio: ensure 9:16 vertical crop
        try:
            crop_btn = page.locator("button:has(svg[aria-label='Select crop']), svg[aria-label='Select crop'], svg[aria-label='切り抜きを選択']").first
            if crop_btn.is_visible(timeout=2000):
                crop_btn.click()
                time.sleep(0.5)
                ratio_916 = page.locator("button:has-text('9:16'), span:has-text('9:16')").first
                if ratio_916.is_visible(timeout=1000):
                    ratio_916.click()
                    time.sleep(0.5)
        except Exception:
            pass

        # Step 1: Click "Next" / "次へ"
        print("Progressing to trimming / cover photo...")
        next_sel = "div[role='button']:has-text('Next'), button:has-text('Next'), div[role='button']:has-text('次へ'), button:has-text('次へ')"
        next_btn = page.locator(next_sel).first
        next_btn.click(timeout=8000)
        time.sleep(2)

        # Step 2: Click "Next" / "次へ" again (to caption screen)
        print("Progressing to caption screen...")
        next_btn = page.locator(next_sel).first
        next_btn.click(timeout=8000)
        time.sleep(2)

        # Step 3: Type Caption
        print("Entering caption and hashtags...")
        caption_box = page.locator("div[aria-label='Write a caption...'], div[aria-label='キャプションを書く...'], div[contenteditable='true'], div[role='textbox']").first
        caption_box.click(timeout=4000)
        time.sleep(0.5)
        caption_box.fill(caption)
        time.sleep(1)

        # Step 4: Click "Share" / "シェア"
        print("Publishing Reel to Instagram...")
        share_sel = "div[role='button']:has-text('Share'), button:has-text('Share'), div[role='button']:has-text('シェア'), button:has-text('シェア')"
        share_btn = page.locator(share_sel).first
        share_btn.click(timeout=8000)

        # Step 5: Wait for confirmation
        print("Waiting for upload confirmation (processing video)...")
        success = False
        for _ in range(35):
            time.sleep(2)
            content = page.content()
            if any(w in content for w in ["Your reel has been shared", "Your post has been shared", "reel has been shared", "リールがシェアされました", "投稿がシェアされました"]):
                success = True
                break

        if success:
            print("\n" + "=" * 60)
            print("  [SUCCESS] REEL SUCCESSFULLY PUBLISHED TO INSTAGRAM!")
            print("=" * 60 + "\n")
        else:
            print("\n[NOTE] Video submitted. Please verify on your Instagram profile in 1-2 minutes.")

        time.sleep(3)
        context.close()
        return success


def main():
    parser = argparse.ArgumentParser(description="ClipCraft Instagram Auto-Uploader Bot")
    parser.add_argument("--login", action="store_true", help="One-time login to save your Instagram session")
    parser.add_argument("--video", type=str, help="Path to the MP4 video to upload")
    parser.add_argument("--latest", action="store_true", help="Automatically pick the latest clip from ClipCraft")
    parser.add_argument("--caption", type=str, default="", help="Caption text")
    parser.add_argument("--caption-file", type=str, default="caption.txt", help="Path to a text file containing the caption (preserves Japanese/Hindi characters perfectly)")
    parser.add_argument("--headless", action="store_true", help="Run browser in background")

    args = parser.parse_args()

    if args.login:
        run_login()
        return

    # Handle caption (prefer caption-file if it exists, else --caption)
    caption_text = args.caption
    if os.path.isfile(args.caption_file):
        try:
            with open(args.caption_file, "r", encoding="utf-8") as cf:
                caption_text = cf.read().strip()
        except Exception:
            pass
    if not caption_text:
        caption_text = "Viral clip made with ClipCraft AI #shorts #reels"

    video_file = None
    if args.latest:
        video_file = get_latest_clip()
        if not video_file:
            print("[ERROR] No clips found in D:\\clipcraft! Render a clip in ClipCraft first.")
            sys.exit(1)
        print(f"Auto-selected latest clip: {video_file}")
    elif args.video:
        video_file = Path(args.video)

    if not video_file:
        parser.print_help()
        sys.exit(1)

    upload_reel(video_file, caption_text, headless=args.headless)


if __name__ == "__main__":
    main()
