import asyncio
from playwright.async_api import async_playwright

async def search_yandex(image_path: str) -> list:
    results = []
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            page = await context.new_page()

            await page.goto("https://yandex.com/images/", timeout=30000)
            await page.wait_for_timeout(3000)

            # Try multiple possible camera button selectors
            camera_selectors = [
                '.InputChorded-Actions button',
                'button[aria-label*="image"]',
                'button[aria-label*="Image"]',
                '.cbir-button',
                '[class*="camera"]',
                '[class*="Camera"]',
            ]

            clicked = False
            for selector in camera_selectors:
                try:
                    await page.click(selector, timeout=3000)
                    clicked = True
                    break
                except:
                    continue

            if not clicked:
                # Try finding file input directly
                await page.evaluate("""
                    const input = document.querySelector('input[type="file"]');
                    if (input) input.style.display = 'block';
                """)

            await page.wait_for_timeout(1000)

            # Try to set file input
            file_inputs = [
                'input[type="file"]',
                'input[accept*="image"]',
            ]
            for selector in file_inputs:
                try:
                    await page.set_input_files(selector, image_path, timeout=5000)
                    break
                except:
                    continue

            await page.wait_for_timeout(5000)

            # Grab result links
            links = await page.eval_on_selector_all(
                'a[href]',
                'elements => elements.map(e => ({ url: e.href, text: e.innerText }))'
            )

            for link in links:
                url = link.get("url", "")
                text = link.get("text", "").strip()
                if (url.startswith("http") and
                    "yandex" not in url and
                    "google" not in url and
                    text and len(text) > 3):
                    results.append({"url": url, "title": text[:100], "source": "Yandex"})

            await browser.close()
    except Exception as e:
        results.append({"error": str(e), "source": "Yandex"})

    return results


async def search_tineye(image_path: str) -> list:
    results = []
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            page = await context.new_page()

            await page.goto("https://tineye.com/", timeout=30000)
            await page.wait_for_timeout(3000)

            # Make file input visible and upload
            await page.evaluate("""
                const inputs = document.querySelectorAll('input[type="file"]');
                inputs.forEach(i => {
                    i.style.display = 'block';
                    i.style.opacity = '1';
                    i.style.visibility = 'visible';
                });
            """)

            await page.wait_for_timeout(500)

            file_selectors = [
                'input[type="file"]',
                'input[accept*="image"]',
                '#upload_button',
            ]
            uploaded = False
            for selector in file_selectors:
                try:
                    await page.set_input_files(selector, image_path, timeout=5000)
                    uploaded = True
                    break
                except:
                    continue

            if not uploaded:
                results.append({"error": "Could not find upload input on TinEye", "source": "TinEye"})
                await browser.close()
                return results

            await page.wait_for_timeout(6000)

            # Try multiple result selectors
            result_selectors = [
                ".match a", ".result a", "article a",
                ".matches a", "[class*='result'] a"
            ]
            matches = []
            for selector in result_selectors:
                try:
                    matches = await page.eval_on_selector_all(
                        selector,
                        'elements => elements.map(e => ({ url: e.href, text: e.innerText }))'
                    )
                    if matches:
                        break
                except:
                    continue

            for match in matches:
                url = match.get("url", "")
                text = match.get("text", "").strip()
                if url.startswith("http") and "tineye" not in url:
                    results.append({"url": url, "title": text[:100] or url, "source": "TinEye"})

            await browser.close()
    except Exception as e:
        results.append({"error": str(e), "source": "TinEye"})

    return results


def run_image_search(image_path: str) -> dict:
    async def run_all():
        yandex, tineye = await asyncio.gather(
            search_yandex(image_path),
            search_tineye(image_path)
        )
        return yandex, tineye

    yandex_results, tineye_results = asyncio.run(run_all())

    return {
        "yandex": [r for r in yandex_results if "error" not in r],
        "tineye": [r for r in tineye_results if "error" not in r],
        "errors": [r for r in yandex_results + tineye_results if "error" in r]
    }