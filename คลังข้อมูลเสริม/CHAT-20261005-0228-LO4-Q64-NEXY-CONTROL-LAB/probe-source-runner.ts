import { createHash } from "node:crypto";
import { runProbe } from "./probe-core.ts";
console.log(createHash("sha256").update(runProbe()).digest("hex"));
