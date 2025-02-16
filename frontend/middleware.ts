import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const isAuthenticated = request.cookies.has("userAuth");

  // List the paths you want to protect (adjust as needed)
  if (["/", "/accounts"].includes(pathname) && !isAuthenticated) {
    const returnUrl = encodeURIComponent(request.nextUrl.pathname);
    // Use a relative URL since the API is on the same domain.
    const loginUrl = new URL(`/api/auth/login?returnTo=${returnUrl}`, request.url);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/", "/accounts"],
};
