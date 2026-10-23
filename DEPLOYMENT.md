# EVCSMS Cloud Deployment Guide (Render & Vercel)

This project is fully configured for permanent, free-tier cloud hosting on **Render** (FastAPI Backend) and **Vercel** (React SPA Frontend), or as a unified full-stack service.

---

## Architecture Overview

| Component | Technology | Recommended Host | Free Tier URL Format |
| :--- | :--- | :--- | :--- |
| **Backend API** | FastAPI + SQLite + Uvicorn | [Render.com](https://render.com) | `https://evcsms-backend.onrender.com` |
| **Frontend UI** | React + Vite + Tailwind | [Vercel](https://vercel.com) | `https://evcsms.vercel.app` |
| **Full-Stack Alternative** | Unified Docker / Render Blueprint | Render Blueprint | Single combined URL |

---

## Step 1: Push the Project to Your GitHub Account

1. Open [GitHub.com](https://github.com/new) and click **New Repository**.
2. Name your repository (for example: `evcsms` or `ev-charging-system`).
3. Set visibility to **Public** or **Private** (do NOT initialize with a README/license, as we already have code).
4. In your local terminal (PowerShell in `oosmd project`), run:

```powershell
# Add your GitHub repository as remote origin (replace with your actual GitHub URL)
git remote add origin https://github.com/<YOUR-GITHUB-USERNAME>/<YOUR-REPO-NAME>.git

# Push the main branch to GitHub
git push -u origin main
```

---

## Step 2: Deploy Backend to Render (Free Web Service)

1. Sign in to [Render.com](https://dashboard.render.com/) with GitHub.
2. Click **New +** > **Web Service**.
3. Select your GitHub repository (`evcsms`).
4. Configure the service settings:
   - **Name**: `evcsms-backend` (or your choice)
   - **Region**: Choose the closest region (e.g. Frankfurt / Singapore / Oregon)
   - **Branch**: `main`
   - **Root Directory**: `evcsms/backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`
5. Under **Environment Variables**, add:
   - `SECRET_KEY` = `evcsms_super_secret_jwt_key_2026_cloud_prod`
   - `PROJECT_NAME` = `EV Charging Station Management System`
   - `DATABASE_URL` = `sqlite:///./evcsms.db`
6. Click **Create Web Service**.
7. Wait 2–3 minutes for build and boot. Render will provide your public backend URL:
   `https://evcsms-backend.onrender.com`
   - Verify it by visiting `https://evcsms-backend.onrender.com/docs` (Swagger UI).

---

## Step 3: Deploy Frontend to Vercel (Free Global CDN)

1. Sign in to [Vercel.com](https://vercel.com) using your GitHub account.
2. Click **Add New...** > **Project**.
3. Import your repository (`evcsms`).
4. In the configuration screen:
   - **Root Directory**: Click *Edit* and select `evcsms/frontend`
   - **Framework Preset**: `Vite` (auto-detected)
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Expand **Environment Variables** and add:
   - **Key**: `VITE_API_BASE_URL`
   - **Value**: `https://<YOUR-RENDER-BACKEND-NAME>.onrender.com/api/v1`
     *(Make sure to append `/api/v1` to your Render URL)*
6. Click **Deploy**.
7. Vercel will build and deploy your app in ~30 seconds and provide your live URL:
   `https://evcsms.vercel.app`

---

## Alternative: 1-Click Render Blueprint (Full-Stack Automated)

If you prefer hosting both frontend and backend on Render using the preconfigured `render.yaml`:

1. In [Render Dashboard](https://dashboard.render.com/), click **New +** > **Blueprint**.
2. Connect your repository.
3. Render reads [render.yaml](file:///c:/Users/manep/oosmd%20project/render.yaml) and automatically creates:
   - `evcsms-backend`: Python API Web Service
   - `evcsms-frontend`: Vite React Static Site
   - Automatically injects the backend URL into `VITE_API_BASE_URL`!
4. Click **Apply** to launch both services.

---

## Demo Accounts & Verification

Once deployed, open your live Vercel URL and test with the pre-seeded credentials:

| Role | Email | Password | Access |
| :--- | :--- | :--- | :--- |
| **Station Admin** | `admin@evcsms.com` | `adminpassword123` | Admin Analytics, Charger Management, Real-time telemetry |
| **EV Owner** | `owner@evcsms.com` | `ownerpassword123` | Booking slots, Active charging simulation, Wallet & Payments |
| **New User** | Any custom email | Any custom password | Free registration via `/register` |

---

## Local Development (Unchanged)

Your local development workflow remains 100% functional:
- **Backend**: `cd evcsms\backend && uvicorn app.main:app --reload`
- **Frontend**: `cd evcsms\frontend && npm run dev`
