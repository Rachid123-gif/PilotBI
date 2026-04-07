import { redirect } from "next/navigation";

/**
 * Root page — redirects to the dashboard.
 * The main landing page lives on pilotbi.netlify.app (index.html).
 * The Next.js app serves only the authenticated application.
 */
export default function Home() {
  redirect("/tableau-de-bord");
}
