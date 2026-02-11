# Deployment Guide: Sharia Copilot

This guide outlines the steps to deploy the Sharia Copilot application (Frontend & Backend) to Vercel.

## Prerequisites

- [Vercel CLI](https://vercel.com/download) installed and authenticated (`vercel login`).
- Environment variables for Pinecone and Google Gemini.

## 1. Backend Deployment (FastAPI)

The backend is located in the `backend/` directory and utilizes the Vercel Python runtime.

### Configuration
We have already prepared:
- `backend/requirements.txt`: Python dependencies.
- `backend/vercel.json`: Routing and runtime configuration.

### Steps
1. Navigate to the backend directory: `cd backend`
2. Deploy using Vercel CLI:
   ```bash
   vercel
   ```
3. Follow the prompts to create a new project.
4. Add the following environment variables in the Vercel dashboard:
   - `PINECONE_API_KEY`: Your Pinecone API key.
   - `GOOGLE_API_KEY`: Your Google Gemini API key.
5. Deploy to production:
   ```bash
   vercel --prod
   ```
6. **Note the deployed Backend URL** (e.g., `https://sharia-copilot-api.vercel.app`).

## 2. Frontend Deployment (Next.js)

The frontend is located in the `frontend/` directory.

### Configuration
The code is optimized to use `NEXT_PUBLIC_BACKEND_URL` for API communication.

### Steps
1. Navigate to the frontend directory: `cd frontend`
2. Deploy using Vercel CLI:
   ```bash
   vercel
   ```
3. Follow the prompts.
4. Add the following environment variable:
   - `NEXT_PUBLIC_BACKEND_URL`: The URL of your deployed backend (from Step 1).
5. Deploy to production:
   ```bash
   vercel --prod
   ```

## Summary of Environment Variables

| Project | Variable | Description |
| :--- | :--- | :--- |
| **Backend** | `PINECONE_API_KEY` | Access key for Sharia standard vector DB. |
| **Backend** | `GOOGLE_API_KEY` | Access key for Gemini AI. |
| **Frontend** | `NEXT_PUBLIC_BACKEND_URL` | The URL of the deployed FastAPI backend. |

---

> [!TIP]
> You can also connect your GitHub repository to Vercel for automatic deployments on every push. In that case, make sure to set the **Root Directory** for each Vercel project correctly (`backend/` for the API and `frontend/` for the UI).
