/**
 * Theme registry.
 *
 * Each theme is a CSS variable set + optional Google Fonts URL. Switching
 * themes is purely a config change; no rendering code knows about specific
 * themes. Add a new theme:
 *
 *   1. Add an entry below.
 *   2. Optionally add to `config/site.config.schema.json` enum.
 *   3. Set `theme.preset` in `config/site.config.json`.
 */

export interface Theme {
  name: string;
  description: string;
  fonts_url?: string;
  font_family: string;
  /** CSS variables applied to :root in light mode. */
  light: Record<string, string>;
  /** CSS variables applied to :root in dark mode. */
  dark: Record<string, string>;
  /** Optional extra global CSS appended after :root blocks. */
  extra_css?: string;
}

export const themes: Record<string, Theme> = {
  academic: {
    name: "Academic",
    description: "Paper-like serif aesthetic. EB Garamond. Suits researchers, writers, scientists.",
    fonts_url: "https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&display=swap",
    font_family: "'EB Garamond', Georgia, 'Times New Roman', serif",
    light: {
      "--paper": "#fbfaf6",
      "--ink": "#1a1a1a",
      "--ink-soft": "#4a4a4a",
      "--ink-muted": "#7a7a7a",
      "--rule": "#d8d4c7",
      "--link-bg": "#ffffff",
      "--link-bg-hover": "#f4efe1",
      "--accent": "#5b3a1f",
    },
    dark: {
      "--paper": "#15140f",
      "--ink": "#f0ece0",
      "--ink-soft": "#c8c4b6",
      "--ink-muted": "#8a8678",
      "--rule": "#3a372e",
      "--link-bg": "#1f1d17",
      "--link-bg-hover": "#2a2820",
      "--accent": "#c9a878",
    },
  },

  minimal: {
    name: "Minimal",
    description: "Clean sans-serif, near-white background. Apple-clean.",
    fonts_url: "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap",
    font_family: "'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif",
    light: {
      "--paper": "#ffffff",
      "--ink": "#0a0a0a",
      "--ink-soft": "#404040",
      "--ink-muted": "#737373",
      "--rule": "#e5e5e5",
      "--link-bg": "#fafafa",
      "--link-bg-hover": "#f0f0f0",
      "--accent": "#0a0a0a",
    },
    dark: {
      "--paper": "#0a0a0a",
      "--ink": "#fafafa",
      "--ink-soft": "#a3a3a3",
      "--ink-muted": "#737373",
      "--rule": "#262626",
      "--link-bg": "#171717",
      "--link-bg-hover": "#262626",
      "--accent": "#fafafa",
    },
  },

  terminal: {
    name: "Terminal",
    description: "Monospace, hacker green-on-black. For builders.",
    fonts_url: "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap",
    font_family: "'JetBrains Mono', ui-monospace, SFMono-Regular, Consolas, monospace",
    light: {
      "--paper": "#f6f7f3",
      "--ink": "#0d2818",
      "--ink-soft": "#1a3d2a",
      "--ink-muted": "#5a7268",
      "--rule": "#c8d0c4",
      "--link-bg": "#ffffff",
      "--link-bg-hover": "#e8efe5",
      "--accent": "#1a7a3d",
    },
    dark: {
      "--paper": "#0a0e0a",
      "--ink": "#7dff97",
      "--ink-soft": "#5acc7a",
      "--ink-muted": "#3d8a52",
      "--rule": "#1a2a1a",
      "--link-bg": "#0f1610",
      "--link-bg-hover": "#1a2418",
      "--accent": "#7dff97",
    },
  },

  "dark-space": {
    name: "Dark Space",
    description: "Deep navy with subtle gold accents. Cosmic vibe.",
    fonts_url: "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&display=swap",
    font_family: "'Cormorant Garamond', Georgia, serif",
    light: {
      "--paper": "#f5f5fa",
      "--ink": "#0a0e1f",
      "--ink-soft": "#2a2e4a",
      "--ink-muted": "#6a6e8a",
      "--rule": "#d0d4e0",
      "--link-bg": "#ffffff",
      "--link-bg-hover": "#ebeef5",
      "--accent": "#7a5c1f",
    },
    dark: {
      "--paper": "#05070f",
      "--ink": "#e8e8f0",
      "--ink-soft": "#b0b4c8",
      "--ink-muted": "#6a6e8a",
      "--rule": "#1a1f30",
      "--link-bg": "#0d1220",
      "--link-bg-hover": "#161c2e",
      "--accent": "#d4af6a",
    },
  },
};

export function resolveTheme(preset: string): Theme {
  return themes[preset] ?? themes.academic;
}
