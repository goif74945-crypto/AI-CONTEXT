import { createHash } from "node:crypto";
import { runProbe } from "./dist/probe-core.js";
console.log(createHash("sha256").update(runProbe()).digest("hex"));
