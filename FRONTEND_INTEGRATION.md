# Contact Form — Frontend Integration

Backend is live at `POST /api/contact/` (see [contact/views.py](contact/views.py), [contact/serializers.py](contact/serializers.py)). This doc covers what the Next.js frontend needs to wire up `contactForm.jsx`.

## Endpoint

```
POST {NEXT_PUBLIC_API_URL}/api/contact/
Content-Type: application/json
```

## Request body

| Field | Type | Required | Notes |
|---|---|---|---|
| `full_name` | string | yes | |
| `email` | string | yes | must be a valid email |
| `phone` | string | yes | |
| `company_name` | string | no | |
| `designation` | string | no | |
| `hear_about` | string | no | one of: `"Google Search"`, `"Social Media"`, `"Referral"`, `"Advertisement"`, `"Other"` |
| `message` | string | yes | |
| `interests` | string[] | no, defaults to `[]` | subset of: `"Website"`, `"SEO"`, `"Branding"`, `"Google Ads"`, `"Meta Ads"`, `"CRM & Automation"`, `"Other"` |
| `budget` | string \| null | no | one of: `"Under $2,000"`, `"$2,000 – $5,000"`, `"$5,000 – $10,000"`, `"$10,000+"`, `"Let's Discuss"` |

Field names are `snake_case` on the wire — map from the form's `camelCase` state when building the payload.

## Responses

**201 Created** — submission saved (and a notification email is fired off to the team; failures there don't affect this response):

```json
{
  "id": 1,
  "full_name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "555-1234",
  "company_name": "",
  "designation": "",
  "hear_about": "",
  "message": "Hi there",
  "interests": ["SEO", "Other"],
  "budget": "$2,000 – $5,000",
  "created_at": "2026-06-18T06:15:48.186520Z"
}
```

**400 Bad Request** — validation failed, body is a field-keyed error map, e.g.:

```json
{ "email": ["Enter a valid email address."] }
```

## `handleSubmit` for `contactForm.jsx`

```js
const handleSubmit = async () => {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/contact/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        full_name: formData.fullName,
        email: formData.email,
        phone: formData.phone,
        company_name: formData.companyName,
        designation: formData.designation,
        hear_about: formData.hearAbout,
        message: formData.message,
        interests: selectedInterests,
        budget: selectedBudget,
      }),
    });

    if (!res.ok) {
      const errors = await res.json().catch(() => null);
      console.error("Contact form validation error:", errors);
      alert("Something went wrong. Please check the form and try again.");
      return;
    }

    alert("Form submitted successfully!");
  } catch (err) {
    console.error("Contact form network error:", err);
    alert("Something went wrong. Please try again.");
  }
};
```

## Environment

Set `NEXT_PUBLIC_API_URL` to the deployed DRF host:

- Local dev: `NEXT_PUBLIC_API_URL=http://127.0.0.1:8000` (in `.env.local`)
- Production: the Railway-deployed backend URL, e.g. `NEXT_PUBLIC_API_URL=https://<your-backend>.up.railway.app` (set in Vercel/Railway env vars for the frontend)

## CORS

The backend only accepts cross-origin requests from origins listed in `CORS_ALLOWED_ORIGINS` ([twocoreglobal_backend/settings.py](twocoreglobal_backend/settings.py)):

- `http://localhost:3000`
- `https://twocoreglobal.com`

If the frontend is deployed under a different origin (e.g. a Vercel preview URL), add it to that list or requests will be blocked by the browser with a CORS error.
