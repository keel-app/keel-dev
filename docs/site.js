// keel.keellabs.dev: download links straight from the latest GitHub release, and the
// visitor's system picked out. Without this script every button opens the releases page.
(function () {
  const ASSETS = {
    "dmg": /_universal\.dmg$/,
    "msi-x64": /_x64_en-US\.msi$/,
    "msi-arm64": /_arm64_en-US\.msi$/,
    "appimage-x64": /_amd64\.AppImage$/,
    "appimage-arm64": /_aarch64\.AppImage$/,
    "deb-x64": /_amd64\.deb$/,
    "deb-arm64": /_arm64\.deb$/,
  };
  const NAMES = { macos: "macOS", windows: "Windows", linux: "Linux" };

  function detect() {
    const ua = navigator.userAgent;
    const p = ((navigator.userAgentData && navigator.userAgentData.platform) || navigator.platform || ua).toLowerCase();
    if (/android|iphone|ipad/i.test(ua)) return null; // phones: no recommendation
    if (p.includes("mac")) return { os: "macos", arm: false };
    if (p.includes("win")) return { os: "windows", arm: /arm/i.test(ua) };
    if (p.includes("linux")) return { os: "linux", arm: /aarch64|arm64/i.test(ua) };
    return null;
  }

  function primaryAsset(sys) {
    if (sys.os === "macos") return "dmg";
    if (sys.os === "windows") return sys.arm ? "msi-arm64" : "msi-x64";
    return sys.arm ? "appimage-arm64" : "appimage-x64";
  }

  async function windowsOnArm(sys) {
    // Chrome and Edge tell the CPU architecture only when asked.
    if (sys.os !== "windows" || !navigator.userAgentData || !navigator.userAgentData.getHighEntropyValues) return sys;
    try {
      const v = await navigator.userAgentData.getHighEntropyValues(["architecture"]);
      return { ...sys, arm: v.architecture === "arm" };
    } catch { return sys; }
  }

  function apply(release, sys) {
    const version = release.tag_name.replace(/^v/, "");
    document.querySelectorAll("[data-version]").forEach((el) => { el.textContent = version; });
    const urls = {};
    for (const [key, re] of Object.entries(ASSETS)) {
      const asset = (release.assets || []).find((a) => re.test(a.name));
      if (asset) urls[key] = asset.browser_download_url;
    }
    document.querySelectorAll("[data-asset]").forEach((a) => {
      if (urls[a.dataset.asset]) a.href = urls[a.dataset.asset];
    });
    const note = document.getElementById("release-note");
    note.textContent = `Keel ${version}. Free for personal and commercial local development.`;
    if (sys) {
      const key = primaryAsset(sys), primary = document.getElementById("primary-download");
      if (urls[key]) {
        primary.href = urls[key];
        primary.textContent = `Download for ${NAMES[sys.os]}`;
      }
    }
  }

  let sys = detect();
  if (sys) {
    const card = document.querySelector(`.downloads .card[data-os="${sys.os}"]`);
    if (card) card.classList.add("recommended");
  }
  Promise.all([
    fetch("https://api.github.com/repos/keel-app/keel-dev/releases/latest").then((r) => (r.ok ? r.json() : Promise.reject(r.status))),
    sys ? windowsOnArm(sys) : Promise.resolve(null),
  ]).then(([release, s]) => apply(release, s)).catch(() => { /* keep the links to the releases page */ });
})();
