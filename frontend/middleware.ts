import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const isAuthenticated = request.cookies.has("userAuth");

  // Redirect unauthenticated requests on protected routes
  if (["/", "/accounts"].includes(pathname) && !isAuthenticated) {
    // Using the internal Docker network name "backend"
    return NextResponse.redirect(new URL("http://backend/auth/login"));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/", "/accounts"],
};
