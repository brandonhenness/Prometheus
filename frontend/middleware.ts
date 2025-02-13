import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

function getApiUrl(request: NextRequest, path: string) {
  // Get the current hostname, e.g., current.site or www.current.site
  const currentHost = request.nextUrl.hostname;
  
  // Logic to construct the API hostname.
  // For example, if the current hostname starts with "www.", remove it.
  const baseDomain = currentHost.startsWith("www.")
    ? currentHost.substring(4)
    : currentHost;
  
  // Prepend the API subdomain.
  const apiHost = `api.${baseDomain}`;
  
  // Return the full API URL.
  return `https://${apiHost}${path}`;
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const isAuthenticated = request.cookies.has("userAuth");

  // If unauthenticated users try to access protected routes, redirect them.
  if (["/", "/accounts"].includes(pathname) && !isAuthenticated) {
    // Construct the API URL dynamically.
    const redirectUrl = getApiUrl(request, "/auth/kerberos");
    return NextResponse.redirect(redirectUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/", "/accounts"],
};
