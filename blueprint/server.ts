/**
 * Blueprint WebSocket Server
 *
 * Standalone Node.js server for Blueprint feature.
 * Runs on port 8002 alongside main Worker Bee backend on 8001.
 *
 * WebSocket Protocol:
 * Client → Server: { action: "generate_paths", idea: string, features: string[] }
 * Server → Client: { type: "status", message: string }
 * Server → Client: { type: "paths", data: BlueprintData }
 * Server → Client: { type: "error", error: string }
 */

import express from "express";
import cors from "cors";
import { WebSocketServer, WebSocket } from "ws";
import * as http from "http";
import * as dotenv from "dotenv";
import { generateBlueprintPaths } from "./routes/blueprint";

// Load environment variables from parent directory
dotenv.config({ path: "../.env" });

const app = express();
const PORT = 8002;

// CORS - allow requests from Lovable frontend
app.use(
  cors({
    origin: "*", // In production, restrict to your Lovable domain
    credentials: true
  })
);

app.use(express.json());

// Health check endpoint
app.get("/health", (req, res) => {
  res.json({
    status: "ok",
    service: "blueprint-server",
    version: "1.0.0",
    port: PORT,
    timestamp: new Date().toISOString()
  });
});

// Create HTTP server
const server = http.createServer(app);

// Create WebSocket server
const wss = new WebSocketServer({ server });

// Connection counter for logging
let connectionCount = 0;

// WebSocket connection handler
wss.on("connection", (ws: WebSocket) => {
  const connectionId = ++connectionCount;
  console.log(`[${new Date().toISOString()}] Blueprint client connected (ID: ${connectionId})`);

  // Send ready message (matches frontend expectation)
  ws.send(
    JSON.stringify({
      type: "blueprint_ready"
    })
  );

  // Message handler
  ws.on("message", async (message: Buffer) => {
    try {
      const data = JSON.parse(message.toString());
      console.log(`[${new Date().toISOString()}] Received action: ${data.action}`);

      if (data.action === "blueprint_paths") {
        // Validate input
        if (!data.idea) {
          ws.send(
            JSON.stringify({
              type: "blueprint_error",
              message: "Missing required field: 'idea'"
            })
          );
          return;
        }

        // Send generating status (matches frontend expectation)
        ws.send(
          JSON.stringify({
            type: "blueprint_generating"
          })
        );

        // Generate paths
        console.log(`[${new Date().toISOString()}] Generating paths for idea: "${data.idea.substring(0, 50)}..."`);

        const result = await generateBlueprintPaths(
          data.idea,
          data.features || []
        );

        if (result.ok && result.data) {
          // Success - send paths (matches frontend expectation)
          console.log(`[${new Date().toISOString()}] Successfully generated ${result.data.paths.length} paths`);

          ws.send(
            JSON.stringify({
              type: "blueprint_paths",
              data: result.data
            })
          );
        } else {
          // Error - send error message (matches frontend expectation)
          console.error(`[${new Date().toISOString()}] Error generating paths: ${result.error}`);

          ws.send(
            JSON.stringify({
              type: "blueprint_error",
              message: result.error || "Unknown error occurred"
            })
          );
        }
      } else if (data.action === "ping") {
        // Heartbeat/keepalive
        ws.send(
          JSON.stringify({
            type: "pong",
            timestamp: Date.now()
          })
        );
      } else {
        // Unknown action
        ws.send(
          JSON.stringify({
            type: "error",
            error: `Unknown action: '${data.action}'`
          })
        );
      }
    } catch (error) {
      console.error(`[${new Date().toISOString()}] Error processing message:`, error);

      ws.send(
        JSON.stringify({
          type: "error",
          error: `Server error: ${error instanceof Error ? error.message : String(error)}`
        })
      );
    }
  });

  // Error handler
  ws.on("error", (error) => {
    console.error(`[${new Date().toISOString()}] WebSocket error (ID: ${connectionId}):`, error);
  });

  // Close handler
  ws.on("close", () => {
    console.log(`[${new Date().toISOString()}] Blueprint client disconnected (ID: ${connectionId})`);
  });
});

// Start server
server.listen(PORT, () => {
  console.log("\n" + "=".repeat(70));
  console.log("🗺️  BLUEPRINT SERVER STARTED");
  console.log("=".repeat(70));
  console.log(`Port: ${PORT}`);
  console.log(`Health: http://localhost:${PORT}/health`);
  console.log(`WebSocket: ws://localhost:${PORT}`);
  console.log(`Time: ${new Date().toISOString()}`);
  console.log("=".repeat(70) + "\n");

  // Check API key
  if (!process.env.ANTHROPIC_API_KEY) {
    console.error("⚠️  WARNING: ANTHROPIC_API_KEY not found in environment");
    console.error("⚠️  Blueprint generation will fail until API key is configured");
    console.error("⚠️  Add ANTHROPIC_API_KEY to ~/worker-bee/.env\n");
  } else {
    console.log("✅ ANTHROPIC_API_KEY configured\n");
  }
});

// Graceful shutdown
process.on("SIGTERM", () => {
  console.log("\n🛑 SIGTERM received, shutting down gracefully...");

  wss.clients.forEach((client) => {
    client.close();
  });

  server.close(() => {
    console.log("✅ Blueprint server shut down complete\n");
    process.exit(0);
  });
});

process.on("SIGINT", () => {
  console.log("\n\n🛑 SIGINT received (Ctrl+C), shutting down gracefully...");

  wss.clients.forEach((client) => {
    client.close();
  });

  server.close(() => {
    console.log("✅ Blueprint server shut down complete\n");
    process.exit(0);
  });
});

// Unhandled rejection handler
process.on("unhandledRejection", (reason, promise) => {
  console.error("[${new Date().toISOString()}] Unhandled Rejection at:", promise, "reason:", reason);
});
