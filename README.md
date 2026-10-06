# ViralForge Studio

ViralForge Studio is a VS Code extension that generates a render-ready vertical video project for:

- TikTok
- Instagram Reels
- YouTube Shorts

The generated project is 1080x1920, 60 FPS, 15 seconds, H.264, and uses deterministic motion graphics built with Remotion.

## Commands

Open the VS Code Command Palette and run:

- `ViralForge: Create Short Video Project`
- `ViralForge: Open Remotion Studio`
- `ViralForge: Render Current Short`

## Fast start

1. Clone or download this branch.
2. Open this folder in VS Code.
3. Run `npm install`.
4. Press `F5` to launch an Extension Development Host.
5. In the new VS Code window, open an empty working folder.
6. Run `ViralForge: Create Short Video Project`.
7. Choose TikTok, Instagram Reels, or YouTube Shorts.
8. Enter the hook, subtitle, and accent color.
9. Choose `Install + Studio` to preview or `Render Now` to produce the MP4.

## Generated video stack

- Remotion 4.0.527
- React 18.3.1
- TypeScript strict mode
- 1080x1920 vertical canvas
- 60 FPS
- H.264 render
- CRF 18 final render
- deterministic particles
- kinetic hook animation
- punch zoom and shake
- impact cards
- neon glow
- final CTA scene

No source image, video, music, or font asset is required to render the default composition.

## Build a VSIX

Run:

```bash
npm install
npm run lint
npm run package
```

The GitHub Actions workflow also verifies the JavaScript syntax and packages a VSIX artifact on pushes to `social-video-studio`.

## Scope

This branch is standalone and intentionally separated from the rest of AI-CONTEXT. Its initial commit points to an empty Git tree, so no files from `main` are present in this branch.

## License

MIT
