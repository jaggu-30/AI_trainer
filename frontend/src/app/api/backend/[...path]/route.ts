import { NextRequest, NextResponse } from "next/server";

const configuredBackendApiUrl =
  process.env.BACKEND_API_URL;
const renderBackendHostPort =
  process.env.BACKEND_API_HOSTPORT;

// Local development uses BACKEND_API_URL.  Render supplies the API service's
// private host and port, so the proxy can remain server-side without exposing
// the API URL to browser code.
const BACKEND_API_URL = (
  configuredBackendApiUrl ??
  (renderBackendHostPort
    ? `http://${renderBackendHostPort}/api/v1`
    : "http://localhost:8000/api/v1")
).replace(/\/$/, "");

type RouteContext = {
  params: Promise<{
    path: string[];
  }>;
};

async function proxyRequest(
  request: NextRequest,
  context: RouteContext,
) {
  const { path } = await context.params;

  const backendPath = path.join("/");
  const search = request.nextUrl.search;

  const targetUrl =
    `${BACKEND_API_URL}/${backendPath}${search}`;

  const headers = new Headers();

  const authorization =
    request.headers.get("authorization");

  const contentType =
    request.headers.get("content-type");

  const accept =
    request.headers.get("accept");

  if (authorization) {
    headers.set(
      "Authorization",
      authorization,
    );
  }

  if (contentType) {
    headers.set(
      "Content-Type",
      contentType,
    );
  }

  if (accept) {
    headers.set(
      "Accept",
      accept,
    );
  }

  const hasBody =
    request.method !== "GET" &&
    request.method !== "HEAD";

  const body = hasBody
    ? await request.arrayBuffer()
    : undefined;

  let response: Response;

  try {
    response = await fetch(
      targetUrl,
      {
      method: request.method,
      headers,
      body,
      cache: "no-store",
      },
    );
  } catch {
    return NextResponse.json(
      {
        detail:
          "The backend API is offline. Start the FastAPI service and try again.",
      },
      {
        status: 503,
      },
    );
  }

  const responseHeaders = new Headers();

  const responseContentType =
    response.headers.get(
      "content-type",
    );

  if (responseContentType) {
    responseHeaders.set(
      "Content-Type",
      responseContentType,
    );
  }

  return new NextResponse(
    response.body,
    {
      status: response.status,
      headers: responseHeaders,
    },
  );
}

export async function GET(
  request: NextRequest,
  context: RouteContext,
) {
  return proxyRequest(
    request,
    context,
  );
}

export async function POST(
  request: NextRequest,
  context: RouteContext,
) {
  return proxyRequest(
    request,
    context,
  );
}

export async function PUT(
  request: NextRequest,
  context: RouteContext,
) {
  return proxyRequest(
    request,
    context,
  );
}

export async function PATCH(
  request: NextRequest,
  context: RouteContext,
) {
  return proxyRequest(
    request,
    context,
  );
}

export async function DELETE(
  request: NextRequest,
  context: RouteContext,
) {
  return proxyRequest(
    request,
    context,
  );
}
