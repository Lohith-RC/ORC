# Frontend Guidelines

## Frontend Purpose

The React frontend provides public product information, authentication, protected screening, profile editing, result history, theme selection, and browser-generated reports.

## Route Map

| Route | Access | Component | Purpose |
|---|---|---|---|
| `/` | Public | `Home` | Product landing page |
| `/about` | Public | `About` | Team and project information |
| `/contact` | Public | `Contact` | Contact presentation; form is not functional |
| `/login` | Public | `Login` | Authenticate user |
| `/register` | Public | `Register` | Create account and auto-login |
| `/upload` | Protected | `Upload` | Submit image and risk factors |
| `/profile` | Protected | `Profile` | Edit profile and view history |

## Design System

### Typography

- Body font: `Inter`
- Display/headings font: `Outfit`
- Always define a system fallback.
- Use clear, plain medical language in result states.

### Color

- Primary accent: teal/emerald
- Neutral surface: slate/gray
- Cancer/high-risk: red
- Uncertain: yellow
- Low image quality: orange
- Non-cancer/acceptable: green

Color must never be the only way status is communicated. Pair color with text and icons.

### Theme

- Tailwind class-based dark mode.
- Theme stored in `localStorage`.
- Every new screen must support both themes.

### Motion

- Framer Motion is used heavily.
- Respect `prefers-reduced-motion`.
- Avoid motion that delays access to results or creates false clinical authority.
- Disable or simplify mouse-tracking and 3D tilt on touch devices and low-power contexts.

## Component Guidelines

- Keep route components focused on page composition.
- Extract repeated cards, form fields, result badges, and API state patterns.
- Centralize API access in one client module.
- Centralize auth state in a context/provider rather than passing tokens through many components.
- Add an error boundary for unexpected rendering errors.
- Do not place clinically significant logic only in presentation components.

## API Client Guidelines

Replace hard-coded URLs with a configured base URL:

```js
const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL,
});
```

The shared client should:

- Attach authorization credentials.
- Handle `401` responses consistently.
- Normalize API errors.
- Set a reasonable timeout.
- Avoid logging sensitive responses.

## Authentication UX

- Protected routes redirect unauthenticated users to login.
- Preserve the intended destination when redirecting to login.
- Handle expired tokens explicitly.
- Do not claim logout invalidates a JWT server-side unless revocation exists.
- Prefer secure HTTP-only cookies for production after backend design review.

## Upload UX

- Accept only formats supported by the backend.
- Show maximum file size before selection.
- Validate file type and size in the browser for fast feedback.
- Preserve backend validation as authoritative.
- Explain how to capture a useful oral image:
  - Good lighting
  - Focused lesion area
  - Minimal blur
  - No filters
- Display loading progress or clear waiting state because inference runs 23 forward passes.

## Result UX

Result priority must be:

1. Screening status
2. Recommended next action
3. Medical disclaimer
4. Image-quality and clinical-risk warnings
5. Confidence and uncertainty details

Suggested guidance:

| Status | Guidance |
|---|---|
| Cancer | Seek prompt specialist evaluation; this is not a diagnosis |
| Uncertain | Image/model uncertainty is high; repeat capture and consult a specialist |
| Non-cancer | No cancer pattern detected, but persistent symptoms still require clinical review |
| Low quality | Retake the image; do not rely on the current result |
| High clinical risk | Recommend professional screening regardless of image result |

The current radial overlay labeled “Simulated Grad-CAM” is not a model explanation. Keep the label explicit or remove it until real XAI is implemented.

## Reporting Guidelines

Downloaded reports should include:

- User-entered identity only when consented
- Analysis timestamp
- Screening result
- Confidence, uncertainty, risk score, and image-quality status
- Model version
- Clear disclaimer and referral guidance

Client-generated PDFs are user convenience documents, not signed clinical records.

## Accessibility

- Target WCAG 2.2 AA.
- All controls must be keyboard operable.
- Use visible focus styles.
- Associate labels and error text with form fields.
- Announce loading, errors, and results with appropriate live regions.
- Provide alt text that describes purpose, not decorative detail.
- Ensure status colors pass contrast requirements.
- Avoid hover-only information.

## Content Integrity

- Do not display unsupported claims such as “HIPAA compliant,” validated accuracy, medical partnerships, or data sources without evidence.
- Clearly separate implemented capability from planned research.
- Use “screening,” “analysis,” or “triage support,” not “diagnosis.”

## Testing Checklist

- Public and protected route behavior
- Registration auto-login
- Login by username and email
- Upload success and every error state
- Cancer, non-cancer, uncertain, low-quality, and high-risk rendering
- PDF generation
- Profile update and history
- Light/dark themes
- Mobile, keyboard, and reduced-motion behavior

